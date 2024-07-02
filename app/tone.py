import numpy as np
import sounddevice as sd


a0 = 1e-5 
sr = 44100
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


if __name__ == '__main__':
    ear='left'
    tone = sinusoid(d=1, f=250, phi=0, l=60, channel=ear)
    sd.play(tone, 44100)
    sd.wait()