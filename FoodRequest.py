import uuid
import datetime

class FoodRequest:
   def __init__(self, customer_id, delivery_address, number_of_people, request_id = None, items = None, made = None ,status = "pending"):
      self.customer_id = customer_id
      self.delivery_address = delivery_address
      self.number_of_people = number_of_people
      self.request_id = request_id
      self.items = items
      self.status = status
      self.made = made