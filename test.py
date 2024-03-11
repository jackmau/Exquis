import tkinter as tk
from tkinter import ttk
import time
import rtmidi
from PIL import Image, ImageTk
import threading

desired_device_name = 'Exquis 0'

cs1 = [[150,113,23],
       [31,206,203],
       [255,0,127],
       [115,194,251],
       [197,75,140],
       [226,88,34],
       [135,206,235],
       [255,36,0],
       [173,216,230],
       [207,16,32],
       [0,255,239],
       [242,133,0]]
cs2 = [[255,253,208],
       [30,144,255],
       [237,201,175],
       [16,52,166],
       [194,178,128],
       [229,170,112],
       [17,100,180],
       [255,215,0],
       [93,138,168],
       [251,206,177],
       [0,112,255],
       [227,218,201]]

rr = 79/255

def HarmonicTable(st_note, jump, cols_lens, row_len, int_y, int_xz,cs1,cs2):
    col, notes = zip(*[(z,st_note + jump*z + x * int_y[z] + q + int_xz[y]) for q in range(row_len) for y in range(2) for z in range(2) for x in range(cols_lens[y][z])][:-sum(cols_lens[1])])
    return [notes, [list(zip(cs1,cs2))[notes[x] % 12][col[x]] for x in range(len(notes))]]

def HarmonicTableHorizontal(st_note, jump, cols_lens, row_len, int_y, int_z, cs1, cs2):
    note1, col1 = HarmonicTable(st_note,0, [[cols_lens[0],0],[cols_lens[1],0]], row_len, [int_y[0],0], [0,int_z[0]],cs1,cs2)
    note1 = note1 + (0,)*5
    col1 = col1 + [[0]*3]*5
    note2, col2 = HarmonicTable(st_note+jump,0, [[0,cols_lens[0]],[0,cols_lens[1]]], row_len, [0,int_y[1]], [0,int_z[1]],cs1,cs2)
    return [note1+note2,col1+col2]

class MidiSender:
    def __init__(self, midi_out, interval):
        self.midi_out = midi_out
        self.interval = interval
        self.is_running = False

    def start_sending_midi(self):
        self.is_running = True
        while self.is_running:
            self.midi_out.send_message([0xF0, 0x00, 0x21, 0x7E, 0xF7])
            time.sleep(self.interval / 1000.0)

    def stop_sending_midi(self):
        self.is_running = False
        


class MidiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI Sender")


        self.images = [
            {"path": "img/1.PNG", "name": "Horizontal"},
            {"path": "img/2.PNG", "name": "Vertical"},
            {"path": "path_to_image3.jpg", "name": "Image 3"}
        ]

        self.selected_image_index = tk.StringVar()
        self.selected_image_index.set("0")
        self.midi_sender = None  # To store the MidiSender instance
        self.midi_thread = None  # To store the reference to the MIDI thread
        self.create_gui()

    def create_gui(self):
        # Image display
        self.image_label = ttk.Label(self.root, text="Choose an image:")
        self.image_label.pack()

        self.image_combo = ttk.Combobox(self.root, values=[img["name"] for img in self.images], textvariable=self.selected_image_index)
        self.image_combo.pack()
        self.image_combo.bind("<<ComboboxSelected>>", self.show_selected_image)

        self.canvas = tk.Canvas(self.root, width=1200, height=700)
        self.canvas.pack()
        

        # MIDI buttons
        self.start_button = ttk.Button(self.root, text="Start MIDI", command=self.start_midi)
        self.start_button.pack()

        self.stop_button = ttk.Button(self.root, text="Stop MIDI", command=self.stop_midi)
        self.stop_button.pack()

    def show_selected_image(self, event):
        selected_image_path = self.images[self.image_combo.current()]["path"]
        image = Image.open(selected_image_path)
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo  # Keep a reference to avoid garbage collectio

    def start_midi(self):

        midi_out = rtmidi.MidiOut()
        available_ports = midi_out.get_ports()

        if desired_device_name not in available_ports:
            raise ValueError(f"MIDI output port '{desired_device_name}' not found.")

        midi_out.open_port(available_ports.index(desired_device_name))
        print(f"Successfully opened MIDI output port: {desired_device_name}")
        self.midi_sender = MidiSender(midi_out, interval=400)
        self.midi_thread = threading.Thread(target=self.midi_sender.start_sending_midi)
        self.midi_thread.start()
        time.sleep(0.8)
        selected_image_index = self.image_combo.current()
        if selected_image_index == 0:
            notes, colours = HarmonicTable(24,12*4+2, [[3,3],[2,3]], 6, [11,-11], [0,6], cs1,cs2)
        else:
            notes, colours = HarmonicTableHorizontal(29,12*4+5, [6,5],3,[5,-5],[3,-2],cs1,cs2)
        for k in range(61):
            color_sysex = [0xF0, 0x00, 0x21, 0x7E, 0x03, k, round(colours[k][0]*rr),
                           round(colours[k][1]*rr), round(colours[k][2]*rr), 0xF7]
            note_sysex = [0xF0, 0x00, 0x21, 0x7E, 0x04, k, notes[k], 0xF7]
            midi_out.send_message(color_sysex)
            midi_out.send_message(note_sysex)

    def stop_midi(self):
        if self.midi_sender and self.midi_sender.is_running:
            # Signal the MidiSender instance to stop
            self.midi_sender.stop_sending_midi()
            self.midi_thread.join()
            self.midi_thread = None

    


if __name__ == "__main__":
    root = tk.Tk()
    app = MidiApp(root)
    root.mainloop()

