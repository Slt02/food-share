import tkinter as tk
from tkinter import messagebox
from datetime import datetime

import re

class Database:
    def __init__(self):
        try:
            from merkdb import Database as MerkDB
            self.merkdb = MerkDB()
            self.connection = self.merkdb.connection
        except ImportError:
            self.connection = None
    
    def execute_query(self, query, params=None):
        if hasattr(self, 'merkdb'):
            return self.merkdb.execute_query(query, params)
        return [("John", "Doe", "johndoe", "john@example.com", "password123", "1234567890", "123 Main St")]

class CredentialController:
    def __init__(self):
        self.diondb = Database()

    def validate_email(self, email):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(email_regex, email) is not None

    def validate_password_strength(self, password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters."
        if not re.search(r'[A-Z]', password):
            return False, "Password must include at least one uppercase letter."
        if not re.search(r'[0-9]', password):
            return False, "Password must include at least one number."
        if not re.search(r'[\W_]', password):
            return False, "Password must include at least one symbol."
        return True, "Password is strong."

    def validate_phone(self, phone):
        if not phone.strip():
            return True
        digits_only = re.sub(r'\D', '', phone)
        return len(digits_only) == 10

    def update(self, user_id, updated_info):
        try:
            filtered_updates = {k: v for k, v in updated_info.items() if v.strip()}
            if not filtered_updates:
                return False, "No updates provided."
            return True, "User info updated successfully."
        except Exception as e:
            return False, f"Database error: {str(e)}"

def get_main_screen_callback(user_role, parent):
    return lambda: parent.deiconify()

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

            success, message = self.controller.update(self.user_id, updates)

            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

        tk.Label(self.window, text="Update Account Info", font=("Helvetica", 16)).pack(pady=10)

        self.name_entry = self._add_labeled_entry("Name")
        self.surname_entry = self._add_labeled_entry("Surname")
        self.nickname_entry = self._add_labeled_entry("Nickname")
        self.email_entry = self._add_labeled_entry("Email")
        self.password_entry = self._add_labeled_entry("Password", show="*")
        self.phone_entry = self._add_labeled_entry("Phone")
        self.address_entry = self._add_labeled_entry("Address")

        tk.Button(self.window, text="Submit Changes", command=submit_changes).pack(pady=20)
        tk.Button(self.window, text="Main Screen", command=self.go_to_main_screen,
                  bg="#FFA500", fg="white").pack(pady=10)

    def _add_labeled_entry(self, label, show=None):
        tk.Label(self.window, text=label).pack()
        entry = tk.Entry(self.window, show=show) if show else tk.Entry(self.window)
        entry.pack()
        return entry

    def go_to_main_screen(self):
        self.window.destroy()
        self.main_screen_callback()

class MockDonationController:
    def create_donation(self, donor_id, item_name, quantity, donation_date):
        print(f"Creating donation: {item_name} x{quantity}")
        return True

class RegistrationFormScreen:
    def __init__(self, parent, donation_controller):
        self.parent = parent
        self.donation_controller = donation_controller
        self.window = None
        self.donation_data = {}

    def display(self):
        print("📋 Opening Registration Form Screen...")
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("Register Donation")
        self.window.geometry("450x400")
        self.window.configure(bg="#f0f0f0")
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        tk.Label(self.window, text="Register Your Donation", 
                font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=30)
        
        self._create_form_fields()
        self._create_buttons()

    def _create_form_fields(self):
        fields_frame = tk.Frame(self.window, bg="#f0f0f0")
        fields_frame.pack(pady=20, padx=40, fill="both")
        
        tk.Label(fields_frame, text="What are you donating?", 
                font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(anchor="w", pady=(10,5))
        tk.Label(fields_frame, text="Item Name:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", pady=(5,5))
        self.item_name_entry = tk.Entry(fields_frame, font=("Arial", 12), width=30, relief="solid", bd=1)
        self.item_name_entry.pack(fill="x", pady=(0,20))
        self.item_name_entry.focus()
        
        tk.Label(fields_frame, text="How much are you donating?", 
                font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(anchor="w", pady=(10,5))
        tk.Label(fields_frame, text="Quantity:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", pady=(5,5))
        self.quantity_entry = tk.Entry(fields_frame, font=("Arial", 12), width=30, relief="solid", bd=1)
        self.quantity_entry.pack(fill="x", pady=(0,10))
        
        tk.Label(fields_frame, text="Examples: 10 cans, 5 boxes, 20 items, etc.", 
                font=("Arial", 9, "italic"), bg="#f0f0f0", fg="#666").pack(anchor="w", pady=(5,0))

    def _create_buttons(self):
        button_frame = tk.Frame(self.window, bg="#f0f0f0")
        button_frame.pack(pady=30)
        
        tk.Button(button_frame, text="Submit Donation", command=self.submit_donation, 
                 bg="#4CAF50", fg="white", width=18, height=2,
                 font=("Arial", 11, "bold")).pack(side="left", padx=15)
        
        tk.Button(button_frame, text="Cancel", command=self.cancel, 
                 bg="#f44336", fg="white", width=15, height=2,
                 font=("Arial", 11, "bold")).pack(side="right", padx=15)

    def submit_donation(self):
        try:
            item_name = self.item_name_entry.get().strip()
            quantity = self.quantity_entry.get().strip()
            
            if not item_name:
                messagebox.showerror("Missing Information", "Please enter what you are donating")
                self.item_name_entry.focus()
                return
            
            if not quantity or not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showerror("Invalid Input", "Please enter a valid quantity (positive number)")
                self.quantity_entry.focus()
                return
            
            confirm_msg = f"You are donating:\n\n• Item: {item_name}\n• Quantity: {quantity}\n\nSubmit this donation?"
            
            if messagebox.askyesno("Confirm Donation", confirm_msg):
                success = self.donation_controller.create_donation(1, item_name, int(quantity), datetime.now())
                
                if success:
                    messagebox.showinfo("Success", "Donation registered successfully!\nThank you for your generosity!")
                    self.close_and_return_to_main()
                else:
                    messagebox.showerror("Error", "Failed to register donation. Please try again.")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def cancel(self):
        if messagebox.askyesno("Cancel Registration", "Are you sure you want to cancel?"):
            self.close_and_return_to_main()

    def on_window_close(self):
        self.close_and_return_to_main()

    def close_and_return_to_main(self):
        self.window.destroy()
        self.parent.deiconify()

class MainScreenDonor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Donor Main Screen")
        self.root.geometry("400x500")

        self.donation_controller = MockDonationController()

        tk.Label(self.root, text="Donor Main Screen", font=("Helvetica", 16)).pack(pady=20)

        tk.Button(
            self.root,
            text="Report",
            command=self.report,
            width=20,
            height=2
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Register Donation",
            command=self.register_donation,
            width=20,
            height=2
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Track Donation Usage",
            command=self.track_donation_usage,
            width=20,
            height=2
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Manage Account",
            command=self.manage_account,
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2
        ).pack(side="bottom", pady=20)

    def report(self):
        messagebox.showinfo("Report", "Report button pressed. (Not implemented)")

    def register_donation(self):
        print("🔄 Register Donation button clicked!")
        
        self.root.withdraw()
        
        registration_form = RegistrationFormScreen(self.root, self.donation_controller)
        registration_form.display()

    def track_donation_usage(self):
        messagebox.showinfo("Track Donation Usage", "Track Donation Usage button pressed. (Not implemented)")

    def manage_account(self):
        self.root.withdraw()
        account_screen = AccountModScreen(self.root, "donor")
        account_screen.displayAccountModScreen(user_id=123)  

    def run(self):
        self.root.mainloop()