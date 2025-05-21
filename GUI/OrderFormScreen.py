import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from OrderController import OrderController

class OrderFormScreen:
    def __init__(self, root, selected_items):
        self.root = root
        self.selected_items = selected_items
        self.root.title("Order Form")
        self.controller = OrderController()  # Create an instance of the OrderController

    # Function to show up the form with the details of the order 
    def showOrderForm(self):
        print("Showing Order Form")
        row = 0
        # Selected Items Summary
        tk.Label(self.root, text="Selected Items:").grid(row=row, column=0, sticky="w", pady=(10, 0))        
        row += 1
        for item, qty in self.selected_items.items():
            tk.Label(self.root, text=f"{item}: {qty}").grid(row=row, column=0, sticky="w")
            row += 1

        # Full Name
        tk.Label(self.root, text="Full Name:").grid(row=row, column=0, sticky="w", pady=(10, 0))
        self.name_entry = tk.Entry(self.root, width=40)
        self.name_entry.grid(row=row, column=1)
        row += 1

        # Address
        tk.Label(self.root, text="Delivery Address:").grid(row=row, column=0, sticky="w", pady=(10, 0))
        self.address_entry = tk.Entry(self.root, width=40)
        self.address_entry.grid(row=row, column=1)
        row += 1

        # Number of People
        tk.Label(self.root, text="Number of People:").grid(row=row, column=0, sticky="w", pady=(10, 0))
        self.people_entry = tk.Entry(self.root, width=10)
        self.people_entry.grid(row=row, column=1, sticky="w")
        row += 1

        # Submit Button
        submit_btn = tk.Button(self.root, text="Complete Order", command=self.click_complete_order)
        submit_btn.config(font=tkFont.Font(size=12, weight="bold"), bg="#4CAF50", fg="white")
        submit_btn.grid(row=row, column=0, columnspan=2, pady=20)

    def click_complete_order(self):
        # Get the values from the entries
        name = self.name_entry.get()
        address = self.address_entry.get()
        num_people = self.people_entry.get()

        # Call the controller to handle the order submission
        self.controller.submit_order(name, address, num_people, self.selected_items)