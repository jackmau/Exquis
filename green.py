import time
import rtmidi

def send_blank_message(midi_out, key_index):
    sys_ex_data = [0xF0, 0x00, 0x21, 0x7E, 0x03, key_index, 0x00, 30, 0x00, 0xF7]
    midi_out.send_message(sys_ex_data)

# Replace 'Exquis 2' with the actual name of your MIDI output port
desired_device_name = 'Exquis 2'

# Open the desired output port
try:
    midi_out = rtmidi.MidiOut()
    available_ports = midi_out.get_ports()

    if desired_device_name not in available_ports:
        raise ValueError(f"MIDI output port '{desired_device_name}' not found.")

    midi_out.open_port(available_ports.index(desired_device_name))
    print(f"Successfully opened MIDI output port: {desired_device_name}")

    # Blank all LEDs
    for key_index in range(61):
        send_blank_message(midi_out, key_index)
        

finally:
    if midi_out.is_port_open():
        midi_out.close_port()
        print("MIDI output port closed")

