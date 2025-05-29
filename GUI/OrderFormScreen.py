import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from order_controller import OrderController

class OrderFormScreen:
    def __init__(self, parent, selected_items, customer_id=None):
        self.parent = parent
        self.selected_items = selected_items
        self.window = tk.Toplevel(self.parent) if parent else tk.Tk()  # Create a new window or use the parent
        self.window.title("Order Form")
        self.controller = OrderController(self.window)  # Create an instance of the OrderController
        self.customer_id = customer_id  # Store customer ID if provided

    # Function to show up the form with the details of the order 
    def showOrderForm(self):
        # Set background color
        self.window.configure(bg="#9AFF9A")
        row = 0
        # Selected Items Summary
        tk.Label(self.window, text="Selected Items:", bg= "#9AFF9A").grid(row=row, column=0, sticky="w", pady=(10, 0))        
        row += 1
        for item, qty in self.selected_items.items():
            tk.Label(self.window, text=f"{item}: {qty}", bg= "#9AFF9A").grid(row=row, column=0, sticky="w")
            row += 1

        # Full Name
        tk.Label(self.window, text="Full Name:", bg= "#9AFF9A").grid(row=row, column=0, sticky="w", pady=(10, 0))
        self.name_entry = tk.Entry(self.window, width=40)
        self.name_entry.grid(row=row, column=1)
        row += 1

        # Address
        tk.Label(self.window, text="Delivery Address:", bg= "#9AFF9A").grid(row=row, column=0, sticky="w", pady=(10, 0))
        self.address_entry = tk.Entry(self.window, width=40)
        self.address_entry.grid(row=row, column=1)
        row += 1

        # Number of People
        tk.Label(self.window, text="Number of People:", bg= "#9AFF9A").grid(row=row, column=0, sticky="w", pady=(10, 0))
        self.people_entry = tk.Entry(self.window, width=10)
        self.people_entry.grid(row=row, column=1, sticky="w")
        row += 1

        # Submit Button
        submit_btn = tk.Button(self.window, text="Complete Order", command=self.click_complete_order)
        submit_btn.config(font=tkFont.Font(size=12, weight="bold"), bg="#4CAF50", fg="white")
        submit_btn.grid(row=row, column=0, columnspan=2, pady=20)

    def click_complete_order(self):
        # Get the values from the entries
        name = self.name_entry.get()
        address = self.address_entry.get()
        num_people = self.people_entry.get()

        # Call the controller to handle the order submission
        self.controller.submit_order(self.customer_id, num_people, address,  self.selected_items)