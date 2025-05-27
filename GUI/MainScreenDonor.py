import tkinter as tk
from tkinter import messagebox

class MainScreenDonor:
    def __init__(self, user_data=None):
        self.root = tk.Tk()
        self.root.title("Donor Main Screen")
        self.root.geometry("400x500")
        
        # Store user data and get the real user ID
        self.user_data = user_data
        self.user_id = user_data['id'] if user_data else None
        
        # Initialize DonationController - will be set up when needed
        self.DonationController = None
        
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

        # "Track Donation Usage" button - Updated to show PersonalDonationsScreen
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

    def _initialize_donation_controller(self):
        """Initialize DonationController when needed"""
        if self.DonationController is not None:
            return True
            
        try:
            from DonationController import DonationController
            self.DonationController = DonationController()
            print("DonationController initialized successfully")
            return True
        except ImportError:
            print("Could not import DonationController")
            return False
        except Exception as e:
            print(f"Error initializing DonationController: {e}")
            return False

    def _initialize_registration_form(self):
        """Initialize RegistrationFormScreen when needed"""
        try:
            from RegistrationFormScreen import RegistrationFormScreen
            return RegistrationFormScreen
        except ImportError:
            try:
                from GUI.RegistrationFormScreen import RegistrationFormScreen
                return RegistrationFormScreen
            except ImportError:
                print("Could not import RegistrationFormScreen")
                return None

    def _initialize_account_mod(self):
        """Initialize AccountModScreen when needed"""
        try:
            from AccountModScreen import AccountModScreen
            return AccountModScreen
        except ImportError:
            try:
                from GUI.AccountModScreen import AccountModScreen
                return AccountModScreen
            except ImportError:
                print("Could not import AccountModScreen")
                return None

    def _initialize_personal_donations_screen(self):
        """Initialize PersonalDonationsScreen when needed"""
        try:
            from PersonalDonationsScreen import PersonalDonationsScreen
            return PersonalDonationsScreen
        except ImportError:
            try:
                from GUI.PersonalDonationsScreen import PersonalDonationsScreen
                return PersonalDonationsScreen
            except ImportError:
                print("Could not import PersonalDonationsScreen")
                return None

    def report(self):
        messagebox.showinfo("Report", "Report button pressed. (Not implemented)")

    def register_donation(self):
        """Open the registration form screen"""
        print("Register Donation button clicked...")
        
        # Initialize DonationController
        if not self._initialize_donation_controller():
            messagebox.showwarning("Missing Module", 
                                 "DonationController not found.\n\n"
                                 "Please make sure you have:\n"
                                 "• DonationController.py file\n"
                                 "• Database.py file (for database)")
            return
        
        # Initialize RegistrationFormScreen
        RegistrationFormScreenClass = self._initialize_registration_form()
        if not RegistrationFormScreenClass:
            messagebox.showwarning("Missing Module", 
                                 "RegistrationFormScreen not found.\n\n"
                                 "Please create RegistrationFormScreen.py file\n"
                                 "with the registration form code.")
            return
        
        try:
            print("Opening Registration Form from Donor Main Screen...")
            self.root.withdraw()  # Hide the donor main screen
            
            # Create and display registration form - pass user_id
            registration_form = RegistrationFormScreenClass(self.root, self.DonationController, self.user_id)
            registration_form.display()
            
        except TypeError as te:
            print(f"TypeError: {te}")
            print("This suggests a signature mismatch. Trying alternative approach...")
            try:
                
                registration_form = RegistrationFormScreenClass(self.root)
                registration_form.DonationController = self.DonationController  
                registration_form.display()
            except Exception as e2:
                print(f"Alternative approach failed: {e2}")
                messagebox.showerror("Error", f"Failed to create registration form:\n{str(te)}\n\nTry checking RegistrationFormScreen constructor.")
                self.root.deiconify()
        except Exception as e:
            print(f"Error opening registration form: {e}")
            messagebox.showerror("Error", f"Failed to open registration form:\n{str(e)}")
            self.root.deiconify()  # Show main screen again if error

    def track_donation_usage(self):
        """Track personal donations - Show PersonalDonationsScreen"""
        print("Track Donation Usage button clicked...")
        
        # Check if user is logged in
        if not self.user_id:
            messagebox.showwarning("Login Required", 
                                 "Please log in to view your donation history.")
            return
        
        # Initialize PersonalDonationsScreen
        PersonalDonationsScreenClass = self._initialize_personal_donations_screen()
        if not PersonalDonationsScreenClass:
            messagebox.showwarning("Missing Module", 
                                 "PersonalDonationsScreen not found.\n\n"
                                 "Please make sure you have:\n"
                                 "• PersonalDonationsScreen.py\n"
                                 "• PersonalDonationsController.py\n"
                                 "• Database.py")
            return
        
        try:
            print(f"Opening Personal Donations Screen for donor ID: {self.user_id}")
            self.root.withdraw()  # Hide the donor main screen
            
            # Create and display PersonalDonationsScreen with logged-in donor's ID
            donations_screen = PersonalDonationsScreenClass(self.root, self.user_id)
            donations_screen.show()
            
            # Show main screen when donations screen closes
            self.root.deiconify()
            
        except Exception as e:
            print(f"Error opening donations screen: {e}")
            messagebox.showerror("Error", f"Could not load your donation history:\n{str(e)}")
            self.root.deiconify()  # Show main screen again if error

    def manage_account(self):
        print("Manage Account button clicked...")
        
        # Initialize AccountModScreen
        AccountModScreen = self._initialize_account_mod()
        if not AccountModScreen:
            messagebox.showwarning("Missing Module", 
                                 "AccountModScreen not found.\n\n"
                                 "Please make sure AccountModScreen.py exists.")
            return
        
        try:
            # Hide the donor main screen while account modifications take place.
            self.root.withdraw()
            # Open the AccountModScreen for a donor.
            account_screen = AccountModScreen(self.root, "donor")
            # Use the real user_id from the logged-in user
            account_screen.displayAccountModScreen(user_id=self.user_id)
            
        except Exception as e:
            print(f"Error opening account screen: {e}")
            messagebox.showerror("Error", f"Failed to open account screen:\n{str(e)}")
            self.root.deiconify()  # Show main screen again if error

    def display(self):
        """Display the donor main screen"""
        self.root.deiconify()  # Show the window if it was hidden
        self.root.mainloop()

    def run(self):
        self.display()