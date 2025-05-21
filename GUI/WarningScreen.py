import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox

# Popup window for warning messages
class WarningScreen:
    def __init__(self, master, message):
        self.top = tk.Toplevel(master)
        self.message = message
        self.top.title("Warning")

    def show_warning(self):
        # Set the size of the popup window
        warning_label = tk.Label(self.top, text=self.message, wraplength=300)
        warning_label.config(font=tkFont.Font(size=12), fg="red")
        warning_label.pack(pady=20)

        ok_button = tk.Button(self.top, text="OK", command=self.close_warning)
        ok_button.config(font=tkFont.Font(size=12), bg="#4CAF50", fg="white")
        ok_button.pack(pady=10)