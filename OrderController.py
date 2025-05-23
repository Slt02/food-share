from Database import Database
from FoodRequest import FoodRequest
from GUI.WarningScreen import WarningScreen
from GUI.ConfirmedOrderScreen import ConfirmedOrderScreen

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
                print("Order submitted successfully!") # TODO: Replace with proper screen message
                self.db.update_quantities(items) # Update the inventory in the database
                print("Inventory updated successfully!")
            else:
                print("Items not available")
                # Show a warning screen if items are not available
                warning_screen = WarningScreen(self.root, "Some of the items are not available! Please check your order.")
                warning_screen.show_warning()
        else:
            # Show a warning screen if the information is not valid
            warning_screen = WarningScreen(self.root, "Please fill in all fields.")
            warning_screen.show_warning()
            print("Warning: Please fill in all fields.")

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
        exists = self.db.query_order(customer_id)
        if exists is not None:
            print("Order exists")
            # Retrieve the order details
        else:
            print("Order does not exist")
