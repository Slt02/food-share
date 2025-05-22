import tkinter as tk
from tkinter import font as tkFont

# Class to display the confirmed order screen
class ConfirmedOrderScreen:
    def __init__(self, root):
        self.root = root

    # Function to show the confirmed order screen with the order details
    def show_confirmed_order(self, food_request):
        #Clear existing widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title Label
        title = tk.Label(self.root, text="🎉 Order Confirmed!", fg="green")
        title.config(font=tkFont.Font(size=18, weight="bold"))
        title.pack(pady=(20, 10))

        # Summary Info
        summary = f"Name: {food_request.customer_id}\n" \
                  f"Address: {food_request.delivery_address}\n" \
                  f"Number of People: {food_request.number_of_people}\n\n" \
                  f"Items Ordered:"
        summary_label = tk.Label(self.root, text=summary)
        summary_label.config(font=tkFont.Font(size=12))
        summary_label.pack(pady=(0, 10))

        for item, qty in food_request.items.items():
            item_label = tk.Label(self.root, text=f"• {item}: {qty}")
            item_label.config(font=tkFont.Font(size=11))
            item_label.pack(anchor="w", padx=30)

        # Close button
        close_button = tk.Button(self.root, text="Close", command=self.close_order)
        close_button.pack(pady=20)

    # TODO: Add a function to close the order screen and return to the main menu
    # For now, it just closes the popup window
    def close_order(self):
        self.root.destroy() # Close the popup window