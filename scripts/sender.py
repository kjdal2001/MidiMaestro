import time
import mido

port_name = 'Roland Digital Piano:Roland Digital Piano MIDI 1 20:0'
with mido.open_output(port_name) as outport:
    msg = mido.Message('note_on', channel=0, note=70)
    outport.send(msg)
    time.sleep(1)
    # pitch_bend = mido.Message('pitchwheel', channel=0, pitch=8191)
    # outport.send(pitch_bend)
    time.sleep(1)
    # msg2 = msg.copy(note=71)
    # outport.send(msg2)