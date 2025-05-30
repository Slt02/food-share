class Donation:
    def __init__ (self, donor_id, donation_date, donation_info):
        self.donor_id = donor_id
        self.donation_date = donation_date
        self.donation_info = donation_info
        
        self.donations = []
