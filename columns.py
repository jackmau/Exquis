import random
import rtmidi
import time

# Replace 'Exquis 2' with the actual name of your MIDI output port
desired_device_name = 'Exquis 2'

# Define the columns with start and step indices
columns = [
    {'start': 0, 'step': 11},   # Column 1
    {'start': 6, 'step': 11},   # Column 2
    {'start': 1, 'step': 11},   # Column 3
    {'start': 7, 'step': 11},   # Column 4
    {'start': 2, 'step': 11},   # Column 5
    {'start': 8, 'step': 11},   # Column 6
    {'start': 3, 'step': 11},   # Column 7
    {'start': 9, 'step': 11},   # Column 8
    {'start': 4, 'step': 11},   # Column 9
    {'start': 10, 'step': 11},  # Column 10
    {'start': 5, 'step': 11},   # Column 11
]

# Number of color cycles
num_color_cycles = 10

# Function to send RGB messages
def send_rgb_message(midi_out, key_index, red, green, blue):
    sys_ex_data = [0xF0, 0x00, 0x21, 0x7E, 0x03, key_index, red, green, blue, 0xF7]
    midi_out.send_message(sys_ex_data)

try:
    # Open the MIDI output port
    midi_out = rtmidi.MidiOut()
    available_ports = midi_out.get_ports()

    if desired_device_name not in available_ports:
        raise ValueError(f"MIDI output port '{desired_device_name}' not found.")

    midi_out.open_port(available_ports.index(desired_device_name))
    print(f"Successfully opened MIDI output port: {desired_device_name}")

    # Iterate through color cycles
    for color_cycle in range(num_color_cycles):
        # Iterate through each column
        for column_index, column in enumerate(columns):
            # Random RGB color values for the current column
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)

            # Illuminate the current column with the same color
            key_index = column['start']
            for _ in range(6):
                send_rgb_message(midi_out, key_index, red, green, blue)
                key_index += column['step']

            # Pause briefly after illuminating the column
            time.sleep(0.5)

            # Blank the current column
            key_index = column['start']
            for _ in range(6):
                send_rgb_message(midi_out, key_index, 0, 0, 0)
                key_index += column['step']

finally:
    # Close the MIDI output port
    if midi_out.is_port_open():
        midi_out.close_port()
        print("MIDI output port closed")
