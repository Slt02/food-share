class Donor: 
    def __init__(self, Donor_id, name, email, phone_number, donation_info):
         self.Donor_id = Donor_id
         self.name = name
         self.email = email
         self.phone_number = phone_number
         self.donation_info = donation_info

         self.donation_history = []
    