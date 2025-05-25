from User import User

class Customer(User):
    def __init__(self, customer_id, username, name, surname, password, email, phone_number):
        super.__init__(customer_id, username, name, surname, password, email)
        self.phone_number = phone_number
        self.order_history = []