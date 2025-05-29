from Users.User import User

class Admin(User):
    def __init__(self, username, name, surname, password, email, admin_id=None):
        super().__init__(admin_id, username, name, surname, password, email)

    