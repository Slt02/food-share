from User import User

class Donor(User): 
    def __init__(self, donor_id, username, name, surname, password, email, phone_number):
        super.__init__(self, donor_id, username, name, surname, password, email)
        self.phone_number = phone_number
        self.donation_history = [] # List to store donation history
    