from User import User

class Admin(User):
    def __init__(self, admin_id, username, name, surname, password, email):
        super().__init__(admin_id, username, name, surname, password, email)