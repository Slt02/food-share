from datetime import datetime
from typing import Dict, Any, List, Optional
from Database import Database

class DonationController:
    def __init__(self, host="localhost", user="root", password="", database="foodshare"):
        self.db = Database(host, user, password, database)
        # Create donations table if it doesn't exist
        self.db.create_donations_table()
    
    def check_details(self, donation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check item name and quantity only
        """
        errors = []
        
        # Check item name
        if 'item_name' not in donation_data or not donation_data['item_name']:
            errors.append("Item name is required")
        
        # Check quantity
        if 'quantity' not in donation_data or not donation_data['quantity']:
            errors.append("Quantity is required")
        else:
            try:
                quantity = int(donation_data['quantity'])
                if quantity <= 0:
                    errors.append("Quantity must be a positive number")
            except (ValueError, TypeError):
                errors.append("Quantity must be a valid number")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def validate_donation(self, donation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the donation
        """
        # First check details
        check_result = self.check_details(donation_data)
        
        if not check_result['valid']:
            return check_result
        
        # Validation passed
        return {
            'valid': True,
            'errors': []
        }
    
    def creating_donation(self, donation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create the donation in the database using Database class
        """
        try:
            # Add default values for required fields if not provided
            if 'donor_id' not in donation_data:
                donation_data['donor_id'] = 'ANONYMOUS'
            if 'donation_date' not in donation_data:
                donation_data['donation_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Use Database class method to create donation
            donation_id = self.db.create_donation(
                donor_id=donation_data['donor_id'],
                item_name=donation_data['item_name'],
                quantity=int(donation_data['quantity']),
                donation_date=donation_data['donation_date']
            )
            
            if donation_id:
                # Get the created donation using Database class method
                created_donation = self.db.get_donation_by_id(donation_id)
                
                return {
                    'success': True,
                    'donation': created_donation,
                    'message': f"Donation registered successfully with ID: {donation_id}"
                }
            else:
                return {
                    'success': False,
                    'error': 'Database error',
                    'message': "Failed to create donation"
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': "Failed to create donation"
            }
    
    def display(self) -> Dict[str, Any]:
        """Get all donations for display using Database class"""
        donations = self.db.get_all_donations()
        return {
            'total_donations': len(donations),
            'donations': donations
        }
    
    def close(self):
        """Close database connection"""
        if hasattr(self.db, 'close'):
            self.db.close()