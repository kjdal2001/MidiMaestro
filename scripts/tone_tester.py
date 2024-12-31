import numpy as np
import sounddevice as sd

from MidiMaestro.envelope import Envelope

# Generate a simple tone
fs = 44100  # Sampling rate
# frequency = 500  # Hz
# duration = 1  # seconds
# time = np.linspace(0, duration, int(fs * duration), endpoint=False)
# audio_signal = 1 * np.sin(2 * np.pi * frequency * time)

# audio_signal2 = 0.5 * np.sin(2 * np.pi * frequency*2 * time)

# audio_signal3 = (1/16) * np.sin(2 * np.pi * frequency*4 * time)

# print(max(audio_signal2 + audio_signal))

# fade = np.linspace(1, 0, int(fs * duration), endpoint=False)

###### testing envelope
e = Envelope(10, 10, 0.75, 1000, 500)
audio_signal = e.apply(440)

# Send signal to speakers
sd.play( (audio_signal) , samplerate=fs)
sd.wait()