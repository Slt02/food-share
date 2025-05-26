from tkinter import messagebox
from Database import Database
from FoodRequest import FoodRequest
from GUI.WarningScreen import WarningScreen
from GUI.ConfirmedOrderScreen import ConfirmedOrderScreen
from GUI.TrackOrderScreen import TrackOrderScreen
from Report import Report
#from GUI.OrderHistoryScreen import OrderHistoryScreen

class OrderController:
    def __init__(self, root = None):
        self.root = root # Initialize the root window
        self.db = Database() # Create a new instance of the Database class

    # Submit an order to the database
    def submit_order(self, customer_id, number_of_people, delivery_address, items):
        if(self.validate_info(number_of_people, delivery_address, items)):
            # Check availability of items via Database
            # If items are available, create a new order
            if self.db.check_availability(items):
                # Create a new Food Request
                food_request = FoodRequest(customer_id, delivery_address, number_of_people, items)
                self.db.save_order(food_request) # Save the order to the database
                success_screen = ConfirmedOrderScreen(self.root) # Create a new Confirmed Order screen
                success_screen.show_confirmed_order(food_request) # Show the order confirmation screen
                self.db.update_quantities(items) # Update the inventory in the database
            else:
                print("Items not available")
                # Show a warning screen if items are not available
                warning_screen = WarningScreen(self.root, "Some of the items are not available! Please check your order.")
                warning_screen.show_warning()
        else:
            # Show a warning screen if the information is not valid
            warning_screen = WarningScreen(self.root, "Please fill in all fields.")
            warning_screen.show_warning()

    # Validate the information provided by the customer (missing fields, etc.)
    def validate_info(self, number_of_people, delivery_address, items):
        # Validate the information provided by the customer
        if not number_of_people or not delivery_address or not items:
            print("Missing information")
            return False
        return True

    # Check order existence
    def check_order_existence(self, customer_id):
        # Check if the order exists in the database
        request = self.db.query_order(customer_id)
        if request is not None:
            order_status_screen = TrackOrderScreen(self.root, customer_id)
            order_status_screen.show_order_status(request) # Show the order status screen
        else:
            # Show a warning screen if the order does not exist
            warning_screen = WarningScreen(self.root, "No order found for this customer ID.")
            warning_screen.show_warning()

    # Fetch order history
    def fetch_order_history(self, customer_id):
        from GUI.OrderHistoryScreen import OrderHistoryScreen
        # Fetch the order history from the database
        orders = self.db.query_order_history(customer_id)
        if orders:
            order_history_screen = OrderHistoryScreen(self.root, customer_id) 
            order_history_screen.display_order_history(orders)
        else:
            # Show a warning screen if no orders are found
            warning_screen = WarningScreen(self.root, "No order history found for this customer ID.")
            warning_screen.show_warning()

    # Validate report submission
    def validate_report(self, order, description):
        # Validate the report text
        if not description:
            warning_screen = WarningScreen(self.root, "Please provide a description for the report.")
            warning_screen.show_warning()
        else:
            report = Report(order.request_id, order.customer_id, description)
            self.db.create_report(report)  # Save the report to the database
            messagebox.showinfo("Report Submitted", "Your report has been submitted successfully.")
            # Redirect to order history
            self.fetch_order_history(order.customer_id)