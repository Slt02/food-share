from Users.User import User

# Child class of User Class
class DropOffAgent(User):
    def __init__(self, username, name, surname, email, password, phone_number, dropOff_id= None):
        super().__init__(dropOff_id, username, name, surname, password, email)
        self.phone_number = phone_number
        self.deliveries_taken = [] # List of deliveries taken by the agent