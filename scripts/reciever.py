import numpy as np
import sounddevice as sd

import mido
#from mido import MidiInput

# List available MIDI input ports
print("Available MIDI input ports:")
print(mido.get_input_names())

# Open the Roland FP-30X input port
port_name = 'Roland Digital Piano:Roland Digital Piano MIDI 1 20:0'  # Replace with your port name
with mido.open_input(port_name) as inport:
    print(f"Listening to MIDI data from {port_name}...")

    for msg in inport:
        print(msg)  # Print received MIDI messages