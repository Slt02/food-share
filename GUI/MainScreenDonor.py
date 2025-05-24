import tkinter as tk
from tkinter import messagebox
from GUI.AccountModScreen import AccountModScreen  

class MainScreenDonor:
    def __init__(self, user_data=None):
        self.root = tk.Tk()
        self.root.title("Donor Main Screen")
        self.root.geometry("400x500")
        
        # Store user data and get the real user ID
        self.user_data = user_data
        self.user_id = user_data['id'] if user_data else None
        
        # Display welcome message with user name
        if user_data:
            welcome_text = f"Donor Main Screen - Welcome {user_data['name']}"
        else:
            welcome_text = "Donor Main Screen"
        
        tk.Label(self.root, text=welcome_text, font=("Helvetica", 16)).pack(pady=20)

        # "Report" button
        tk.Button(
            self.root,
            text="Report",
            command=self.report,
            width=20,
            height=2
        ).pack(pady=10)

        # "Register Donation" button
        tk.Button(
            self.root,
            text="Register Donation",
            command=self.register_donation,
            width=20,
            height=2
        ).pack(pady=10)

        # "Track Donation Usage" button
        tk.Button(
            self.root,
            text="Track Donation Usage",
            command=self.track_donation_usage,
            width=20,
            height=2
        ).pack(pady=10)

        # "Manage Account" button at the bottom.
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
        messagebox.showinfo("Register Donation", "Register Donation button pressed. (Not implemented)")

    def track_donation_usage(self):
        messagebox.showinfo("Track Donation Usage", "Track Donation Usage button pressed. (Not implemented)")

    def manage_account(self):
        # Hide the donor main screen while account modifications take place.
        self.root.withdraw()
        # Open the AccountModScreen for a donor.
        account_screen = AccountModScreen(self.root, "donor")
        # Use the real user_id from the logged-in user instead of hardcoded 123
        account_screen.displayAccountModScreen(user_id=self.user_id)

    def display(self):
        """Display the donor main screen"""
        self.root.deiconify()  # Show the window if it was hidden
        self.root.mainloop()

    def run(self):
        self.display()