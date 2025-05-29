import tkinter as tk
from tkinter import messagebox
from GUI.AccountModScreen import AccountModScreen  
from GUI.StatisticsReportScreen import StatisticsReportScreen
from GUI.DropOffRegistrationScreen import DropOffRegistrationScreen

class MainScreenAdmin:
    def __init__(self, root=None, user_data=None):
        self.root = tk.Tk() if root is None else root 
        self.root.title("Admin Main Screen")
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
            welcome_text = f"ADMIN - Welcome {user_data['name']}"
        else:
            welcome_text = "ADMIN"
        
        tk.Label(
            self.root, 
            text=welcome_text, 
            font=("Helvetica", 14), 
            bg="#9AFF9A", 
            fg="#2F4F4F"
        ).pack(pady=(0, 20))

        # "Manage Inventory" button
        tk.Button(
            self.root,
            text="Manage Inventory",
            command=self.manage_inventory,
            width=20,
            height=2,
            bg="#32CD32",
            fg="white",
            font=("Helvetica", 10, "bold")
        ).pack(pady=10)

        # "Monitor Requests" button
        tk.Button(
            self.root,
            text="Monitor Requests",
            command=self.monitor_requests,
            width=20,
            height=2,
            bg="#32CD32",
            fg="white",
            font=("Helvetica", 10, "bold")
        ).pack(pady=10)

        # "Monitor Delivery" button
        tk.Button(
            self.root,
            text="Monitor Delivery",
            command=self.monitor_delivery,
            width=20,
            height=2,
            bg="#32CD32",
            fg="white",
            font=("Helvetica", 10, "bold")
        ).pack(pady=10)

        # "View Statistics & Reports" button
        tk.Button(
            self.root,
            text="View Statistics & Reports",
            command=self.view_statistics,
            width=20,
            height=2,
            bg="#32CD32",
            fg="white",
            font=("Helvetica", 10, "bold")
        ).pack(pady=10)

        # "Create Drop-Off Account" button
        tk.Button(
            self.root,
            text="Create Drop-Off Account",
            command=self.create_drop_off_agent_account,
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

    def manage_inventory(self):
        from GUI.ManageInventoryScreen import ManageInventoryScreen
        
        # Hide the admin main screen
        self.root.withdraw()
        
        # Create a new window for inventory management
        inventory_window = tk.Toplevel(self.root)
        inventory_app = ManageInventoryScreen(inventory_window)
        
    def monitor_requests(self):
        

        from GUI.PendingOrdersScreen import PendingOrdersScreen
        
        # Hide the admin main screen
        self.root.withdraw()
        
        # Create a new window for inventory management
        PendingOrders_window = tk.Toplevel(self.root)
        PendingOrders_app = PendingOrdersScreen(PendingOrders_window)


    def monitor_delivery(self):
        messagebox.showinfo("Monitor Delivery", "Monitor Delivery button clicked. (Not implemented)")

    def view_statistics(self):
        # Pass the real admin_id instead of hardcoded 123
        admin_id = self.user_id if self.user_id else 123
        StatisticsReportScreen(self.root, admin_id=admin_id)

    def manage_account(self):
        # Hide the admin main screen while AccountModScreen is active.
        self.root.withdraw()

        # Open the AccountModScreen window;
        # pass self.root as the parent and the role "admin".
        account_screen = AccountModScreen(self.root, "admin")
        # Use the real user_id from the logged-in user instead of hardcoded 123
        account_screen.displayAccountModScreen(user_id=self.user_id)

    def display(self):
        """Display the admin main screen"""
        self.root.deiconify()  # Show the window if it was hidden
        self.root.mainloop()

    def run(self):
        self.display()

        # Create a new Drop-Off Agent account when the button is clicked
    
    # Click handler for "Create Drop-Off Account" button
    def create_drop_off_agent_account(self):
        # Open the DropOffRegistrationScreen
        drop_off_screen = DropOffRegistrationScreen(self.root)
        drop_off_screen.show_registration_form()