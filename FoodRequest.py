import uuid
import datetime

class FoodRequest:
   def __init__(self, customer_id, delivery_address, number_of_people, items = None):
    self.customer_id = customer_id
    self.delivery_address = delivery_address
    self.number_of_people = number_of_people
    self.items = items
    self.made = datetime.datetime.now()
    self.status = "Pending"