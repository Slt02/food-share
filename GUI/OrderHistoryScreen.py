import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk

class OrderHistoryScreen:
    def __init__(self, root):
        self.root = root

    # Display the order history in a formatted manner
    def display_order_history(self, history_list):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title = tk.Label(self.root, text="🕘 Order History", fg="#333")
        title.config(font=tkFont.Font(size=18, weight="bold"))
        title.pack(pady=20)

        # Loop through each order and display details
        for order in history_list:
            order_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
            order_frame.pack(pady=5, fill="x", padx=20)

            summary = f"Order ID: {order.request_id}\n" \
                      f"Date: {order.made}\n" \
                      f"Status: {order.status}\n" \
                      f"Address: {order.delivery_address}\n" \
                      f"People: {order.number_of_people}"

            summary_label = tk.Label(order_frame, text=summary, justify="left")
            summary_label.pack(anchor="w")

            tk.Label(order_frame, text="Items:", font=tkFont.Font(weight="bold")).pack(anchor="w", pady=(5, 0))

            for item, qty in order.items.items():
                item_label = tk.Label(order_frame, text=f"• {item}: {qty}")
                item_label.pack(anchor="w", padx=15)

        # Back button
        tk.Button(self.root, text="Back to Main Menu", command=self.back_to_main).pack(pady=20)

    def back_to_main(self):
        print("Returning to main menu...") #TODO: Placeholder for actual back navigation logic