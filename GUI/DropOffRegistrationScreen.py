import tkinter as tk
from tkinter import font as tkFont
from DropOffRegistrationController import DropOffRegistrationController

class DropOffRegistrationScreen:
    def __init__(self, root):
        self.root = root
        self.controller = DropOffRegistrationController(root)

    def show_registration_form(self):
        # Clear current screen
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="📦 Drop-Off Agent Registration", fg="#003366", bg="#9AFF9A")
        title.config(font=tkFont.Font(size=18, weight="bold"))
        title.pack(pady=20)

        # Entry fields
        self.entries = {}
        fields = ["Name", "Surname", "Username", "Email", "Password", "Phone"]
        for field in fields:
            label = tk.Label(self.root, text=f"{field}:" , bg="#9AFF9A")
            label.pack()
            entry = tk.Entry(self.root, show="*" if field == "Password" else None, width=30)
            entry.pack(pady=5)
            self.entries[field.lower()] = entry

        # Submit Button
        submit_btn = tk.Button(self.root, text="Create Account", bg="#004d99", fg="white", 
                               command=self.submit_form)
        submit_btn.pack(pady=15)

        # Back Button
        back_btn = tk.Button(self.root, text="Back", command=self.back_to_main_screen,)
        back_btn.pack()

    # Method to handle form submission
    def submit_form(self):
        # Collect data from entry fields
        name = self.entries["name"].get()
        surname = self.entries["surname"].get()
        username = self.entries["username"].get()
        email = self.entries["email"].get()
        password = self.entries["password"].get()
        phone = self.entries["phone"].get()
        
        # Clear the entry fields after submission
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        # Submit the form through controller
        self.controller.submit_form(name, surname, username, email, password, phone)

    # Method to navigate back to the main screen
    def back_to_main_screen(self):
        from GUI.MainScreenAdmin import MainScreenAdmin
        # Clear current screen
        for widget in self.root.winfo_children():
            widget.destroy()

       # Back to main screen
        MainScreenAdmin(self.root)
