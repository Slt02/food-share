# User Class that represents the parent class for all types of users
class User:
    def __init__(self, user_id, username, name, surname, password, email):  
        self.user_id = user_id
        self.username = username
        self.name = name
        self.surname = surname
        self.__password = password
        self.email = email
        self.is_logged_in = False

    def get_password(self): # Password getter
        return self.__password
    
    def __str__(self):
        return f"User ID: {self.user_id}, Username: {self.username}, Name: {self.name}, Surname: {self.surname}, Email: {self.email}"