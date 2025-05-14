import uuid
import datetime

class FoodRequest:
 def __init__(self, user_id, delivery_address, items = None):
    self.request_id = str(uuid.uuid4())
    self.user_id = user_id
    self.items = items
    self.delivery_address = delivery_address
    self.made = datetime.datetime.now()
    self.status = "Pending"

