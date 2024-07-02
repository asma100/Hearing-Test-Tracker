import numpy as np
import sounddevice as sd
from app.models import User, TestResult,LTestvalue,RTestvalue
from app import db
from flask_login import current_user
from flask import request

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
def handle_playtone_request(request, freq):
    dbLevel = request.form.get('dbLevel')
    heard = request.form.get('heard')
    userEar = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.id.desc()).first()


    if not userEar:
        print("No ear entry found for the current user!")
        return False

    ear = userEar.ear
    userResult = None

    if ear == 'left':
        userResult = LTestvalue.query.filter_by(user_id=current_user.id).order_by(LTestvalue.id.desc()).first()

        if not userResult:
            userResult = LTestvalue(user_id=current_user.id)
            db.session.add(userResult)
    elif ear == 'right':
        userResult = RTestvalue.query.filter_by(user_id=current_user.id).order_by(RTestvalue.id.desc()).first()
        if not userResult:
            userResult = RTestvalue(user_id=current_user.id)
            db.session.add(userResult)

    if dbLevel:
        print(f"Playing tone: Frequency={freq} Hz, dB Level={dbLevel}, Ear={ear}")
        tone = sinusoid(d=1, f=freq, phi=0, l=float(dbLevel), channel=ear)
        sd.play(tone, sr)
        sd.wait()

    if heard:
        print(f"Heard at {freq} Hz: {heard} dB")
        setattr(userResult, f'f{freq}db', float(heard))
        db.session.commit()

    return heard

def classify_hearing_level(dB):
    if dB is None:
        return 'No data'
    if dB <= 25:
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
    
    valid_dB_values = [getattr(user_result, freq) for freq in frequencies if getattr(user_result, freq) is not None]
    overall_assessment = classify_hearing_level(sum(valid_dB_values) / len(valid_dB_values) if valid_dB_values else None)
    
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