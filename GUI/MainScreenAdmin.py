import tkinter as tk
from tkinter import messagebox
from GUI.AccountModScreen import AccountModScreen  

class MainScreenAdmin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Main Screen")
        self.root.geometry("400x500")

        tk.Label(self.root, text="Admin Main Screen", font=("Helvetica", 16)).pack(pady=20)

        # "Manage Inventory" button
        tk.Button(
            self.root,
            text="Manage Inventory",
            command=self.manage_inventory,
            width=20,
            height=2
        ).pack(pady=10)

        # "Monitor Requests" button
        tk.Button(
            self.root,
            text="Monitor Requests",
            command=self.monitor_requests,
            width=20,
            height=2
        ).pack(pady=10)

        # "Monitor Delivery" button
        tk.Button(
            self.root,
            text="Monitor Delivery",
            command=self.monitor_delivery,
            width=20,
            height=2
        ).pack(pady=10)

        # "View Statistics & Reports" button
        tk.Button(
            self.root,
            text="View Statistics & Reports",
            command=self.view_statistics,
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

    def manage_inventory(self):
        messagebox.showinfo("Manage Inventory", "Manage Inventory button clicked. (Not implemented)")

    def monitor_requests(self):
        messagebox.showinfo("Monitor Requests", "Monitor Requests button clicked. (Not implemented)")

    def monitor_delivery(self):
        messagebox.showinfo("Monitor Delivery", "Monitor Delivery button clicked. (Not implemented)")

    def view_statistics(self):
        messagebox.showinfo("Statistics & Reports", "View Statistics & Reports button clicked. (Not implemented)")

    def manage_account(self):
        # Hide the admin main screen while AccountModScreen is active.
        self.root.withdraw()

        # Open the AccountModScreen window;
        # pass self.root as the parent and the role "admin".
        account_screen = AccountModScreen(self.root, "admin")
        account_screen.displayAccountModScreen(user_id=123)  

    def run(self):
        self.root.mainloop()

