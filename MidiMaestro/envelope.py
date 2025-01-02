import numpy as np

import MidiMaestro.constants as constants
from MidiMaestro.waveform import Waveform

fs = 44100  # Sampling rate

class Envelope:
    def __init__(self, attack_ms, decay_ms, sustain_level, sustain_ms, release_ms):
        self.attack_ms = attack_ms
        self.decay_ms = decay_ms
        self.sustain_level = sustain_level
        self.sustain_ms = sustain_ms
        self.release_ms = release_ms
        self.sustain_position = self.attack_sample_count() + self.decay_sample_count()

    def envelope_frequency(self, frequency):
        attack_sample_count = int(fs * self.attack_ms / 1000)
        attack_samples = np.linspace(0, self.attack_ms/1000, attack_sample_count, endpoint=False)
        attack_signal_flat = 0.5 * np.sin(2 * np.pi * frequency * attack_samples)
        attack_signal = np.array([x*(i/attack_sample_count) for (i, x) in enumerate(attack_signal_flat)])

        decay_sample_count = int(fs * self.decay_ms / 1000)
        decay_samples = np.linspace(0, self.decay_ms/1000, decay_sample_count, endpoint=False)
        decay_signal_flat = 0.5 * np.sin(2 * np.pi * frequency * decay_samples)
        decay_signal = np.array([x*((decay_sample_count-(i*(1-self.sustain_level)))/decay_sample_count) for (i, x) in enumerate(decay_signal_flat)])
        
        sustain_sample_count = int(fs * self.sustain_ms / 1000)
        sustain_samples = np.linspace(0, self.sustain_ms/1000, sustain_sample_count, endpoint=False)
        sustain_signal = 0.5 * np.sin(2 * np.pi * frequency * sustain_samples) * self.sustain_level

        release_sample_count = int(fs * self.release_ms/ 1000)
        release_samples = np.linspace(0, self.release_ms/1000, release_sample_count, endpoint=False)
        release_signal_flat = 0.5 * np.sin(2 * np.pi * frequency * release_samples)
        release_signal = np.array([x * ((self.sustain_level-(i*self.sustain_level/release_sample_count))) for (i, x) in enumerate(release_signal_flat)])
        
        return np.append(np.append(np.append(attack_signal, decay_signal), sustain_signal), release_signal)

    def apply_to_tone(self, tone):
        for frequency, intensity in tone.get_harmonics():
            print(frequency)
            self.envelope_frequency(frequency)

    def attack_sample_count(self):
        return int(fs * self.attack_ms / 1000)

    def decay_sample_count(self):
        return int(fs * self.decay_ms / 1000)
    
    def release_sample_count(self):
        return int(fs * self.release_ms / 1000)

    def get_attack_waveform(self, frequency):
        attack_sample_count = self.attack_sample_count()
        attack_samples = np.linspace(0, self.attack_ms/1000, attack_sample_count, endpoint=False)
        attack_signal_flat = 0.5 * np.sin(2 * np.pi * frequency * attack_samples)
        return np.array([x*(i/attack_sample_count) for (i, x) in enumerate(attack_signal_flat)])

    def get_decay_waveform(self, frequency):
        decay_sample_count = self.decay_sample_count()
        decay_samples = np.linspace(0, self.decay_ms/1000, decay_sample_count, endpoint=False) + self.attack_sample_count()
        decay_signal_flat = 0.5 * np.sin(2 * np.pi * frequency * decay_samples)
        return np.array([x*((decay_sample_count-(i*(1-self.sustain_level)))/decay_sample_count) for (i, x) in enumerate(decay_signal_flat)])

    def get_sustain_waveform(self, frequency, samples_requested):
        samples_per_cycle = constants.samplerate / frequency
        samples_to_return = max(samples_requested, samples_per_cycle)
        time_in_seconds = samples_to_return / constants.samplerate
        sustain_samples = np.linspace(0, time_in_seconds, samples_to_return, endpoint=False) + self.sustain_position
        self.sustain_position += samples_to_return
        return 0.5 * np.sin(2 * np.pi * frequency * sustain_samples)

    def get_release_waveform(self, frequency):
        release_sample_count = self.release_sample_count()
        release_samples = np.linspace(0, self.release_ms/1000, release_sample_count, endpoint=False) + self.sustain_position
        release_signal_flat = 0.5 * np.sin(2 * np.pi * frequency * release_samples)
        return np.array([x * ((self.sustain_level-(i*self.sustain_level/release_sample_count))) for (i, x) in enumerate(release_signal_flat)])