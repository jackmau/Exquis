import random
import rtmidi
import time

# Replace 'Exquis 2' with the actual name of your MIDI output port
desired_device_name = 'Exquis 2'

# Define the rows with start and end indices
rows = [
    {'start': 60, 'end': 55},  # Row 1
    {'start': 54, 'end': 50},  # Row 2
    {'start': 49, 'end': 44},  # Row 3
    {'start': 43, 'end': 39},  # Row 4
    {'start': 38, 'end': 33},  # Row 5
    {'start': 32, 'end': 28},  # Row 6
    {'start': 27, 'end': 22},  # Row 7
    {'start': 21, 'end': 17},  # Row 8
    {'start': 16, 'end': 11},  # Row 9
    {'start': 10, 'end': 6},   # Row 10
    {'start': 5, 'end': 0},    # Row 11
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
        # Iterate through each row
        for row_index, row in enumerate(rows):
            # Random RGB color values for the current row
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)

            # Illuminate the current row with the same color
            for key_index in range(row['start'], row['end'] - 1, -1):
                send_rgb_message(midi_out, key_index, red, green, blue)

            # Pause briefly after illuminating the row
            start_time = time.perf_counter()
            while time.perf_counter() - start_time < 0.2:
                pass

            # Blank the current row
            for key_index in range(row['start'], row['end'] - 1, -1):
                send_rgb_message(midi_out, key_index, 0, 0, 0)

finally:
    # Close the MIDI output port
    if midi_out.is_port_open():
        midi_out.close_port()
        print("MIDI output port closed")
