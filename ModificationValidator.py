import re
from Database import Database


class ModificationValidator:
    """
    Controller class for validating and processing inventory modifications.
    Handles validation of item data and database updates for the FoodShare inventory system.
    """
    
    def __init__(self):
        self.db = Database()
        
        # Define valid categories based on your database
        self.valid_categories = ['Chips', 'fumar', 'vegetables', 'fruits', 'dairy', 'meat', 'beverages', 'sweet',]
        
        # Validation rules
        self.MIN_ITEM_NAME_LENGTH = 2
        self.MAX_ITEM_NAME_LENGTH = 100
        self.MIN_DESCRIPTION_LENGTH = 5
        self.MAX_DESCRIPTION_LENGTH = 500
        self.MIN_QUANTITY = 0
        self.MAX_QUANTITY = 10000
    
    def validate_item_name(self, item_name):
        """
        Validates the item name.
        
        Args:
            item_name (str): The name of the item
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not item_name or not isinstance(item_name, str):
            return False, "Item name is required and must be a string"
        
        item_name = item_name.strip()
        
        if len(item_name) < self.MIN_ITEM_NAME_LENGTH:
            return False, f"Item name must be at least {self.MIN_ITEM_NAME_LENGTH} characters long"
        
        if len(item_name) > self.MAX_ITEM_NAME_LENGTH:
            return False, f"Item name must not exceed {self.MAX_ITEM_NAME_LENGTH} characters"
        
        # Check if item name contains only valid characters (letters, numbers, spaces, hyphens)
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', item_name):
            return False, "Item name can only contain letters, numbers, spaces, and hyphens"
        
        return True, None
    
    def validate_description(self, description):
        """
        Validates the item description.
        
        Args:
            description (str): The description of the item
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not description or not isinstance(description, str):
            return False, "Description is required and must be a string"
        
        description = description.strip()
        
        if len(description) < self.MIN_DESCRIPTION_LENGTH:
            return False, f"Description must be at least {self.MIN_DESCRIPTION_LENGTH} characters long"
        
        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            return False, f"Description must not exceed {self.MAX_DESCRIPTION_LENGTH} characters"
        
        return True, None
    
    def validate_category(self, category):
        """
        Validates the item category.
        
        Args:
            category (str): The category of the item
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not category or not isinstance(category, str):
            return False, "Category is required and must be a string"
        
        category = category.strip().lower()
        
        if category not in [cat.lower() for cat in self.valid_categories]:
            return False, f"Invalid category. Valid categories are: {', '.join(self.valid_categories)}"
        
        return True, None
    
    def validate_quantity(self, quantity):
        """
        Validates the item quantity (in numbers, not kg).
        
        Args:
            quantity: The quantity of the item
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return False, "Quantity must be a valid integer number"
        
        if quantity < self.MIN_QUANTITY:
            return False, f"Quantity cannot be negative (minimum: {self.MIN_QUANTITY})"
        
        if quantity > self.MAX_QUANTITY:
            return False, f"Quantity cannot exceed {self.MAX_QUANTITY}"
        
        return True, None
    
    def validate_modifications(self, item_name, description, category, quantity):
        """
        Validates all modifications for an inventory item.
        
        Args:
            item_name (str): The name of the item
            description (str): The description of the item
            category (str): The category of the item
            quantity: The quantity of the item
            
        Returns:
            tuple: (is_valid, error_messages)
        """
        errors = []
        
        # Validate item name
        is_valid, error = self.validate_item_name(item_name)
        if not is_valid:
            errors.append(f"Item Name: {error}")
        
        # Validate description
        is_valid, error = self.validate_description(description)
        if not is_valid:
            errors.append(f"Description: {error}")
        
        # Validate category
        is_valid, error = self.validate_category(category)
        if not is_valid:
            errors.append(f"Category: {error}")
        
        # Validate quantity
        is_valid, error = self.validate_quantity(quantity)
        if not is_valid:
            errors.append(f"Quantity: {error}")
        
        if errors:
            return False, errors
        
        return True, None
    
    def check_item_exists(self, item_name):
        """
        Checks if an item already exists in the inventory.
        
        Args:
            item_name (str): The name of the item to check
            
        Returns:
            bool: True if item exists, False otherwise
        """
        try:
            query = "SELECT COUNT(*) FROM inventory WHERE item_name = %s"
            result = self.db.execute_query(query, (item_name.strip(),))
            
            if result and result[0][0] > 0:
                return True
            return False
            
        except Exception as e:
            print(f"Error checking item existence: {e}")
            return False
    
    def add_item(self, item_name, description, category, quantity):
        """
        Adds a new item to the inventory after validation.
        
        Args:
            item_name (str): The name of the item
            description (str): The description of the item
            category (str): The category of the item
            quantity: The quantity of the item
            
        Returns:
            tuple: (success, message)
        """
        # Validate modifications
        is_valid, errors = self.validate_modifications(item_name, description, category, quantity)
        
        if not is_valid:
            return False, f"Validation failed: {'; '.join(errors)}"
        
        # Clean input data
        item_name = item_name.strip()
        description = description.strip()
        category = category.strip()
        quantity = int(quantity)
        
        # Check if item already exists
        if self.check_item_exists(item_name):
            return False, f"Item '{item_name}' already exists in inventory"
        
        try:
            # Insert new item into inventory
            query = "INSERT INTO inventory (item_name, description, category, quantity) VALUES (%s, %s, %s, %s)"
            params = (item_name, description, category, quantity)
            self.db.execute_query(query, params)
            self.db.connection.commit()
            
            return True, f"Item '{item_name}' added successfully to inventory"
            
        except Exception as e:
            self.db.connection.rollback()
            return False, f"Database error while adding item: {str(e)}"
    
    def update_item(self, item_name, new_description=None, new_category=None, new_quantity=None):
        """
        Updates an existing item in the inventory after validation.
        
        Args:
            item_name (str): The name of the item to update
            new_description (str, optional): New description
            new_category (str, optional): New category
            new_quantity (optional): New quantity
            
        Returns:
            tuple: (success, message)
        """
        # Check if item exists
        if not self.check_item_exists(item_name):
            return False, f"Item '{item_name}' does not exist in inventory"
        
        # Build update query dynamically based on provided parameters
        update_fields = []
        params = []
        errors = []
        
        if new_description is not None:
            is_valid, error = self.validate_description(new_description)
            if is_valid:
                update_fields.append("description = %s")
                params.append(new_description.strip())
            else:
                errors.append(f"Description: {error}")
        
        if new_category is not None:
            is_valid, error = self.validate_category(new_category)
            if is_valid:
                update_fields.append("category = %s")
                params.append(new_category.strip())
            else:
                errors.append(f"Category: {error}")
        
        if new_quantity is not None:
            is_valid, error = self.validate_quantity(new_quantity)
            if is_valid:
                update_fields.append("quantity = %s")
                params.append(int(new_quantity))
            else:
                errors.append(f"Quantity: {error}")
        
        # Check if there are validation errors
        if errors:
            return False, f"Validation failed: {'; '.join(errors)}"
        
        # Check if there are any fields to update
        if not update_fields:
            return False, "No modifications provided"
        
        try:
            # Build and execute update query
            query = f"UPDATE inventory SET {', '.join(update_fields)} WHERE item_name = %s"
            params.append(item_name.strip())
            
            self.db.execute_query(query, tuple(params))
            self.db.connection.commit()
            
            return True, f"Item '{item_name}' updated successfully"
            
        except Exception as e:
            self.db.connection.rollback()
            return False, f"Database error while updating item: {str(e)}"
    
    def update_quantity(self, item_name, new_quantity):
        """
        Convenience method to update only the quantity of an item.
        
        Args:
            item_name (str): The name of the item
            new_quantity: The new quantity
            
        Returns:
            tuple: (success, message)
        """
        return self.update_item(item_name, new_quantity=new_quantity)
    
    def get_item_details(self, item_name):
        """
        Retrieves details of a specific item from inventory.
        
        Args:
            item_name (str): The name of the item
            
        Returns:
            dict or None: Item details if found, None otherwise
        """
        try:
            query = "SELECT item_name, description, category, quantity FROM inventory WHERE item_name = %s"
            result = self.db.execute_query(query, (item_name.strip(),))
            
            if result:
                return {
                    'item_name': result[0][0],
                    'description': result[0][1],
                    'category': result[0][2],
                    'quantity': result[0][3]
                }
            return None
            
        except Exception as e:
            print(f"Error retrieving item details: {e}")
            return None
    
    def close(self):
        """
        Closes the database connection.
        """
        if self.db:
            self.db.close()


# Example usage
if __name__ == "__main__":
    # Create validator instance
    validator = ModificationValidator()
    
    # Example 1: Add a new item
    success, message = validator.add_item(
        item_name="Apples",
        description="Fresh red apples from local farms",
        category="fruits",
        quantity=50
    )
    print(f"Add item: {message}")
    
    # Example 2: Update an existing item's quantity
    success, message = validator.update_quantity("Apples", 75)
    print(f"Update quantity: {message}")
    
    # Example 3: Update multiple fields
    success, message = validator.update_item(
        item_name="Apples",
        new_description="Organic red apples from certified farms",
        new_category="fruits",
        new_quantity=100
    )
    print(f"Update item: {message}")
    
    # Example 4: Try to add an invalid item
    success, message = validator.add_item(
        item_name="A",  # Too short
        description="Test",  # Too short
        category="invalid_category",  # Invalid category
        quantity=-5  # Negative quantity
    )
    print(f"Invalid add: {message}")
    
    # Close database connection
    validator.close()