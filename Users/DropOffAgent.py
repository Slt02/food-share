from User import User

# Child class of User Class
class DropOffAgent(User):
    def __init__(self, dropOff_id, username, name, surname, email, password, phone_number):
        super().__init__(self, dropOff_id, username, name, surname, email, password)
        self.phone_number = phone_number
        self.deliveries_taken = [] # List of deliveries taken by the agent