import tkinter as tk
from tkinter import messagebox
from GUI.AccountModScreen import AccountModScreen  # Ensure this file is in the same directory or in the PYTHONPATH

class CustomerMainScreen:
    def __init__(self, user_data=None):
        self.root = tk.Tk()
        self.root.title("Customer Main Screen")
        self.root.geometry("400x500")
        
        # Store user data and get the real user ID
        self.user_data = user_data
        self.user_id = user_data['id'] if user_data else None
        
        # Display welcome message with user name
        if user_data:
            welcome_text = f"Customer Main Screen - Welcome {user_data['name']}"
        else:
            welcome_text = "Customer Main Screen"
        
        tk.Label(self.root, text=welcome_text, font=("Helvetica", 16)).pack(pady=20)

        # "Menu" button
        tk.Button(self.root, text="Menu", command=self.menu, width=20, height=2).pack(pady=10)
        
        # "Order History" button
        tk.Button(self.root, text="Order History", command=self.order_history, width=20, height=2).pack(pady=10)
        
        # "Track Order" button
        tk.Button(self.root, text="Track Order", command=self.track_order, width=20, height=2).pack(pady=10)

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

    def menu(self):
        messagebox.showinfo("Menu", "Menu button clicked. (Not implemented)")

    def order_history(self):
        messagebox.showinfo("Order History", "Order History button clicked. (Not implemented)")

    def track_order(self):
        messagebox.showinfo("Track Order", "Track Order button clicked. (Not implemented)")

    def manage_account(self):
        # Hide the main screen while account modifications take place.
        self.root.withdraw()
        # Open the AccountModScreen passing in the parent window and role ("customer").
        account_screen = AccountModScreen(self.root, "customer")
        # Use the real user_id from the logged-in user instead of hardcoded 7
        account_screen.displayAccountModScreen(user_id=self.user_id)

    def display(self):
        """Display the customer main screen"""
        self.root.deiconify()  # Show the window if it was hidden
        self.root.mainloop()

    def run(self):
        self.display()