import mido

def list_midi_ports():
    print("Available MIDI Ports:")
    for port in mido.get_output_names():
        print(port)

# List available MIDI output ports
list_midi_ports()
