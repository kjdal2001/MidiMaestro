import numpy as np
from pynput import keyboard
import sounddevice as sd
import time

import MidiMaestro.constants as constants
from MidiMaestro.envelope import Envelope
from MidiMaestro.tone import Tone

start_idx = 0
buffer = np.array([])

e = Envelope(100, 50, 0.25, 2000, 500)
t = Tone(440, [1, 0.8, 0.6, 0.5, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1])
audio_signal = t.build_waveform(e)


def callback(outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    global start_idx

    remaining_signal = len(buffer) - start_idx
    print(f"{frames} {remaining_signal} {len(buffer)}")
    valid_frames = frames if frames < remaining_signal else remaining_signal
    outdata[:valid_frames] = buffer[start_idx:start_idx+valid_frames].reshape(-1, 1)
    outdata[valid_frames:] = 0
    start_idx += valid_frames

def on_press(key):
    global buffer
    buffer = np.append(buffer, audio_signal)
    print(f"appended {len(audio_signal)} to a total of {len(buffer)}")

listener = keyboard.Listener(on_press=on_press)
listener.start()

with sd.OutputStream(device=7, channels=1, callback=callback, samplerate=constants.samplerate):
    time.sleep(10)
