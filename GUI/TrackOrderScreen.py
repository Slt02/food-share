import tkinter as tk
from tkinter import font as tkFont

class TrackOrderScreen:

    def __init__(self, root):
        self.root = root
    
    def show_order_status(self, food_request):
        # Clear the root window
        # Clear previous content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title = tk.Label(self.root, text="📦 Track Your Order", fg="#333")
        title.config(font=tkFont.Font(size=18, weight="bold"))
        title.pack(pady=20)

        # Status
        status_label = tk.Label(self.root, text=f"Current Status: {food_request.status}")
        status_label.config(font=tkFont.Font(size=14), fg="blue")
        status_label.pack(pady=(0, 10))

        # Summary
        summary = f"Address: {food_request.delivery_address}\n" \
                  f"People: {food_request.number_of_people}\n"
        summary_label = tk.Label(self.root, text=summary)
        summary_label.pack(pady=(0, 10))

        # Items
        tk.Label(self.root, text="Items Ordered:").pack(anchor="w", padx=30)
        for item, qty in food_request.items.items():
            tk.Label(self.root, text=f"• {item}: {qty}").pack(anchor="w", padx=50)
        

        #Return to main menu button
        tk.Button(self.root, text="Back to Main Menu", command=self.back_to_main).pack(pady=20)

    def back_to_main(self):
        # TODO: Implement the logic to go back to the main menu
        print("Back to main menu")
