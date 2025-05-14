class Donation:
    def __init__ (self, donation_id, donor_id, donation_date, donation_info):
        self.donation_id = donation_id
        self.donor_id = donor_id
        self.donation_date = donation_date
        self.donation_info = donation_info
        
        self.donation_history = []
