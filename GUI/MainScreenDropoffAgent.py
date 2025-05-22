import tkinter as tk
from tkinter import messagebox
from GUI.AccountModScreen import AccountModScreen  

class MainScreenDropoffAgent:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Drop-Off Agent Main Screen")
        self.root.geometry("400x500")

        tk.Label(self.root, text="Drop-Off Agent Main Screen", font=("Helvetica", 16)).pack(pady=20)

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
        account_screen.displayAccountModScreen(user_id=123)  

    def run(self):
        self.root.mainloop()

