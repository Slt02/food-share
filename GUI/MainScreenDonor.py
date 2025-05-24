import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import GUI.AccountModScreen from AccountModScreen

import re

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

if __name__ == "__main__":
    print("🚀 Starting Donor Main Screen...")
    
    try:
        app = MainScreenDonor()
        app.run()
        
    except Exception as e:
        print(f"❌ Error running application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")