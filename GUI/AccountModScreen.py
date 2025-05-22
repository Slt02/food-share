import tkinter as tk
from tkinter import messagebox
from CredentialController import CredentialController


class AccountModScreen:
    def __init__(self):
        self.controller = CredentialController()

    def displayAccountModScreen(self, user_id):
        self.user_id = user_id

        def submit_changes():
            updates = {
                "name": self.name_entry.get().strip(),
                "surname": self.surname_entry.get().strip(),
                "nickname": self.nickname_entry.get().strip(),
                "email": self.email_entry.get().strip(),
                "password": self.password_entry.get().strip(),
                "phone": self.phone_entry.get().strip(),
                "address": self.address_entry.get().strip()
            }

            # Send updates to controller
            success, message = self.controller.update(self.user_id, updates)

            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

        # GUI Layout
        self.window = tk.Tk()
        self.window.title("Modify Account")
        self.window.geometry("400x450")

        tk.Label(self.window, text="Update Account Info", font=("Helvetica", 16)).pack(pady=10)

        self.name_entry = self._add_labeled_entry("Name")
        self.surname_entry = self._add_labeled_entry("Surname")
        self.nickname_entry = self._add_labeled_entry("Nickname")
        self.email_entry = self._add_labeled_entry("Email")
        self.password_entry = self._add_labeled_entry("Password", show="*")
        self.phone_entry = self._add_labeled_entry("Phone")
        self.address_entry = self._add_labeled_entry("Address")

        tk.Button(self.window, text="Submit Changes", command=submit_changes).pack(pady=20)

        self.window.mainloop()

    def _add_labeled_entry(self, label, show=None):
        tk.Label(self.window, text=label).pack()
        entry = tk.Entry(self.window, show=show) if show else tk.Entry(self.window)
        entry.pack()
        return entry