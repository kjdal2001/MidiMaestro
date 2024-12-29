import simpleaudio as sa
import numpy as np

def play_tone(frequency, duration):
    """Plays a piano tone with the given frequency and duration."""

    # Create the waveform (sine wave)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    waveform = np.sin(2 * np.pi * frequency * t)

    # Normalize and convert to 16-bit PCM format
    waveform *= 32767 / np.max(np.abs(waveform))
    waveform = waveform.astype(np.int16)

    # Play the sound
    audio = sa.play_buffer(waveform, 1, 2, sample_rate)
    audio.wait_done()

if __name__ == "__main__":
    # Example: Play middle C (C4) for 1 second
    play_tone(261.63, 1)  # 261.63 Hz is the frequency for middle C