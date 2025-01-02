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
t = Tone(440, [1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], e)
# audio_signal = t.build_waveform(e)


def callback(outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    # global start_idx

    # remaining_signal = len(buffer) - start_idx
    # print(f"{frames} {remaining_signal} {len(buffer)}")
    # valid_frames = frames if frames < remaining_signal else remaining_signal
    # outdata[:valid_frames] = buffer[start_idx:start_idx+valid_frames].reshape(-1, 1)
    # outdata[valid_frames:] = 0
    # start_idx += valid_frames

    global t
    samples = t.get_samples(frames)
    valid_frames = min(frames, len(samples))
    outdata[:valid_frames] = samples.reshape(-1, 1)
    outdata[valid_frames:] = 0

key_is_down = False

def on_press(key):
    global t
    global key_is_down
    if key.char == 'a' and key_is_down is False:
        print("pressed!")
        key_is_down = True
        t.key_pressed()

def on_release(key):
    global t
    global key_is_down
    if key.char == "a" and key_is_down is True:
        print("released!")
        key_is_down = False
        t.key_released()

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

with sd.OutputStream(device=7, channels=1, callback=callback, samplerate=constants.samplerate):
    time.sleep(10)
