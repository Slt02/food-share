from Users.User import User

# Child class of User Class
class DropOffAgent(User):
    def __init__(self, username, name, surname, password, email, phone_number):
        super().__init__(username, name, surname, password, email, phone_number)
        self.deliveries_taken = [] # List of deliveries taken by the agent