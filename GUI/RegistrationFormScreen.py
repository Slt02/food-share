import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Mock DonationController to prevent import errors
class MockDonationController:
    def create_donation(self, donor_id, item_name, quantity, donation_date):
        print(f"🔄 Mock: Creating donation - {item_name} x{quantity}")
        print(f"🔄 Mock: Donor ID: {donor_id}, Date: {donation_date}")
        
        # Always return True for testing - should show success popup
        result = True
        print(f"🔄 Mock: Returning {result}")
        return result

# Simple AccountModScreen to avoid GUI import issues
class AccountModScreen:
    def __init__(self, parent, user_role):
        self.parent = parent
        self.window = tk.Toplevel(self.parent)
        self.window.title("Account Management")
        self.window.geometry("300x200")

    def displayAccountModScreen(self, user_id):
        tk.Label(self.window, text=f"Account Management\nUser ID: {user_id}", 
                font=("Arial", 12)).pack(pady=30)
        tk.Button(self.window, text="Close", command=self.close,
                 bg="#4CAF50", fg="white").pack(pady=20)

    def close(self):
        self.window.destroy()
        self.parent.deiconify()

class RegistrationFormScreen:
    def __init__(self, parent, DonationController):
        self.parent = parent
        self.DonationController = DonationController
        self.window = None
        self.donation_data = {}

    def display(self):
        print("Opening Registration Form Screen...")
        
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
            
            # Basic input validation
            if not item_name:
                messagebox.showerror("Missing Information", "Please enter what you are donating")
                self.item_name_entry.focus()
                return
            
            if not quantity or not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showerror("Invalid Input", "Please enter a valid quantity (positive number)")
                self.quantity_entry.focus()
                return
            
            quantity_int = int(quantity)
            
            # Show confirmation dialog
            confirm_msg = f"You are donating:\n\n• Item: {item_name}\n• Quantity: {quantity_int}\n\nSubmit this donation?"
            
            if messagebox.askyesno("Confirm Donation", confirm_msg):
                print("🔄 Submitting donation to DonationController...")
                
                # Check if DonationController is available
                if not self.DonationController:
                    messagebox.showerror("Error", "Donation system is not available. Please try again later.")
                    return
                
                try:
                    print(f"🔍 Validating donation: {item_name} x{quantity_int}")
                    
                    # Call DonationController to create donation
                    success = self.DonationController.create_donation(
                        donor_id=1,  # This would be the actual logged-in donor's ID
                        item_name=item_name,
                        quantity=quantity_int,
                        donation_date=datetime.now()
                    )
                    
                    print(f"🔍 DonationController returned: {success}")
                    
                    if success:
                        # SUCCESS POPUP - Show detailed success message
                        print("✅ Donation created successfully! Showing success popup...")
                        self.show_success_popup(item_name, quantity_int)
                    else:
                        # WARNING POPUP - Validation failed
                        print("⚠️ Donation validation failed! Showing warning popup...")
                        messagebox.showwarning(
                            "Warning! ⚠️", 
                            f"Unable to register your donation.\n\n"
                            f"Possible reasons:\n"
                            f"• Invalid item name or quantity\n"
                            f"• Database connection issue\n"
                            f"• System validation error\n\n"
                            f"Please check your details and try again."
                        )
                
                except Exception as controller_error:
                    # ERROR POPUP - Controller exception
                    print(f"❌ DonationController error: {controller_error}")
                    messagebox.showerror(
                        "System Error! ❌", 
                        f"A system error occurred while processing your donation:\n\n"
                        f"{str(controller_error)}\n\n"
                        f"Please try again or contact support if the problem persists."
                    )
            
        except Exception as e:
            # GENERAL ERROR POPUP
            print(f"❌ General error: {e}")
            messagebox.showerror(
                "Unexpected Error! ❌", 
                f"An unexpected error occurred:\n\n{str(e)}\n\n"
                f"Please try again or restart the application."
            )

    def show_success_popup(self, item_name, quantity):
        """Display a detailed success popup with celebration message"""
        # Generate current timestamp for confirmation
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create success message with celebration emojis and details
        success_message = (
            f"🎉 DONATION REGISTERED SUCCESSFULLY! 🎉\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📦 Item: {item_name}\n"
            f"📊 Quantity: {quantity}\n"
            f"📅 Date: {timestamp}\n"
            f"👤 Donor ID: #001\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🌟 Thank you for your generous donation! 🌟\n\n"
            f"Your contribution will make a real difference\n"
            f"in the lives of those who need it most.\n\n"
            f"🤝 Together, we're building a stronger community!\n\n"
            f"📋 Your donation has been logged and will be\n"
            f"processed by our distribution team shortly.\n\n"
            f"💚 We appreciate your kindness and generosity! 💚"
        )
        
        # Show the success popup
        messagebox.showinfo("🎉 DONATION SUCCESS 🎉", success_message)
        
        # After showing success, return to main screen
        print("✅ Success popup displayed. Returning to main screen...")
        self.close_and_return_to_main()

    def cancel(self):
        if messagebox.askyesno("Cancel Registration", "Are you sure you want to cancel?"):
            self.close_and_return_to_main()

    def on_window_close(self):
        self.close_and_return_to_main()

    def close_and_return_to_main(self):
        print("🔄 Closing registration form and returning to main screen...")
        self.window.destroy()
        self.parent.deiconify()


class MainScreenDonor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Donor Main Screen")
        self.root.geometry("400x500")
        
        # Try to import real DonationController, use mock if not found
        try:
            from DonationController import DonationController
            self.DonationController = DonationController()
            print("✅ Real DonationController connected successfully!")
        except ImportError:
            print("⚠️ Real DonationController not found - using MockDonationController")
            self.DonationController = MockDonationController()

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

        # "Manage Account" button
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
        registration_form = RegistrationFormScreen(self.root, self.DonationController)
        registration_form.display()

    def track_donation_usage(self):
        messagebox.showinfo("Track Donation Usage", "Track Donation Usage button pressed. (Not implemented)")

    def manage_account(self):
        # Hide the donor main screen while account modifications take place
        self.root.withdraw()
        # Open the AccountModScreen for a donor
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