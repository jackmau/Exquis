import tkinter as tk
from tkinter import ttk, font
import time
import rtmidi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading

note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

axis_cs = [[142,244,251],	
	   [ 64, 64, 64],
	   [200,200,200],
	   [ 64, 64, 64],
	   [200,200,200],
	   [200,200,200],
 	   [ 16, 32,128],
	   [200,200,200],
	   [ 64, 64, 64],
	   [200,200,200],
	   [ 64, 64, 64],
	   [200,200,200]]

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

# Layout function defintions

def layout_vertical(st_note, split_structure, x_step, y_step, z_step, jump = 0, excl = [-1,-1,-1]):
    return [(st_note + jump*z + x*y_step[z] + q*x_step[z] + y*z_step[z]) if not(x == excl[0] and y ==excl[1] and z ==excl[2]) else 0 for q in range(6) for y in range(2) for z in range(2) for x in range(split_structure[z][y])][:-sum(split_structure[x][1] for x in range(2))]

def layout_horizontal(st_note, x_step, y_step, z_step, jump = 0 , split = -1):
    s = (split-1)/2-1
    return [st_note + jump*(q>s) + q*x_step[(q>s)] + x*y_step[(q>s)] + z*z_step[(q>s)] for q in range(6) for z in range(2) for x in range([6,5][z])][:-5]

def note_colours(notes, cs, adj = True):
    if adj:
        cs = [[round(cs[y][x] *79/255) for x in range(3)] for y in range(len(cs1))]
    return [[cs[x % 12][y] if x > 0 else 0 for x in notes] for y in range(3)]

def note_number_to_name(note_number):
    """Convert MIDI note number to note name with sharps and flats."""
    if note_number == 0:
        return f""
    else:
        octave = (note_number - 60) // 12
        note_name = note_names[note_number % 12]
    return f"{note_name}{octave + 4}"

def hexagon(ax, center, size, color, label, fontsize):
    """Draw a hexagon on the given axes."""
    angle = np.linspace(0, 2*np.pi, 7)
    x = center[0] + size * np.cos(angle)
    y = center[1] + size * np.sin(angle)
    ax.fill(x, y, color=color, edgecolor='k')
    if sum(color) > 1:
        tx_color = 'black'
    else:
        tx_color = 'white'
    ax.text(center[0], center[1], label, ha='center', va='center', color=tx_color, fontsize=fontsize)

def create_hexagonal_keyboard(ax, notes, r, g, b):
    """Create an image of a hexagonal keyboard."""

    column_width = 2 * np.cos(np.pi / 12)  # Width of a hexagon column
    row_height = 1  # Height of a hexagon row
    size = 0.6  # Size of hexagons
    fontsize = 14  # Font size of note labels

    for col in range(11):
        if col % 2 == 0:
            for row in range(6):
                index = (col+1) * 5 - row + round(col/2)
                center = ((col-1) * column_width/2, row * row_height)
                hexagon(ax, center, size=size, color=(r[index]/80, g[index]/80, b[index]/80), label=notes[index], fontsize=fontsize)
        else:
            for row in range(5):
                index = (col+1) * 5 - row + round((col-1)/2)
                center = ((col-1)  * column_width/2, row * row_height + row_height / 2)
                hexagon(ax, center, size=size, color=(r[index]/80, g[index]/80, b[index]/80), label=notes[index], fontsize=fontsize)

    ax.set_aspect('equal')
    ax.axis('off')

# Classes definiton, thanks to chatGPT!

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
        self.root.title("Exquis Template Editor")

        self.images = ["Vertical Split 6-4",
                       "Diagonal Vertical Split",
                       "Horizontal Split Asymmetric"]

        self.selected_image_index = tk.StringVar()
        self.selected_midi_device = tk.StringVar()
        self.midi_sender = None  # To store the MidiSender instance
        self.midi_thread = None  # To store the reference to the MIDI thread
        self.midi_out = rtmidi.MidiOut()
        self.midi_devices = self.midi_out.get_ports()
        self.split_combos = []
        self.create_gui()

    def create_gui(self):

        self.fig, self.ax = plt.subplots(figsize=(11, 6))
        self.ax.axis('off')
        # Select MIDI Device
        self.midi_device_label = ttk.Label(self.root, text="Select MIDI Device:")
        self.midi_device_label.pack()

        self.midi_device_combo = ttk.Combobox(self.root, values=self.midi_devices, textvariable=self.selected_midi_device)
        self.midi_device_combo.pack()
        self.midi_device_combo.bind("<<ComboboxSelected>>", self.open_midi)

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Create frames for each option
        self.frame1 = ttk.Frame(self.notebook)
        self.frame2 = ttk.Frame(self.notebook)

        # Add frames to the notebook
        self.notebook.add(self.frame1, text="Main Layer")
        self.notebook.add(self.frame2, text="Split Layer")

        # Main parameters
        self.start_note, self.start_octave = tk.IntVar(), tk.IntVar()
        self.x_step1, self.y_step1, self.z_step1 = tk.IntVar(),tk.IntVar(),tk.IntVar()
        ## Start Note
        ttk.Label(self.frame1, text="Start Note:").pack()
        self.start_note_combo = ttk.Combobox(self.frame1, textvariable=self.start_note, values=note_names)
        self.start_note_combo.current(0)
        self.start_note_combo.pack()
        ## Start Octave
        ttk.Label(self.frame1, text="Start Octave:").pack()
        ttk.Spinbox(self.frame1, textvariable=self.start_octave, values=list(range(9))).pack()
        ## X Step
        ttk.Label(self.frame1, text="X semitone intervals:").pack()
        ttk.Spinbox(self.frame1, textvariable=self.x_step1, values=list(range(-11,12))).pack()
        ## Y Step
        ttk.Label(self.frame1, text="Y semitone intervals:").pack()
        ttk.Spinbox(self.frame1, textvariable=self.y_step1, values=list(range(-11,12))).pack()
        ## Z Step
        ttk.Label(self.frame1, text="Z semitone intervals:").pack()
        ttk.Spinbox(self.frame1, textvariable=self.z_step1, values=list(range(-5,6))).pack()
         
        # Split parameters
        split_values = ["No Split","Horizontal","Vertical"]
        self.split = tk.StringVar()
        self.split_start_note, self.split_start_octave = tk.IntVar(), tk.IntVar()
        self.x_step2, self.y_step2, self.z_step2 = tk.IntVar(),tk.IntVar(),tk.IntVar()
        self.split_column = tk.IntVar(value=13)
        ## Split Type
        ttk.Label(self.frame1, text="Start Note:").pack()
        self.split_combo = ttk.Combobox(self.frame2, textvariable=self.split, values=split_values)
        self.split_combo.current(0)
        self.split_combo.pack()
        ## Split Start Note
        ttk.Label(self.frame2, text="Start Note:").pack()
        self.split_start_note_combo = ttk.Combobox(self.frame2, textvariable=self.split_start_note, values=note_names)
        self.split_start_note_combo.current(0)
        self.split_start_note_combo.pack()
        ## Split Start Octave
        ttk.Label(self.frame2, text="Start Octave:").pack()
        ttk.Spinbox(self.frame2, textvariable=self.split_start_octave, values=list(range(9))).pack()
        ## Split X Step
        ttk.Label(self.frame2, text="X semitone intervals:").pack()
        ttk.Spinbox(self.frame2, textvariable=self.x_step2, values=list(range(-11,12))).pack()
        ## Split Y Step
        ttk.Label(self.frame2, text="Y semitone intervals:").pack()
        ttk.Spinbox(self.frame2, textvariable=self.y_step2, values=list(range(-11,12))).pack()
        ## Split Z Step
        ttk.Label(self.frame2, text="Z semitone intervals:").pack()
        ttk.Spinbox(self.frame2, textvariable=self.z_step2, values=list(range(-5,6))).pack()
        ## Add remaining frames according to the type of split
        self.split_combo.bind("<<ComboboxSelected>>", self.add_split_boxes)

        # Button to execute selected option
        self.gen_button = ttk.Button(self.root, text="Generate\nTemplate", command=self.generate_image)
        self.gen_button.pack()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        # MIDI buttons
        self.start_button = ttk.Button(self.root, text="Send Template", command=self.start_midi)
        self.start_button.pack()

        self.stop_button = ttk.Button(self.root, text="Close Connection", command=self.stop_midi)
        self.stop_button.pack()

    def generate_image(self):
        self.ax.clear()
        start_note = self.start_note_combo.current() + 12 * (self.start_octave.get()+1)
        jump = self.split_start_note_combo.current() + 12 * (self.split_start_octave.get()+1) - start_note
        x = [self.x_step1.get(), self.x_step2.get()]
        y = [self.y_step1.get(), self.y_step2.get()]
        z = [self.z_step1.get(), self.z_step2.get()]
        if self.split.get() == "Vertical":
            self.notes = layout_vertical(36, [[3,2],[3,3]], [1,1], [9,-9], [5,5], 3*12+3)
        #elif self.image_combo.current() == 1:
        #    self.notes = layout_vertical(30, [[3,3],[3,2]], [5,5], [3,-3], [4,1], 2*12+8, [2,1,0])
        else:
            #self.notes = layout_horizontal(34, [2,1], [4,-7], [3,-3], 5*12-4, 5)
            self.notes = layout_horizontal(start_note, x, y, z, jump, self.split_column.get())
        self.colours = note_colours(self.notes, axis_cs)
        r,g,b = self.colours
        notes = [note_number_to_name(n) for n in self.notes]
        create_hexagonal_keyboard(self.ax, notes, r, g, b)
        self.canvas.draw_idle()

    def open_midi(self, event):
        try:
            self.midi_out.open_port(self.selected_midi_device.get())
            messagebox.showinfo("MIDI connection", f"Successfully opened MIDI output port: {self.selected_midi_device}")
        except:
            messagebox.showerror("MIDI COnnection Error", f"Failed to connect to {self.selected_midi_device}")

    def start_midi(self):
        self.midi_sender = MidiSender(midi_out, interval=400)
        self.midi_thread = threading.Thread(target=self.midi_sender.start_sending_midi)
        self.midi_thread.start()
        time.sleep(0.8)
        r,g,b = self.colours
        notes = self.notes
        for k in range(61):
            color_sysex = [0xF0, 0x00, 0x21, 0x7E, 0x03, k, r[k], g[k], b[k], 0xF7]
            note_sysex = [0xF0, 0x00, 0x21, 0x7E, 0x04, k, notes[k], 0xF7]
            midi_out.send_message(color_sysex)
            midi_out.send_message(note_sysex)

    def stop_midi(self):
        if self.midi_sender and self.midi_sender.is_running:
            # Signal the MidiSender instance to stop
            self.midi_sender.stop_sending_midi()
            self.midi_thread.join()
            self.midi_thread = None
            
    def add_split_boxes(self, event):
        [x.destroy() for x in self.split_combos]
        self.split_combos = []
        if self.split.get() == "Horizontal":
            self.split_combos.append(ttk.Label(self.frame2, text="Column Split:"))
            self.split_combos.append(ttk.Combobox(self.frame2, textvariable=self.split_column, values=list(range(3,8))))
            [x.pack() for x in self.split_combos]
        if self.split.get() == "Vertical":    
            pass

if __name__ == "__main__":
    root = tk.Tk()
    # Define a new font with a custom size
    custom_font = ('TkDefaultFont', 14)   # Change the size to your desired value
    style = ttk.Style()
    style.configure('.', font=custom_font)
    # Set the custom font as the default font for all widgets
    root.option_add("*Font", custom_font)
    app = MidiApp(root)
    root.mainloop()

