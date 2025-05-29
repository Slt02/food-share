from Users.User import User

class Customer(User):
    def __init__(self, username, name, surname, password, email, phone_number, customer_id=None):
        super().__init__(customer_id, username, name, surname, password, email)
        self.phone_number = phone_number
        