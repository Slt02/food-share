import re
from Database import Database



class CredentialController:
    def __init__(self):
        self.Database = Database() 

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
            user_data = self.Database.get_user_by_email(email)
            
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
    
    def register(self, name, surname, email, password, phone, role):
        """
        Registers a new user and creates appropriate Customer/Donor object.
        Returns (success, message, user_object) tuple.
        """
        try:
            # Validate name fields
            name_valid, name_msg = self.validate_name_field(name)
            if not name_valid:
                return False, f"First name error: {name_msg}", None
            
            surname_valid, surname_msg = self.validate_name_field(surname)
            if not surname_valid:
                return False, f"Last name error: {surname_msg}", None
            
            # Validate email format
            if not self.validate_email(email):
                return False, "Invalid email format.", None
            
            # Check if email already exists
            existing_user = self.Database.get_user_by_email(email)
            if existing_user is not None:
                return False, "An account with this email already exists.", None
            
            # Validate password strength
            password_valid, password_msg = self.validate_password_strength(password)
            if not password_valid:
                return False, password_msg, None
            
            # Validate phone number
            if not self.validate_phone(phone):
                return False, "Phone number must be exactly 10 digits.", None
            
            # Validate role
            valid_roles = ['customer', 'donor', 'admin', 'dropoffagent']
            if role not in valid_roles:
                return False, "Invalid role specified.", None
            
            # Generate username from email (before @ symbol)
            username = email.split('@')[0]
            
            # Create the appropriate object based on role
            if role == 'customer':
                # Import Customer class
                from Users.Customer import Customer
                
                # Create Customer object
                customer_obj = Customer(
                    username=username,
                    name=name.strip(),
                    surname=surname.strip(),
                    password=password,
                    email=email.strip().lower(),
                    phone_number=phone.strip(),
                    customer_id=None  # Will be set after database insertion
                )
                
                # Store customer in database
                user_id = self.Database.create_customer_user(customer_obj)
                
                if user_id:
                    customer_obj.user_id = user_id  # Set the ID returned from database
                    return True, f"Welcome to FoodShare! Your customer account has been created successfully.", customer_obj
                else:
                    return False, "Failed to create customer account. Please try again.", None
                    
            elif role == 'donor':
                # Import Donor class
                from Users.Donor import Donor
                
                # Create Donor object
                donor_obj = Donor(
                    username=username,
                    name=name.strip(),
                    surname=surname.strip(),
                    password=password,
                    email=email.strip().lower(),
                    phone_number=phone.strip(),
                    donor_id=None  # Will be set after database insertion
                )
                
                # Store donor in database
                user_id = self.Database.create_donor_user(donor_obj)
                
                if user_id:
                    donor_obj.user_id = user_id  # Set the ID returned from database
                    return True, f"Welcome to FoodShare! Your donor account has been created successfully.", donor_obj
                else:
                    return False, "Failed to create donor account. Please try again.", None
            
            else:
                # For admin and dropoffagent, create basic user record for now
                # You can extend this later if you have Admin/DropoffAgent classes
                user_data = {
                    'name': name.strip(),
                    'surname': surname.strip(),
                    'username': username,
                    'email': email.strip().lower(),
                    'password': password,
                    'phone': phone.strip(),
                    'role': role
                }
                
                user_id = self.Database.create_user(user_data)
                
                if user_id:
                    safe_user_data = {k: v for k, v in user_data.items() if k != 'password'}
                    safe_user_data['id'] = user_id
                    return True, f"Welcome to FoodShare! Your {role} account has been created successfully.", safe_user_data
                else:
                    return False, "Failed to create account. Please try again.", None
                    
        except Exception as e:
            print(f"Registration error: {e}")
            return False, "Registration failed due to system error.", None

    def open_user_main_screen(self, user_data):
        
        role = user_data['role']
        
        try:
            if role == 'admin':
                from GUI.MainScreenAdmin import MainScreenAdmin
                # MainScreenAdmin expects: (root=None, user_data=None)
                screen = MainScreenAdmin(root=None, user_data=user_data)
                screen.display()
                
            elif role == 'customer':
                from GUI.MainScreenCustomer import CustomerMainScreen
                # FIXED: CustomerMainScreen expects customer_id, but we need to pass user_data
                # We'll create a wrapper to handle this inconsistency
                screen = CustomerMainScreen(root=None, customer_id=user_data.get('id'))
                # Store user_data as an attribute for consistency
                screen.user_data = user_data
                screen.user_id = user_data.get('id')
                screen.display()
                
            elif role == 'donor':
                from GUI.MainScreenDonor import MainScreenDonor
                # MainScreenDonor expects: (user_data=None)
                screen = MainScreenDonor(user_data=user_data)
                screen.display()
                
            elif role == 'dropoffagent':
                from GUI.MainScreenDropoffAgent import MainScreenDropoffAgent
                # MainScreenDropoffAgent expects: (user_data=None)
                screen = MainScreenDropoffAgent(user_data=user_data)
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
    
    
    def validate_email(self, email):
        """Checks if the email format is valid."""
        if not email or not email.strip():
            return False
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(email_regex, email.strip()) is not None

    def validate_password_strength(self, password):
        """Checks if password is strong (length, uppercase, number, symbol)."""
        if not password:
            return False, "Password cannot be empty."
        if len(password) < 8:
            return False, "Password must be at least 8 characters."
        if not re.search(r'[A-Z]', password):
            return False, "Password must include at least one uppercase letter."
        if not re.search(r'[0-9]', password):
            return False, "Password must include at least one number."
        if not re.search(r'[\W_]', password):
            return False, "Password must include at least one special character."

        return True, "Password is strong."

    def validate_credentials(self, email, password, phone=None):
        """Validates credentials with simple checks."""
        if not self.validate_email(email):
            print("Invalid email format.")
            return False

        strong, message = self.validate_password_strength(password)
        if not strong:
            print(f"Password error: {message}")
            return False

        if phone is not None:
            if not self.validate_phone(phone):
                print("Phone number must be exactly 10 digits.")
                return False

        print("Email, password, and phone format are valid.")
        return True

    def validate_phone(self, phone):
        """Validates phone number format (must be exactly 10 digits)"""
        if not phone or not phone.strip():
            return False  # Phone is required
        
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it's exactly 10 digits
        if len(digits_only) != 10:
            return False
        
        return True
    
    def validate_name_field(self, name):
        """Validates name fields (name, surname, username)"""
        if not name or not name.strip():
            return False, "Field cannot be empty."
        
        if len(name.strip()) < 2:
            return False, "Field must be at least 2 characters long."
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name.strip()):
            return False, "Field can only contain letters, spaces, hyphens, and apostrophes."
        
        return True, "Valid."
    
    def update(self, user_id, updated_info):
        """Updates user information using the database method"""
        return self.Database.update_account_info(user_id, updated_info, self)

    def update_name(self, user_id, new_name):
        return self.update(user_id, {"name": new_name})

    def update_surname(self, user_id, new_surname):
        return self.update(user_id, {"surname": new_surname})

    def update_username(self, user_id, new_username):
        return self.update(user_id, {"username": new_username})

    def update_email(self, user_id, new_email):
        """Updates user's email after validating format."""
        if not self.validate_email(new_email):
            return False, "Invalid email format."
        return self.update(user_id, {"email": new_email})