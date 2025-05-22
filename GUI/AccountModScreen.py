import tkinter as tk
from tkinter import messagebox
from CredentialController import CredentialController

# Define main menu callbacks for each user type.

def open_admin_main_screen(parent):
    print("Opening Admin Main Screen...")  
    parent.deiconify()

def open_customer_main_screen(parent):
    print("Opening Customer Main Sreen...")
    parent.deiconify()

def open_donor_main_screen(parent):
    print("Opening Donor Main Screen...")
    parent.deiconify()

def open_drop_off_agent_main_screen(parent):
    print("Opening Drop-Off Agent Main Screen...")
    parent.deiconify()

# Function to determine the correct main menu callback given the parent window.
def get_main_screen_callback(user_role, parent):
    callbacks = {
        "admin": open_admin_main_screen,
        "customer": open_customer_main_screen,
        "donor": open_donor_main_screen,
        "drop_off_agent": open_drop_off_agent_main_screen
    }
    # Return a lambda that calls the corresponding function with the parent window.
    return lambda: callbacks[user_role](parent)

class AccountModScreen:
    def __init__(self, parent, user_role):
        
        self.controller = CredentialController()
        self.parent = parent
        
        self.main_screen_callback = get_main_screen_callback(user_role, parent)
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("Modify Account")
        self.window.geometry("400x500")

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

        # GUI Layout for Account Modification Screen
        tk.Label(self.window, text="Update Account Info", font=("Helvetica", 16)).pack(pady=10)

        self.name_entry = self._add_labeled_entry("Name")
        self.surname_entry = self._add_labeled_entry("Surname")
        self.nickname_entry = self._add_labeled_entry("Nickname")
        self.email_entry = self._add_labeled_entry("Email")
        self.password_entry = self._add_labeled_entry("Password", show="*")
        self.phone_entry = self._add_labeled_entry("Phone")
        self.address_entry = self._add_labeled_entry("Address")

        tk.Button(self.window, text="Submit Changes", command=submit_changes).pack(pady=20)

        # "Main Menu" button to return to the main screen.
        tk.Button(self.window, text="Main Screen", command=self.go_to_main_screen,
                  bg="#FFA500", fg="white").pack(pady=10)

    def _add_labeled_entry(self, label, show=None):
        tk.Label(self.window, text=label).pack()
        entry = tk.Entry(self.window, show=show) if show else tk.Entry(self.window)
        entry.pack()
        return entry

    def go_to_main_screen(self):
        self.window.destroy()  # Close the account modification window.
        self.main_screen_callback()  # Re-display the main screen 