class Tone:
    def __init__(self, fundamental_frequency, overtone_intensities):
        self.ff = fundamental_frequency
        self.overtone_intensities = overtone_intensities

    def get_harmonics(self):
        return [(self.ff*(i+1), intensity) for (i, intensity) in enumerate(self.overtone_intensities)]

    def build_waveform(self, envelope):
        # waveform = envelope.get_empty_wave()
        # for frequency, intensity in self.get_harmonics():
            # waveform += intensity * envelope.envelope_frequency(frequency)

        waveform = envelope.envelope_frequency(self.ff)
        print(self.ff)
        waveform /= max(waveform)
        return waveform