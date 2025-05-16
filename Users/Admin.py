from Users.User import User

class Admin(User):
    def __init__(self, username, name, surname, password, email, phone_number):
        super().__init__(username, name, surname, password, email, phone_number)