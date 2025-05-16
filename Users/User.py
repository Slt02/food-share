# User Class that represents the parent class for all types of users
class User:
    def __init__(self, username, name, surname, password, email, phone_number):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.is_logged_in = False