class Delivery:
    def __init__ (self, order_id, Drop_off_Agent_id, customer_id, customer_address):
        self.order_id = order_id
        self.Drop_off_Agent_id = Drop_off_Agent_id
        self.customer_id = customer_id
        self.customer_address = customer_address
        self.items = []
    