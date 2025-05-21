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

    
    
    
    def validate_credentials(self, email, password):
        
        #Validates credentials with simple checks.
        if not self.validate_email(email):
            print("Invalid email format.")
            return False

        strong, message = self.validate_password_strength(password)
        if not strong:
            print(f"Password error: {message}")
            return False

        print("Email and password format are valid.")
        return True

    
    
    
    
    
    
    def update(self, user_id, updated_info):
        
        #Only updates changed fields. Skips update if no change.
        
        current_query = "SELECT email, phone FROM users WHERE id = %s"
        result = self.diondb.execute_query(current_query, (user_id,))

        if not result:
            print("User not found.")
            return

        current_data = dict(zip(["email", "phone"], result[0]))
        changed_fields = {k: v for k, v in updated_info.items() if current_data.get(k) != v}

        if not changed_fields:
            print("No changes detected. Nothing to update.")
            return

        update_clauses = []
        values = []

        for key, value in changed_fields.items():
            update_clauses.append(f"{key} = %s")
            values.append(value)

        values.append(user_id)

        query = f"UPDATE users SET {', '.join(update_clauses)} WHERE id = %s"
        self.diondb.execute_query(query, tuple(values))
        self.diondb.connection.commit()
        print("User info updated successfully.")
        
    def update_name(self, user_id, new_name):
        self.update(user_id, {"name": new_name})

    def update_surname(self, user_id, new_surname):
        self.update(user_id, {"surname": new_surname})

    def update_nickname(self, user_id, new_nickname):
        self.update(user_id, {"nickname": new_nickname})

controller = CredentialController()

""""
def test_valid_credentials():
    controller = CredentialController()
    
    email = "user@example.com"
    password = "Ssssssss!"

    result = controller.validate_credentials(email, password)
    

    

# Run the test
test_valid_credentials()
"""

def test_update_email_for_emily():
    controller = CredentialController()

    user_id = 7  # Change this if Emily has a different ID in your database
    new_email = "emily.newstone@example.com"

    # Validate the new email format before updating
    if controller.validate_email(new_email):
        controller.update(user_id, {"email": new_email})
    else:
        print("New email format is invalid.")

# Run the test
test_update_email_for_emily()

