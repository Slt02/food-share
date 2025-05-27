from Database import Database


class PersonalDonationsController:
    """Controller to manage personal donation tracking for donors"""
    
    def __init__(self):
        self.database = Database()
    
    def find_personal_donations(self, donor_id):
        """Find all donations made by the logged-in donor using their ID from login session"""
        try:
            query = """
                SELECT d.donation_id, d.item_name, d.quantity, d.donation_date, 
                       d.status, d.pickup_location, d.description
                FROM donations d 
                WHERE d.donor_id = %s 
                ORDER BY d.donation_date DESC
            """
            donations = self.database.execute_query(query, (donor_id,))
            
            if donations:
                print(f"Found {len(donations)} donations for logged-in donor (ID: {donor_id})")
                for donation in donations:
                    donation_id, item_name, quantity, date, status, location, desc = donation
                    print(f"- {item_name} ({quantity}) - Status: {status} - Date: {date}")
                return donations
            else:
                print(f"No past donations found for logged-in donor (ID: {donor_id})")
                return []
                
        except Exception as e:
            print(f"Error finding personal donations for donor {donor_id}: {e}")
            return []
    
    def get_donation_details(self, donation_id):
        """Get detailed information about a specific donation"""
        try:
            query = """
                SELECT d.donation_id, d.item_name, d.quantity, d.donation_date,
                       d.status, d.pickup_location, d.description, d.expiry_date,
                       u.first_name, u.last_name
                FROM donations d
                JOIN users u ON d.donor_id = u.user_id
                WHERE d.donation_id = %s
            """
            result = self.database.execute_query(query, (donation_id,))
            
            if result:
                donation_data = result[0]
                donation_details = {
                    'donation_id': donation_data[0],
                    'item_name': donation_data[1],
                    'quantity': donation_data[2],
                    'donation_date': donation_data[3],
                    'status': donation_data[4],
                    'pickup_location': donation_data[5],
                    'description': donation_data[6],
                    'expiry_date': donation_data[7],
                    'donor_name': f"{donation_data[8]} {donation_data[9]}"
                }
                print(f"Retrieved details for donation ID: {donation_id}")
                return donation_details
            else:
                print(f"Donation ID {donation_id} not found")
                return None
                
        except Exception as e:
            print(f"Error getting donation details: {e}")
            return None
    
    def get_donation_status_summary(self, donor_id):
        """Get summary of donation statuses for a donor"""
        try:
            query = """
                SELECT status, COUNT(*) as count
                FROM donations 
                WHERE donor_id = %s 
                GROUP BY status
            """
            result = self.database.execute_query(query, (donor_id,))
            
            if result:
                status_summary = {}
                for status, count in result:
                    status_summary[status] = count
                return status_summary
            else:
                return {}
                
        except Exception as e:
            print(f"Error getting donation status summary: {e}")
            return {}
    
    def update_donation_status(self, donation_id, new_status):
        """Update the status of a donation (for admin use)"""
        try:
            query = "UPDATE donations SET status = %s WHERE donation_id = %s"
            self.database.execute_update(query, (new_status, donation_id))
            print(f"Updated donation {donation_id} status to: {new_status}")
            return True
            
        except Exception as e:
            print(f"Error updating donation status: {e}")
            return False
    
    def get_recent_donations(self, donor_id, limit=5):
        """Get the most recent donations by a donor"""
        try:
            query = """
                SELECT donation_id, item_name, quantity, donation_date, status
                FROM donations 
                WHERE donor_id = %s 
                ORDER BY donation_date DESC 
                LIMIT %s
            """
            result = self.database.execute_query(query, (donor_id, limit))
            
            if result:
                return result
            else:
                return []
                
        except Exception as e:
            print(f"Error getting recent donations: {e}")
            return []
    
    def count_total_donations(self, donor_id):
        """Count total number of donations made by a donor"""
        try:
            query = "SELECT COUNT(*) FROM donations WHERE donor_id = %s"
            result = self.database.execute_query(query, (donor_id,))
            
            if result:
                return result[0][0]
            else:
                return 0
                
        except Exception as e:
            print(f"Error counting donations: {e}")
            return 0