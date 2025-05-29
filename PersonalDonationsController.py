from Database import Database


class PersonalDonationsController:
    """Controller to manage personal donation tracking for donors"""
    
    def __init__(self):
        try:
            self.database = Database()
            print("DEBUG: Database connection established successfully")
        except Exception as e:
            print(f"DEBUG: Failed to establish database connection: {e}")
            self.database = None
    
    def find_personal_donations(self, donor_id):
        """Find all donations made by the logged-in donor using their ID from login session"""
        print(f"DEBUG: Starting find_personal_donations for donor_id: {donor_id}")
        print(f"DEBUG: donor_id type: {type(donor_id)}, value: '{donor_id}'")
        
        if not self.database:
            print("DEBUG: No database connection available")
            return []
            
        try:
            # Convert donor_id to int to ensure proper matching with database
            try:
                donor_id_int = int(donor_id)
                print(f"DEBUG: Converted donor_id to int: {donor_id_int}")
            except (ValueError, TypeError):
                print(f"DEBUG: Could not convert donor_id to int, using as-is: {donor_id}")
                donor_id_int = donor_id
            
            query = """
                SELECT d.id, d.item_name, d.quantity, d.donation_date
                FROM donations d 
                WHERE d.donor_id = %s 
                ORDER BY d.donation_date DESC
            """
            print(f"DEBUG: Executing query: {query}")
            print(f"DEBUG: With parameter: {donor_id_int}")
            
            donations = self.database.execute_query(query, (donor_id_int,))
            print(f"DEBUG: Query returned: {donations}")
            print(f"DEBUG: Type of result: {type(donations)}")
            print(f"DEBUG: Number of results: {len(donations) if donations else 0}")
            
            if donations:
                print(f"Found {len(donations)} donations for logged-in donor (ID: {donor_id_int})")
                for i, donation in enumerate(donations):
                    donation_id, item_name, quantity, date = donation
                    print(f"- Donation {i+1}: ID {donation_id} - {item_name} ({quantity}) - Date: {date}")
                return donations
            else:
                print(f"No past donations found for logged-in donor (ID: {donor_id_int})")
                print("DEBUG: Checking if any donations exist in table...")
                
                # Debug: Check if ANY donations exist
                check_query = "SELECT COUNT(*) FROM donations"
                total_donations = self.database.execute_query(check_query)
                print(f"DEBUG: Total donations in table: {total_donations[0][0] if total_donations else 0}")
                
                # Debug: Check what donor_ids exist
                donor_query = "SELECT DISTINCT donor_id FROM donations LIMIT 10"
                existing_donors = self.database.execute_query(donor_query)
                print(f"DEBUG: Existing donor_ids: {existing_donors}")
                
                return []
                
        except Exception as e:
            print(f"ERROR: Exception in find_personal_donations for donor {donor_id}: {e}")
            print(f"ERROR: Exception type: {type(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_donation_details(self, donation_id):
        """Get detailed information about a specific donation"""
        try:
            query = """
                SELECT d.id, d.item_name, d.quantity, d.donation_date,
                       u.first_name, u.last_name
                FROM donations d
                JOIN users u ON d.donor_id = u.user_id
                WHERE d.id = %s
            """
            result = self.database.execute_query(query, (donation_id,))
            
            if result:
                donation_data = result[0]
                donation_details = {
                    'donation_id': donation_data[0],
                    'item_name': donation_data[1],
                    'quantity': donation_data[2],
                    'donation_date': donation_data[3],
                    'pickup_location': None,  # Not in table
                    'description': None,      # Not in table
                    'expiry_date': None,      # Not in table
                    'donor_name': f"{donation_data[4]} {donation_data[5]}"
                }
                print(f"Retrieved details for donation ID: {donation_id}")
                return donation_details
            else:
                print(f"Donation ID {donation_id} not found")
                return None
                
        except Exception as e:
            print(f"Error getting donation details: {e}")
            return None

    def close(self):
        """Close database connection"""
        if hasattr(self.database, 'close'):
            self.database.close()