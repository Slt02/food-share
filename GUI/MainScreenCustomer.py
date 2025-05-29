import tkinter as tk
from tkinter import messagebox
from GUI.AccountModScreen import AccountModScreen  
from GUI.DropOffRegistrationScreen import DropOffRegistrationScreen
from order_controller import OrderController
from GUI.MenuScreen import MenuScreen
from Database import Database

class CustomerMainScreen:
    def __init__(self, root=None, customer_id=None):
        self.root = root if root is not None else tk.Tk()  # Use provided root or create a new one
        self.root.title("Customer Main Screen")
        self.root.geometry("500x500")
        self.root.configure(bg="#9AFF9A")  # Light green background
        
        # Store user data and get the real user ID
        self.customer_id = customer_id
        self.user_id = customer_id  # Fixed: use customer_id as user_id
        
        # Initialize database connection
        self.init_database()
        
        # FoodShare title at the top
        tk.Label(
            self.root, 
            text="FoodShare", 
            font=("Helvetica", 20, "bold"), 
            bg="#9AFF9A", 
            fg="#2F4F4F"
        ).pack(pady=(20, 10))
        
        # Display welcome message with user name
        welcome_text = "CUSTOMER - Welcome"
        
        tk.Label(
            self.root, 
            text=welcome_text, 
            font=("Helvetica", 14), 
            bg="#9AFF9A", 
            fg="#2F4F4F"
        ).pack(pady=(0, 20))

        # "Menu" button
        tk.Button(
            self.root, 
            text="Menu", 
            command=self.menu, 
            width=20, 
            height=2,
            bg="#32CD32",
            fg="white",
            font=("Helvetica", 10, "bold")
        ).pack(pady=10)
        
        # "Order History" button
        tk.Button(
            self.root, 
            text="Order History", 
            command=self.order_history, 
            width=20, 
            height=2,
            bg="#32CD32",
            fg="white",
            font=("Helvetica", 10, "bold")
        ).pack(pady=10)
        
        # "Track Order" button
        tk.Button(
            self.root, 
            text="Track Order", 
            command=self.track_order, 
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

    def init_database(self):
        """Initialize database connection using Database class"""
        try:
            self.db = Database()
        except Exception as e:
            self.db = None

    def menu(self):
        """Open MenuScreen to display available food items"""        
        if not self.db:
            messagebox.showerror("Database Error", "No database connection available")
            return
        
        try:
            # Hide the main screen
            self.root.withdraw()
            
            # Create and display MenuScreen - Fixed: only pass parent parameter
            menu_screen = MenuScreen(self.root, self.customer_id)
            menu_screen.show()
            
            # Show main screen when menu window is closed
            self.root.deiconify()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open menu screen:\n{str(e)}")
            self.root.deiconify()  # Show main screen again

    # Fetch and display the order history for the customer when the button is clicked
    def order_history(self):
        order_controller = OrderController(self.root)
        order_controller.fetch_order_history(self.customer_id)

    # Track the order for the customer when the button is clicked
    def track_order(self):
        order_controller = OrderController(self.root)
        order_controller.check_order_existence(self.customer_id)

    def manage_account(self):
        # Hide the main screen while account modifications take place.
        self.root.withdraw()
        # Open the AccountModScreen passing in the parent window and role ("customer").
        account_screen = AccountModScreen(self.root, "customer")
        # Use the real user_id from the logged-in user
        account_screen.displayAccountModScreen(user_id=self.user_id)

    def display(self):
        """Display the customer main screen"""
        self.root.deiconify()  # Show the window if it was hidden
        self.root.mainloop()

    def run(self):
        self.display()