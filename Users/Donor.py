from Users.User import User

class Donor(User): 
    def __init__(self, username, name, surname, password, email, phone_number, donor_id=None):
        super().__init__(donor_id, username, name, surname, password, email)
        self.phone_number = phone_number
        self.donation_history = [] # List to store donation history
    