import uuid
import datetime

class FoodRequest:
   def __init__(self, request_id, customer_id, delivery_address, items = None):
    #self.request_id = str(uuid.uuid4())
    self.request_id = request_id
    self.customer_id = customer_id
    self.delivery_address = delivery_address
    self.items = items
    self.made = datetime.datetime.now()
    self.status = "Pending"