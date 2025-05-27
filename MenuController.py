from Database import Database


class MenuController:
    
    def __init__(self):
        self.database = Database()
    
    def check_availability(self):
        """Check inventory table for available items and return the data"""
        try:
            # Query to get all items from inventory table
            query = "SELECT item_name, quantity FROM inventory WHERE quantity > 0"
            available_items = self.database.execute_query(query)
            
            if available_items:
                print("Available items found:")
                for item in available_items:
                    item_name, quantity = item
                    print(f"- {item_name}: {quantity} available")
                return available_items
            else:
                print("No items currently available in inventory.")
                return []
                
        except Exception as e:
            print(f"Error checking inventory availability: {e}")
            return []
    
    def get_all_inventory_items(self):
        """Get all items from inventory table regardless of availability"""
        try:
            query = "SELECT item_name, quantity FROM inventory"
            all_items = self.database.execute_query(query)
            
            if all_items:
                return all_items
            else:
                print("No items found in inventory table.")
                return []
                
        except Exception as e:
            print(f"Error retrieving inventory items: {e}")
            return []
    
    def get_item_quantity(self, item_name):
        """Get the quantity of a specific item from inventory"""
        try:
            query = "SELECT quantity FROM inventory WHERE item_name = %s"
            result = self.database.execute_query(query, (item_name,))
            
            if result:
                return result[0][0]  # Return the quantity
            else:
                print(f"Item '{item_name}' not found in inventory.")
                return 0
                
        except Exception as e:
            print(f"Error getting item quantity: {e}")
            return 0
    
    def is_item_available(self, item_name, requested_quantity=1):
        """Check if a specific item is available in the requested quantity"""
        try:
            available_quantity = self.get_item_quantity(item_name)
            
            if available_quantity >= requested_quantity:
                print(f"✓ {item_name} is available (Requested: {requested_quantity}, Available: {available_quantity})")
                return True
            else:
                print(f"✗ {item_name} is not available in requested quantity (Requested: {requested_quantity}, Available: {available_quantity})")
                return False
                
        except Exception as e:
            print(f"Error checking item availability: {e}")
            return False
    
    def get_item_details(self, item_name):
        """Get detailed information about a specific item from inventory (category, description)"""
        try:
            query = "SELECT item_name, category, description FROM inventory WHERE item_name = %s"
            result = self.database.execute_query(query, (item_name,))
            
            if result:
                item_name, category, description = result[0]
                return {
                    'item_name': item_name,
                    'category': category,
                    'description': description
                }
            else:
                print(f"Item '{item_name}' not found in inventory.")
                return None
                
        except Exception as e:
            print(f"Error getting item details: {e}")
            return None
    
    def show_menu(self):
        """Display the menu with available items from inventory"""
        available_items = self.check_availability()
        
        if available_items:
            print("\n" + "="*50)
            print("           FOOD SHARE MENU")
            print("="*50)
            
            for i, item in enumerate(available_items, 1):
                item_name, quantity = item
                print(f"{i}. {item_name}")  # Quantity hidden from user
            
            print("="*50)
            return available_items
        else:
            print("\nNo items currently available.")
            return []