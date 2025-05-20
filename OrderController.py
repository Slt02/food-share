from Database import Database
from FoodRequest import FoodRequest

class OrderController:
    def __init__(self):
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
                print("Order submitted successfully!") # TODO: Replace with proper screen message
                self.db.update_quantities(items) # Update the inventory in the database
                print("Inventory updated successfully!")
            else:
                print("Items not available")
                # TODO: Replace with proper screen message

    # Validate the information provided by the customer (missing fields, etc.)
    def validate_info(self, numberOfPpl, delivery_address, items):
        # Validate the information provided by the customer
        if not numberOfPpl or not delivery_address or not items:
            print("Missing information") # TODO: Replace with proper screen message
            return False
        return True

# test case
if __name__ == "__main__":
    order_controller = OrderController()
    order_controller.submit_order(2, 3, "123 Main St", {"chips": 5})
    # Add more test cases as needed