import numpy as np
import sounddevice as sd

from MidiMaestro.envelope import Envelope
from MidiMaestro.tone import Tone

# Generate a simple tone
fs = 44100  # Sampling rate
frequency = 440  # Hz
duration = 1  # seconds
time = np.linspace(0, duration, int(fs * duration), endpoint=False)
audio_signal = 1 * np.sin(2 * np.pi * frequency * time)

# audio_signal2 = 0.5 * np.sin(2 * np.pi * frequency*2 * time)

# audio_signal3 = (1/16) * np.sin(2 * np.pi * frequency*4 * time)

# print(max(audio_signal2 + audio_signal))

# fade = np.linspace(1, 0, int(fs * duration), endpoint=False)

###### testing envelope
e = Envelope(100, 50, 0.25, 5000, 500)
t = Tone(440, [1, 0.8, 0.6, 0.5, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1])
audio_signal = t.build_waveform(e)

# Send signal to speakers
sd.play( (audio_signal) , samplerate=fs)
sd.wait()