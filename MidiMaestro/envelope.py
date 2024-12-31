import numpy as np

from MidiMaestro.waveform import Waveform

fs = 44100  # Sampling rate

class Envelope:
    def __init__(self, attack_ms, decay_ms, sustain_level, sustain_ms, release_ms):
        self.attack_ms = attack_ms
        self.decay_ms = decay_ms
        self.sustain_level = sustain_level
        self.sustain_ms = sustain_ms
        self.release_ms = release_ms

    def apply(self, frequency):
        attack_sample_count = int(fs * self.attack_ms / 1000)
        attack_samples = np.linspace(0, self.attack_ms, attack_sample_count, endpoint=False)
        attack_signal_flat = 0.5 * np.sin(2 * np.pi * frequency * attack_samples)
        attack_signal = np.array([x*(i/attack_sample_count) for (i, x) in enumerate(attack_signal_flat)])

        decay_sample_count = int(fs * self.decay_ms / 1000)
        decay_samples = np.linspace(0, self.decay_ms, decay_sample_count, endpoint=False)
        decay_signal_flat = 0.5 * np.sin(2 * np.pi * frequency * decay_samples)
        decay_signal = np.array([x*((decay_sample_count-(i*(1-self.sustain_level)))/decay_sample_count) for (i, x) in enumerate(decay_signal_flat)])
        
        sustain_sample_count = int(fs * self.sustain_ms / 1000)
        sustain_samples = np.linspace(0, self.sustain_ms, sustain_sample_count, endpoint=False)
        sustain_signal = 0.5 * np.sin(2 * np.pi * frequency * sustain_samples) * self.sustain_level

        release_sample_count = int(fs * self.release_ms/ 1000)
        release_samples = np.linspace(0, self.release_ms, release_sample_count, endpoint=False)
        release_signal_flat = 0.5 * np.sin(2 * np.pi * frequency * release_samples)
        release_signal = np.array([x * ((self.sustain_level-(i*self.sustain_level/release_sample_count))) for (i, x) in enumerate(release_signal_flat)])
        
        return np.append(np.append(np.append(attack_signal, decay_signal), sustain_signal), release_signal)