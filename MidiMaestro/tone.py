import numpy as np

class Tone:
    def __init__(self, fundamental_frequency, overtone_intensities, envelope):
        self._ff = fundamental_frequency
        self._overtone_intensities = overtone_intensities
        self._envelope = envelope
        self._key_down = False
        self._buffer = np.array([])
        self._buffer_position = 0

    def get_harmonics(self):
        return [(self._ff*(i+1), intensity) for (i, intensity) in enumerate(self._overtone_intensities)]

    # def build_waveform(self, envelope):
    #     waveform = envelope.envelope_frequency(self._ff)
    #     waveform /= max(waveform)
    #     return waveform

    def get_samples(self, samples_requested):
        samples_remaining = len(self._buffer) - self._buffer_position

        if samples_remaining >= samples_requested:
            chunk_start = self._buffer_position
            chunk_end = self._buffer_position + samples_requested
            self._buffer_position += samples_requested
            return self._buffer[chunk_start:chunk_end]
        elif self._key_down:
            additional_samples_needed = samples_requested - samples_remaining
            sustain_waveform = np.zeros(additional_samples_needed)
            for frequency, intensity in self.get_harmonics():
                sustain_waveform += intensity * self._envelope.get_sustain_waveform(frequency, additional_samples_needed)
            self._buffer = np.append(self._buffer, sustain_waveform)
            chunk_start = self._buffer_position
            chunk_end = self._buffer_position + samples_requested
            self._buffer_position += samples_requested
            return self._buffer[chunk_start:chunk_end]
        else:
            chunk_start = self._buffer_position
            self._buffer_position += samples_remaining
            return self._buffer[chunk_start:]

    def key_pressed(self):
        self._key_down = True
        
        attack_waveform = np.zeros(self._envelope.attack_sample_count())
        decay_waveform = np.zeros(self._envelope.decay_sample_count())
        for frequency, intensity in self.get_harmonics():
            attack_waveform += intensity * self._envelope.get_attack_waveform(frequency)
            decay_waveform += intensity * self._envelope.get_decay_waveform(frequency)

        self._buffer = np.append(attack_waveform, decay_waveform)
        self._buffer_position = 0

    def key_released(self):
        self._key_down = False
        release_waveform = np.zeros(self._envelope.release_sample_count())
        for frequency, intensity in self.get_harmonics():
            release_waveform += intensity * self._envelope.get_release_waveform(frequency)
        self._buffer = np.append(self._buffer, release_waveform)