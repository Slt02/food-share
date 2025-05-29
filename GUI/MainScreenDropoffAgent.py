import tkinter as tk
from tkinter import messagebox
from GUI.AccountModScreen import AccountModScreen  
from GUI.UpdateDeliveryStatusScreen import UpdateDeliveryStatusScreen
from GUI.AvailableRequestsScreen import AvailableRequestsScreen

class MainScreenDropoffAgent:
    def __init__(self, user_data=None):
        self.root = tk.Tk()
        self.root.title("Drop-Off Agent Main Screen")
        self.root.geometry("400x500")
        self.root.configure(bg="#9AFF9A")  # Light green background
        
        # Store user data and get the real user ID
        self.user_data = user_data
        self.user_id = user_data['id'] if user_data else None
        
        # FoodShare title at the top
        tk.Label(
            self.root, 
            text="FoodShare", 
            font=("Helvetica", 20, "bold"), 
            bg="#9AFF9A", 
            fg="#2F4F4F"
        ).pack(pady=(20, 10))
        
        # Display welcome message with user name
        if user_data:
            welcome_text = f"DROP-OFF AGENT - Welcome {user_data['name']}"
        else:
            welcome_text = "DROP-OFF AGENT"
        
        tk.Label(
            self.root, 
            text=welcome_text, 
            font=("Helvetica", 14), 
            bg="#9AFF9A", 
            fg="#2F4F4F"
        ).pack(pady=(0, 20))

        # "Update Delivery Status" button
        tk.Button(
            self.root,
            text="Update Delivery Status",
            command=self.update_delivery_status,
            width=20,
            height=2,
            bg="#32CD32",
            fg="white",
            font=("Helvetica", 10, "bold")
        ).pack(pady=10)

        # "Assign Delivery" button
        tk.Button(
            self.root,
            text="Assign Delivery",
            command=self.assign_delivery,
            width=20,
            height=2,
            bg="#32CD32",
            fg="white",
            font=("Helvetica", 10, "bold")
        ).pack(pady=10)

        # "View Available Requests" button
        tk.Button(
            self.root,
            text="View Available Requests",
            command=self.view_available_requests,
            width=20,
            height=2,
            bg="#32CD32",
            fg="white",
            font=("Helvetica", 10, "bold")
        ).pack(pady=10)

        # "Manage Account" button moved up with other buttons
        tk.Button(
            self.root,
            text="Manage Account",
            command=self.manage_account,
            bg="#32CD32",
            fg="white",
            width=20,
            height=2,
            font=("Helvetica", 10, "bold")
        ).pack(pady=10)

    def update_delivery_status(self):
        UpdateDeliveryStatusScreen(self.root, self.user_id)

    def assign_delivery(self):
        AvailableRequestsScreen(self.root, self.user_id)

    def view_available_requests(self):
        AvailableRequestsScreen(self.root, self.user_id)

    def manage_account(self):
        # Hide the drop-off agent main screen while the account modification window is active.
        self.root.withdraw()
        # Open the AccountModScreen for a drop-off agent.
        account_screen = AccountModScreen(self.root, "dropoffagent")
        
        account_screen.displayAccountModScreen(user_id=self.user_id)

    def display(self):
        """Display the dropoff agent main screen"""
        self.root.deiconify()  # Show the window if it was hidden
        self.root.mainloop()

    def run(self):
        self.display()