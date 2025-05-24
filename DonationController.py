from merkdb import Database

class DonationController:
    def __init__(self):
        self.merkdb = Database()

    def check_donation_details(self, item_name, quantity):
        """Ensure donation details are valid before proceeding."""
        if not item_name or quantity <= 0:
            print("Invalid donation details: Item name must not be empty and quantity must be greater than zero.")
            return False
        
        print(f"Donation details checked: Item = {item_name}, Quantity = {quantity}")
        return True

    def validate_donation(self, item_name, quantity):
        """Perform final validation on the donation details."""
        if not self.check_donation_details(item_name, quantity):
            print("Validation failed due to incorrect donation details.")
            return False
        
        print("Donation details validated successfully.")
        return True

    def create_donation(self, donor_id, item_name, quantity, donation_date):
        """Ensure donation details are validated before inserting a new record."""
        if not self.validate_donation(item_name, quantity):
            return False

        query = """
        INSERT INTO donations (donor_id, item_name, quantity, donation_date)
        VALUES (%s, %s, %s, %s)
        """
        params = (donor_id, item_name, quantity, donation_date)

        try:
            self.db.execute_query(query, params)
            self.db.connection.commit()
            print("Donation successfully recorded.")
            return True
        except Exception as e:
            print(f"Error while processing donation: {e}")
            return False
