import numpy as np
import sounddevice as sd

# Generate a simple tone
fs = 44100  # Sampling rate
frequency = 500  # Hz
duration = 1  # seconds
time = np.linspace(0, duration, int(fs * duration), endpoint=False)
audio_signal = 0.5 * np.sin(2 * np.pi * frequency * time)

# Send signal to speakers
sd.play(audio_signal, samplerate=fs)
sd.wait()