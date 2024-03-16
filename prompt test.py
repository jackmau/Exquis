import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def option1():
    print("Option 1 selected")
    print("Parameter 1:", param1_var.get())
    print("Parameter 2:", param2_var.get())
    create_result_window()

def option2():
    print("Option 2 selected")
    print("Parameter 1:", param1_var.get())
    print("Parameter 3:", param3_var.get())
    create_result_window()

def option3():
    print("Option 3 selected")
    print("Parameter 1:", param1_var.get())
    create_result_window()

def create_result_window():
    result_window = tk.Toplevel(root)
    result_window.title("Execution Result")

    # Matplotlib widget
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Additional widgets can be added to the result window

# Create a Tkinter window
root = tk.Tk()
root.title("Options")

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create frames for each option
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)

# Add frames to the notebook
notebook.add(frame1, text="Option 1")
notebook.add(frame2, text="Option 2")
notebook.add(frame3, text="Option 3")

# Option 1 parameters
param1_var = tk.StringVar()
param2_var = tk.StringVar()
ttk.Label(frame1, text="Parameter 1:").pack()
ttk.Combobox(frame1, textvariable=param1_var, values=["Option A", "Option B"]).pack()
ttk.Label(frame1, text="Parameter 2:").pack()
ttk.Combobox(frame1, textvariable=param2_var, values=["Option X", "Option Y"]).pack()

# Option 2 parameters
param1_var = tk.StringVar()
param3_var = tk.StringVar()
ttk.Label(frame2, text="Parameter 1:").pack()
ttk.Combobox(frame2, textvariable=param1_var, values=["Option A", "Option B"]).pack()
ttk.Label(frame2, text="Parameter 3:").pack()
ttk.Combobox(frame2, textvariable=param3_var, values=["Option M", "Option N"]).pack()

# Option 3 parameters
param1_var = tk.StringVar()
ttk.Label(frame3, text="Parameter 1:").pack()
ttk.Combobox(frame3, textvariable=param1_var, values=["Option A", "Option B"]).pack()

# Button to execute selected option
execute_button = ttk.Button(root, text="Execute", command=lambda: notebook.tab(notebook.select(), "text")())
execute_button.pack()

# Run the Tkinter event loop
root.mainloop()
