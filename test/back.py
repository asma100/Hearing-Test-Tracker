import numpy as np
import sounddevice as sd
from flask import Flask, jsonify, request, send_file,render_template
from io import BytesIO
import wave

app = Flask(__name__)

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
@app.route("/")
def home():
    return render_template('front.html')

@app.route('/generate_tone', methods=['POST'])
def generate_tone():
    data = request.json
    duration = data.get('duration', 1.0)
    frequency = data.get('frequency', 440.0)
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
    return send_file(byte_io, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(debug=True)
