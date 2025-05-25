import tkinter as tk
from tkinter import font as tkFont
from order_controller import OrderController

class ReportFormScreen:
    def __init__(self, root):
        self.root = root
        self.order_controller = OrderController(self.root)

    # Display the report form for a specific order
    def display_form(self, order):
        # Hold the current order for which the report is being made
        self.current_order = order


       # Clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title = tk.Label(self.root, text="📝 Report a Problem", fg="#b30000")
        title.config(font=tkFont.Font(size=18, weight="bold"))
        title.pack(pady=20)

        # Order ID
        tk.Label(self.root, text=f"Order ID: {order.request_id}", font=tkFont.Font(weight="bold")).pack()

        # Report Reason
        tk.Label(self.root, text="Describe the issue:").pack(pady=(10, 0))
        self.report_entry = tk.Text(self.root, height=6, width=40)
        self.report_entry.pack(pady=5)

        # Submit Button
        submit_btn = tk.Button(self.root, text="Submit Report", bg="#cc0000", fg="white", command=lambda: self.submit_report(order))
        submit_btn.pack(pady=15)

        # Back Button
        tk.Button(self.root, text="Cancel", command=self.back_to_history).pack()

    # Submit the report for the order
    # This method will call the controller to validate and submit the report
    def submit_report(self, order):
        description = self.report_entry.get("1.0", tk.END).strip()
        self.order_controller.validate_report(order, description)
        
    # Navigate back to the order history screen
    def back_to_history(self):
        # Navigate to the order history screen
        self.order_controller.fetch_order_history(self.current_order.customer_id)
