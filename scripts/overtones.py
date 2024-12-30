import time

from MidiMaestro.waveform import Waveform

bf = 261.63

w = Waveform(1)

w.add_frequency(bf, 1)
w.add_frequency(bf*2, 0.7)
w.add_frequency(bf*3, 0.5)
w.add_frequency(bf*4, 0.4)
w.add_frequency(bf*5, 0.3)
w.add_frequency(bf*6, 0.2)
w.add_frequency(bf*7, 0.15)
w.add_frequency(bf*8, 0.1)

# w.add_frequency(440, 1)
# w.add_frequency(660, 0.2)
# w.add_frequency(880, 0.2)
# w.add_frequency(660, 0.2)
# w.add_frequency(660, 0.2)
w.play()
time.sleep(2)