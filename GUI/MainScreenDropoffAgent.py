import tkinter as tk
from tkinter import messagebox
from GUI.AccountModScreen import AccountModScreen  
from GUI.UpdateDeliveryStatusScreen import UpdateDeliveryStatusScreen

class MainScreenDropoffAgent:
    def __init__(self, user_data=None):
        self.root = tk.Tk()
        self.root.title("Drop-Off Agent Main Screen")
        self.root.geometry("400x500")
        
        # Store user data and get the real user ID
        self.user_data = user_data
        self.user_id = user_data['id'] if user_data else None
        
        # Display welcome message with user name
        if user_data:
            welcome_text = f"Drop-Off Agent Main Screen - Welcome {user_data['name']}"
        else:
            welcome_text = "Drop-Off Agent Main Screen"
        
        tk.Label(self.root, text=welcome_text, font=("Helvetica", 16)).pack(pady=20)

        # "Update Delivery Status" button
        tk.Button(
            self.root,
            text="Update Delivery Status",
            command=self.update_delivery_status,
            width=20,
            height=2
        ).pack(pady=10)

        # "Assign Delivery" button
        tk.Button(
            self.root,
            text="Assign Delivery",
            command=self.assign_delivery,
            width=20,
            height=2
        ).pack(pady=10)

        # "View Available Requests" button
        tk.Button(
            self.root,
            text="View Available Requests",
            command=self.view_available_requests,
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

    def update_delivery_status(self):
        messagebox.showinfo("Update Delivery Status", "Update Delivery Status clicked. (Not implemented)")

    def assign_delivery(self):
        messagebox.showinfo("Assign Delivery", "Assign Delivery button clicked. (Not implemented)")

    def view_available_requests(self):
        messagebox.showinfo("View Available Requests", "View Available Requests button clicked. (Not implemented)")

    def manage_account(self):
        # Hide the drop-off agent main screen while the account modification window is active.
        self.root.withdraw()
        # Open the AccountModScreen for a drop-off agent.
        account_screen = AccountModScreen(self.root, "drop_off_agent")
        
        account_screen.displayAccountModScreen(user_id=self.user_id)
    
    def update_delivery_status(self):
        UpdateDeliveryStatusScreen(self.root, self.user_id)

    def display(self):
        """Display the dropoff agent main screen"""
        self.root.deiconify()  # Show the window if it was hidden
        self.root.mainloop()

    def run(self):
        self.display()