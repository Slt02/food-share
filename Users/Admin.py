from User import User

class Admin(User):
    def __init__(self, admin_id, username, name, surname, password, email):
        super().__init__(admin_id, username, name, surname, password, email)

    def create_drop_off_acc(self):
        # TO-DO Function to create a new drop off agent
        pass