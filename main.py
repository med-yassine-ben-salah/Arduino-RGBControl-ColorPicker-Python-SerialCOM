import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
import serial.tools.list_ports


def pick_color(ser):
    color = colorchooser.askcolor(color=selected_color.get())
    if color[1]:
        rgb = color[0]
        hex_code = color[1]

        # Convert RGB values to a string and send it via serial
        rgb_string = ','.join(str(int(value)) for value in rgb)
        ser.write(rgb_string.encode())

        color_label.config(text="Selected color: RGB = {}, Hex = {}".format(rgb, hex_code))
        color_label.config(background=hex_code)
        selected_color.set(hex_code)
        status_msg_label.config(text="Color sent to microcontroller", foreground="#4CAF50")


def scan_ports():
    ports = serial.tools.list_ports.comports()
    com_ports = [port.device for port in ports]
    port_combobox['values'] = com_ports


root = tk.Tk()
root.title("RGB Color Picker")
root.geometry("480x560")
root.configure(background="#fff")  # Set background color to white

# Use a modern theme for ttk widgets
style = ttk.Style()
style.theme_use('clam')

# Style the GUI elements with ttk
style.configure("TButton", padding=10, relief="flat", background="#2196F3", foreground="#fff", font=("Arial", 12))
style.map("TButton",
          background=[('active', '#0D47A1'), ('disabled', '#BDBDBD')])
style.configure("TLabel", padding=10, background="#fff", font=("Arial", 12))
style.configure("TCombobox", font=("Arial", 12), background="#fff", foreground="#000")
style.map("TCombobox", fieldbackground=[('readonly', '#fff')])

# Add labels and tooltips to the GUI elements
color_label = ttk.Label(root, text="Selected color: ", font=("Arial", 14))
color_label.pack(pady=20)
color_label_tooltip = ttk.Label(root, text="Click the 'Pick a Color' button to choose a color", font=("Arial", 12))
color_label_tooltip.pack()

# Keep track of the selected color
selected_color = tk.StringVar()

ser = None  # Declare the ser variable


def open_port():
    global ser
    port = port_combobox.get()
    baudrate = baudrate_combobox.get()

    if port and baudrate:
        try:
            ser = serial.Serial(port, int(baudrate))
            port_status_label.config(text="Port Status: Connected", foreground="#4CAF50")
            status_msg_label.config(text="Serial port {} opened with baud rate {}".format(port, baudrate), foreground="#000")
            print("Serial port {} opened with baud rate {}".format(port, baudrate))
        except serial.SerialException:
            port_status_label.config(text="Port Status: Not Connected", foreground="#F44336")
            status_msg_label.config(text="Error: Could not open serial port", foreground="#F44336")
    else:
        port_status_label.config(text="Port Status: Not Connected", foreground="#F44336")
        status_msg_label.config(text="Please select a valid COM port and baud rate", foreground="#F44336")
        print("Please select a valid COM port and baud rate")


pick_color_button = ttk.Button(root, text="Pick a Color", command=lambda: pick_color(ser))
pick_color_button.pack(pady=20)

# Add COM port selection
port_label = ttk.Label(root, text="Select COM Port:")
port_label.pack()
port_combobox = ttk.Combobox(root, values=[], width=10)
port_combobox.pack()
scan_button = ttk.Button(root, text="Scan Ports", command=scan_ports)
scan_button.pack()

# Automatically scan ports at program launch
scan_ports()

# Add baud rate selection
baudrate_label = ttk.Label(root, text="Select Baud Rate:")
baudrate_label.pack()
baudrate_combobox = ttk.Combobox(root, values=["300", "1200", "2400", "4800", "9600", "14400", "19200",
                                                "38400", "57600", "115200"], width=10)
baudrate_combobox.pack()
baudrate_combobox.set("9600")  # Set default baud rate to 9600

open_port_button = ttk.Button(root, text="Open Port", command=open_port)
open_port_button.pack(pady=20)

# Add port status label
port_status_label = ttk.Label(root, text="Port Status: Not Connected", font=("Arial", 14))
port_status_label.pack()

# Add status message label
status_msg_label = ttk.Label(root, text="", font=("Arial", 12))
status_msg_label.pack()

root.mainloop()