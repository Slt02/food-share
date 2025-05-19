class OrderController:
    
    def submit_order(self, customer_id, delivery_address, items):
        if(self.validate_info(customer_id, delivery_address, items)):
            pass

    def validate_info(self, customer_id, delivery_address, items):
        # Validate the information provided by the customer
        if not customer_id or not delivery_address or not items:
            return False
        else: # Show a warning screen to the user that the information is not valid
            pass
        return True