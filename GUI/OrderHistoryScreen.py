import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk
from GUI.ReportFormScreen import ReportFormScreen
from GUI.MainScreenCustomer import CustomerMainScreen

class OrderHistoryScreen:
    def __init__(self, root, customer_id=None):
        self.customer_id = customer_id
        self.root = root

    # Display the order history in a formatted manner
    def display_order_history(self, history_list):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Wrapper frame to contain canvas and scrollbar
        wrapper = tk.Frame(self.root)
        wrapper.pack(fill="both", expand=True)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(wrapper)
        scrollbar = tk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Title
        title = tk.Label(scrollable_frame, text="🕘 Order History", fg="#333")
        title.config(font=tkFont.Font(size=18, weight="bold"))
        title.pack(pady=20)

        # Loop through each order and display details
        for order in history_list:
            order_frame = tk.Frame(scrollable_frame, bd=2, relief="ridge", padx=50, pady=15)
            order_frame.pack(pady=15, fill="both", padx=30, expand=True)

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

            # Inside the for loop, where each order is displayed, add a report button
            report_button = tk.Button(order_frame, text="Report" , command=lambda o=order: self.click_report(o))
            report_button.pack(pady=(5,0))

        # Back button
        tk.Button(self.root, text="Back to Main Menu", command=self.back_to_main).pack(pady=10)

    # Event handler when the report button is clicked
    def click_report(self, order):
        report_screen = ReportFormScreen(self.root)
        report_screen.display_form(order)

    def back_to_main(self):
        # Clear current screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Load the main screen
        CustomerMainScreen(self.root, self.customer_id)
