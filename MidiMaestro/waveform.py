import numpy as np
import sounddevice as sd


fs = 44100  # Sampling rate

class Waveform:

    def __init__(self, duration):
        self.duration = duration
        self.frequencies = list()

    def add_frequency(self, frequency, relative_volume=1):
        self.frequencies.append((frequency, relative_volume))

    def play(self):
        total_samples = int(fs * self.duration)
        samplepoints = np.linspace(0, self.duration, total_samples, endpoint=False)
        audio_signal = np.linspace(0, 0, total_samples, endpoint=False)
        for (frequency, relative_volume) in self.frequencies:
            audio_signal += 0.5 * relative_volume * np.sin(2 * np.pi * frequency * samplepoints)

        audio_signal /= max(audio_signal)
        print(audio_signal)

        sd.play(audio_signal, samplerate=fs)

# def build(frequency, duration):
#     time = np.linspace(0, duration, int(fs * duration), endpoint=False)
#     audio_signal = 0.5 * np.sin(2 * np.pi * frequency * time)

#     sd.play( (audio_signal) , samplerate=fs)
