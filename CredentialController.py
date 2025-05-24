import re
from Database import Database


class CredentialController:
    def __init__(self):
        self.Database = Database() # Create a new instance of the Database class 

    
    def login(self, email, password):
        """
        Authenticates user credentials against the database.
        Returns (success, message, user_data) tuple.
        """
        # First validate email format
        if not self.validate_email(email):
            return False, "Invalid email format.", None
        
        # Check if password is provided
        if not password or password.strip() == "":
            return False, "Password cannot be empty.", None
        
        try:
            # Query database to find user with matching email
            user_data = self.Database.get_user_by_email(email) # CHANGE DB EVERY TIME!!!!
            
            if user_data is None:
                return False, "Invalid email or password.", None
            
            # Check if the password matches (assuming password is stored in user_data)
            # Note: In production, you should use hashed passwords!
            if user_data.get('password') == password:
                # Remove password from user_data before returning for security
                safe_user_data = {k: v for k, v in user_data.items() if k != 'password'}
                return True, "Login successful.", safe_user_data
            else:
                return False, "Invalid email or password.", None
                
        except Exception as e:
            print(f"Database error during login: {e}")
            return False, "Login failed due to system error.", None
    
    
    def open_user_main_screen(self, user_data):
        """
        Opens the appropriate main screen based on user role.
        """
        role = user_data['role']
        
        try:
            if role == 'admin':
                # Import inside the method to avoid circular imports
                from GUI.MainScreenAdmin import MainScreenAdmin
                screen = MainScreenAdmin(user_data)  # Pass user_data
                screen.display()
                
            elif role == 'customer':
                # Import inside the method to avoid circular imports
                from GUI.MainScreenCustomer import CustomerMainScreen
                screen = CustomerMainScreen(user_data)  # Pass user_data
                screen.display()
                
            elif role == 'donor':
                # Import inside the method to avoid circular imports
                from GUI.MainScreenDonor import MainScreenDonor
                screen = MainScreenDonor(user_data)  # Pass user_data
                screen.display()
                
            elif role == 'dropoffagent':
                # Import inside the method to avoid circular imports
                from GUI.MainScreenDropoffAgent import MainScreenDropoffAgent
                screen = MainScreenDropoffAgent(user_data)  # Pass user_data
                screen.display()
                
            else:
                print(f"Unknown role: {role}")
                return False
                
            return True
            
        except ImportError as e:
            print(f"Error importing screen for role {role}: {e}")
            print("Make sure the main screen files are in the correct location")
            return False
        except Exception as e:
            print(f"Error opening screen for role {role}: {e}")
            return False
    
    
    def get_user_dashboard_route(self, user_role):
        """
        Returns the appropriate dashboard route based on user role.
        """
        dashboard_routes = {
            'admin': 'admin_dashboard',
            'customer': 'customer_main_screen',
            'donor': 'donor_dashboard',
            'dropoffagent': 'agent_dashboard'
        }
        
        return dashboard_routes.get(user_role, 'customer_main_screen')  # Default to customer
    
    
    def check_user_permissions(self, user_role, required_permission):
        """
        Checks if user has permission to access certain features.
        """
        permissions = {
            'admin': ['manage_users', 'view_all_orders', 'manage_inventory', 'view_reports'],
            'customer': ['place_order', 'view_own_orders', 'update_profile'],
            'donor': ['donate_food', 'view_own_donations', 'update_profile'],
            'dropoffagent': ['manage_deliveries', 'view_assigned_orders', 'update_profile']
        }
        
        user_permissions = permissions.get(user_role, [])
        return required_permission in user_permissions
    
    
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
        """Validates name fields (name, surname, username)"""
        if not name.strip():
            return False, "Field cannot be empty."
        
        if len(name.strip()) < 2:
            return False, "Field must be at least 2 characters long."
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name.strip()):
            return False, "Field can only contain letters, spaces, hyphens, and apostrophes."
        
        return True, "Valid."
    
    
    
    def update(self, user_id, updated_info):
        """Updates user information using the database method"""
        return self.Database.update_account_info(user_id, updated_info, self) # change DB EVERY TIME!!!!!

        
    def update_name(self, user_id, new_name):
        return self.update(user_id, {"name": new_name})

    def update_surname(self, user_id, new_surname):
        return self.update(user_id, {"surname": new_surname})

    def update_username(self, user_id, new_username):
        return self.update(user_id, {"username": new_username})

    def update_email(self, user_id, new_email):
        
        #Updates user's email after validating format.
        
        if not self.validate_email(new_email):
            return False, "Invalid email format."
        return self.update(user_id, {"email": new_email})

    