import numpy as np
import sounddevice as sd
from app.models import User, TestResult,LTestvalue,RTestvalue
from app import db
from flask_login import current_user
from flask import request

from io import BytesIO
import wave


a0 = 1e-5  # reference amplitude
sr = 44100  # sample rate

def sinusoid(d, f, phi, l, a0=a0, sr=sr, channel='both'):
    t = np.arange(0, int(round(d * sr))) / sr
    mono_tone = a0 * 10 ** (l / 20) * np.sin(2 * np.pi * f * t + phi)
    
    if channel == 'left':
        stereo_tone = np.column_stack((mono_tone, np.zeros_like(mono_tone)))
    elif channel == 'right':
        stereo_tone = np.column_stack((np.zeros_like(mono_tone), mono_tone))
    else:  # both
        stereo_tone = np.column_stack((mono_tone, mono_tone))
    
    return stereo_tone

def generate_tone_file(data):
    duration = data.get('duration', 1.0)
    frequency = data.get('frequency', 250.0)
    amplitude = data.get('amplitude', 0.1)
    phase = data.get('phase', 0.0)
    channel = data.get('channel', 'both')
    
    tone = sinusoid(duration, frequency, phase, amplitude, channel=channel)
    byte_io = BytesIO()
    
    with wave.open(byte_io, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes((tone * 32767).astype(np.int16).tobytes())
    
    byte_io.seek(0)
    return byte_io

def handle_playtone_request(request, freq):
    dbLevel = request.form.get('amplitude')
    heard = request.form.get('heard')
    userEar = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.id.desc()).first()

    if not userEar:
        print("No ear entry found for the current user!")
        return False, None, None

    ear = userEar.ear
    userResult = None

    if ear == 'left':
        userResult = LTestvalue.query.filter_by(user_id=current_user.id).order_by(LTestvalue.id.desc()).first()

        if userResult and all([userResult.f250db, userResult.f500db, userResult.f1000db, userResult.f2000db, userResult.f4000db, userResult.f8000db]):
            userResult = LTestvalue(user_id=current_user.id)
            db.session.add(userResult)
        elif not userResult:
            userResult = LTestvalue(user_id=current_user.id)
            db.session.add(userResult)
    elif ear == 'right':
        userResult = RTestvalue.query.filter_by(user_id=current_user.id).order_by(RTestvalue.id.desc()).first()

        if userResult and all([userResult.f250db, userResult.f500db, userResult.f1000db, userResult.f2000db, userResult.f4000db, userResult.f8000db]):
            userResult = RTestvalue(user_id=current_user.id)
            db.session.add(userResult)
        if not userResult:
            userResult = RTestvalue(user_id=current_user.id)
            db.session.add(userResult)

    
    if dbLevel:
        print(f"Playing tone: Frequency={freq} Hz, dB Level={dbLevel}, Ear={ear}")
        

    if heard:
        print(f"Heard at {freq} Hz: {heard} dB")
        setattr(userResult, f'f{freq}db', float(heard))
        db.session.commit()

    return heard


def classify_hearing_level(dB):
    if dB is None:
        return 'No data'
    if dB <= 30:
        return 'Normal hearing'
    elif dB <= 40:
        return 'Mild hearing loss'
    elif dB <= 55:
        return 'Moderate hearing loss'
    elif dB <= 70:
        return 'Moderately severe hearing loss'
    elif dB <= 90:
        return 'Severe hearing loss'
    else:
        return 'Profound hearing loss'

def evaluate_hearing(user_result):
    frequencies = ['f250db', 'f500db', 'f1000db', 'f2000db', 'f4000db', 'f8000db']
    results = {}
    for freq in frequencies:
        dB = getattr(user_result, freq, None)
        results[freq] = classify_hearing_level(dB)
    
    # Determine the overall assessment (you can modify this logic as needed)
    overall_assessment = "Normal hearing"
    if any(classify_hearing_level(getattr(user_result, freq, None)) != 'Normal hearing' for freq in frequencies):
        overall_assessment = "Hearing loss detected"

    return results, overall_assessment
    

    
def evaluate_hearing_o(results):
    frequencies = ['f250db', 'f500db', 'f1000db', 'f2000db', 'f4000db', 'f8000db']
    valid_dB_values = []

    for result in results:
        for freq in frequencies:
            dB = getattr(result, freq)
            if dB is not None:
                valid_dB_values.append(dB)

    overall_assessment = classify_hearing_level(sum(valid_dB_values) / len(valid_dB_values)) if valid_dB_values else 'No data'
    
    return overall_assessment
