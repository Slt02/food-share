import re
from diondb import Database


class CredentialController:
    def __init__(self):
        self.diondb = Database() # Create a new instance of the Database class 

    
    
    
    def validate_email(self, email):
        
       # Checks if the email format is valid.
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(email_regex, email) is not None

    
    
    
    def validate_password_strength(self, password):
        
        #Checks if password is strong (length, uppercase, number, symbol).
        if len(password) < 8:
            return False, "Password must be at least 8 characters."
        if not re.search(r'[A-Z]', password):
            return False, "Password must include at least one uppercase letter."
        if not re.search(r'[0-9]', password):
            return False, "Password must include at least one number."
        if not re.search(r'[\W_]', password):
            return False, "Password must include at least one symbol."

        return True, "Password is strong."

    
    
    
    def validate_credentials(self, email, password, phone=None):
        
        #Validates credentials with simple checks.
        if not self.validate_email(email):
            print("Invalid email format.")
            return False

        strong, message = self.validate_password_strength(password)
        if not strong:
            print(f"Password error: {message}")
            return False

        if phone is not None:
            valid_phone, phone_message = self.validate_phone_format(phone)
            if not valid_phone:
                print(f"Phone error: {phone_message}")
                return False

        print("Email, password, and phone format are valid.")
        return True

    
    
    


    def validate_phone(self, phone):
        """Validates phone number format (must be exactly 10 digits)"""
        if not phone.strip():
            return True  # Allow empty phone numbers
        
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it's exactly 10 digits
        if len(digits_only) != 10:
            return False
        
        return True
    
    
    def validate_name_field(self, name):
        """Validates name fields (name, surname, nickname)"""
        if not name.strip():
            return False, "Field cannot be empty."
        
        if len(name.strip()) < 2:
            return False, "Field must be at least 2 characters long."
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name.strip()):
            return False, "Field can only contain letters, spaces, hyphens, and apostrophes."
        
        return True, "Valid."
    
    
    
    def update(self, user_id, updated_info):
        """Updates user information and returns success status"""
        try:
            # Remove empty fields from updates
            filtered_updates = {k: v for k, v in updated_info.items() if v.strip()}
            
            if not filtered_updates:
                return False, "No updates provided."
            
            # Basic validation for email, password, and phone if they're being updated
            if "email" in filtered_updates and not self.validate_email(filtered_updates["email"]):
                return False, "Invalid email format."
            
            if "password" in filtered_updates:
                is_strong, message = self.validate_password_strength(filtered_updates["password"])
                if not is_strong:
                    return False, message
            
            if "phone" in filtered_updates and not self.validate_phone(filtered_updates["phone"]):
                return False, "Phone number must be exactly 10 digits."
            
            # Select all relevant fields for comparison
            fields_to_select = ['name', 'surname', 'nickname', 'email', 'password', 'phone', 'address']
            current_query = f"SELECT {', '.join(fields_to_select)} FROM users WHERE id = %s"
            result = self.diondb.execute_query(current_query, (user_id,))

            if not result:
                return False, "User not found."

            current_data = dict(zip(fields_to_select, result[0]))
            changed_fields = {k: v for k, v in filtered_updates.items() if current_data.get(k) != v}

            if not changed_fields:
                return False, "No changes detected."

            update_clauses = []
            values = []

            for key, value in changed_fields.items():
                update_clauses.append(f"{key} = %s")
                values.append(value)

            values.append(user_id)

            query = f"UPDATE users SET {', '.join(update_clauses)} WHERE id = %s"
            self.diondb.execute_query(query, tuple(values))
            self.diondb.connection.commit()
            
            return True, "User info updated successfully."
            
        except Exception as e:
            return False, f"Database error: {str(e)}"

        
    def update_name(self, user_id, new_name):
        return self.update(user_id, {"name": new_name})

    def update_surname(self, user_id, new_surname):
        return self.update(user_id, {"surname": new_surname})

    def update_nickname(self, user_id, new_nickname):
        return self.update(user_id, {"nickname": new_nickname})

    def update_email(self, user_id, new_email):
        
        #Updates user's email after validating format.
        
        if not self.validate_email(new_email):
            return False, "Invalid email format."
        return self.update(user_id, {"email": new_email})

    def update_address(self, user_id, new_address):
        
        #Updates user's delivery address.
        
        return self.update(user_id, {"address": new_address})