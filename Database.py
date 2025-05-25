import mysql.connector
from FoodRequest import FoodRequest


class Database:
    _connection = None # Class variable to hold the single instance so only one connection is created each time
    # Constructor to initialize the database connection
    def __init__(self, host="localhost", user="root", password="", database="foodshare"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        if Database._connection is None: # Check if a connection already exists
            Database._connection = self.connect()
        
        self.connection = Database._connection # Use the existing connection
        self.cursor = self.connection.cursor() # Create a cursor object to interact with the database

    # Create a new connection to the database
    def connect(self): 
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

   # Close the connection to the database 
    def close(self):
        self.cursor.close()
        self.connection.close()

    # Execute a query on the database
    def execute_query(self, query, params=None): 
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    
    # Check if the items are available in the database
    def check_availability(self, items):
        # Check for every item in the dictionary if it is available in the database
        for item in items:
            print(f"Checking availability for {item}")
            print(f"Quanity: {items[item]}")
            # Query to check if the item is available in the database
            query = "SELECT quantity FROM inventory WHERE item_name = %s"
            params = (item,)
            result = self.execute_query(query, params)

            # If the query is successful, check the available quantity
            if result:
                available_quantity = result[0][0]
                print(f"Available quantity for {item}: {available_quantity}")
                if available_quantity < items[item]: # If the available quantity is less than the requested quantity
                    print(f"Not enough {item} available. Available: {available_quantity}, Requested: {items[item]}")
                    return False
                else:
                    print(f"{item} is available!") 
            else:
                return False # Item not found in inventory
        print("All items are available!")
        return True # All items are available

    # Save the order to the database
    def save_order(self, food_request):
        # Save the order to the database
        query = "INSERT INTO food_requests (customer_id, delivery_address, number_of_people, status) VALUES (%s, %s, %s, %s)"
        params = (food_request.customer_id, food_request.delivery_address, food_request.number_of_people, food_request.status)
        self.execute_query(query, params)
        self.connection.commit() # Commit the changes to the database

        # Get the order ID of the newly created order
        order_id = self.cursor.lastrowid

        #  Save the items in the order to the database
        for item, quantity in food_request.items.items():
            query = "INSERT INTO food_request_items (request_id, item_name, quantity) VALUES (%s, %s, %s)"
            params = (order_id, item, quantity)
            self.execute_query(query, params)

        self.connection.commit() # Commit the changes to the database
        print(f"Order {order_id} saved successfully!")

    # Update the quantities of the items in the database
    def update_quantities(self, items):
        # Update the quantities of the items in the database
        for item, quantity in items.items():
            query = "UPDATE inventory SET quantity = quantity - %s WHERE item_name = %s"
            params = (quantity, item)
            self.execute_query(query, params)

        self.connection.commit()

    # Check if the order exists in the database
    def query_order(self, customer_id):
        # Get the pending orders from the database for the customer
        query = "SELECT * FROM food_requests WHERE customer_id = %s AND status != 'delivered'"
        params = (customer_id,)
        order_data = self.execute_query(query, params)
        
        if not order_data: # If no pending orders are found
            return None

        # Get the order details from the database
        query = "SELECT item_name, quantity FROM food_request_items WHERE request_id = %s"
        params = (order_data[0][0],)
        items_data = self.execute_query(query, params)

        # Hold items to return them
        items = {}
        for item in items_data:
            items[item[0]] = item[1]

        # Create a food request object to return
        food_request = FoodRequest(
            customer_id=order_data[0][1],
            delivery_address=order_data[0][2],
            number_of_people=order_data[0][3],
            items=items,
            status=order_data[0][4],
        )

        return food_request # Return the food request object
    
    # Query the order history for a customer
    def query_order_history(self, customer_id):

        # Get the order history from the database for the customer
        query = "SELECT * FROM food_requests WHERE customer_id = %s and status = 'delivered'"
        # Query to get all orders for a specific customer
        params = (customer_id,)
        order_data = self.execute_query(query, params)

        if not order_data:  # If no orders are found
            return None

        # Get the order details from the database
        order_history = []
        for order in order_data:
            request_id, customer_id, delivery_address, number_of_people, status, created_at = order

            # Get the items for each order
            items_query = "SELECT item_name, quantity FROM food_request_items WHERE request_id = %s"
            items_results = self.execute_query(items_query, (request_id,))
            items = {item: quantity for item, quantity in items_results}

            # Append the order to the history
            food_request = FoodRequest(
                request_id=request_id,
                customer_id=customer_id,
                delivery_address=delivery_address,
                number_of_people=number_of_people,
                items=items,
                status=status,
                made=created_at
            )

            order_history.append(food_request)

        # Return the list of food requests
        return order_history  # Return the list of food requests
    
        # NEW METHOD: Get user by email for login functionality
    
    # Save the report in the database
    def create_report(self, report):
        query = "INSERT INTO reports (request_id, customer_id, description) VALUES (%s, %s, %s)"
        params = (report.request_id, report.customer_id, report.description)
        self.execute_query(query, params)
        self.connection.commit()  # Commit the changes to the database

    # Get user by email for login functionality
    def get_user_by_email(self, email):
        """
        Retrieves user data by email for login authentication.
        Returns user data as dictionary or None if not found.
        """
        try:
            query = "SELECT id, name, surname, email, password, phone, role FROM users WHERE email = %s"
            result = self.execute_query(query, (email,))
            
            if result:
                user_data = {
                    'id': result[0][0],
                    'name': result[0][1],
                    'surname': result[0][2],
                    'email': result[0][3],
                    'password': result[0][4],
                    'phone': result[0][5],
                    'role': result[0][6]
                }
                return user_data
            else:
                return None
                
        except mysql.connector.Error as err:
            print(f"Database error in get_user_by_email: {err}")
            return None
    
    # Get user by ID
    def get_user_by_id(self, user_id):
        """
        Retrieves user data by user ID.
        Returns user data as dictionary or None if not found.
        """
        try:
            query = "SELECT id, name, surname, email, phone, role FROM users WHERE id = %s"
            result = self.execute_query(query, (user_id,))
            
            if result:
                user_data = {
                    'id': result[0][0],
                    'name': result[0][1],
                    'surname': result[0][2],
                    'email': result[0][3],
                    'phone': result[0][4],
                    'role': result[0][5]
                }
                return user_data
            else:
                return None
                
        except mysql.connector.Error as err:
            print(f"Database error in get_user_by_id: {err}")
            return None
    
    # Check if email exists
    def email_exists(self, email):
        """
        Checks if an email already exists in the database.
        Returns True if exists, False otherwise.
        """
        try:
            query = "SELECT COUNT(*) FROM users WHERE email = %s"
            result = self.execute_query(query, (email,))
            
            if result and result[0][0] > 0:
                return True
            return False
                
        except mysql.connector.Error as err:
            print(f"Database error in email_exists: {err}")
            return False
    
    # Update account information
    def update_account_info(self, user_id, updated_info, credential_controller):
        """Updates user information and returns success status"""
        try:
            # Remove empty fields from updates
            filtered_updates = {k: v for k, v in updated_info.items() if v.strip()}
            
            if not filtered_updates:
                return False, "No updates provided."
            
            # Basic validation for email, password, and phone if they're being updated
            if "email" in filtered_updates and not credential_controller.validate_email(filtered_updates["email"]):
                return False, "Invalid email format."
            
            if "password" in filtered_updates:
                is_strong, message = credential_controller.validate_password_strength(filtered_updates["password"])
                if not is_strong:
                    return False, message
            
            if "phone" in filtered_updates and not credential_controller.validate_phone(filtered_updates["phone"]):
                return False, "Phone number must be exactly 10 digits."
            
            # Select fields that exist in the database
            fields_to_select = ['name', 'surname', 'email', 'password', 'phone', 'role']
            current_query = f"SELECT {', '.join(fields_to_select)} FROM users WHERE id = %s"
            result = self.execute_query(current_query, (user_id,))

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
            self.execute_query(query, tuple(values))
            self.connection.commit()
            
            return True, "User info updated successfully."
            
        except Exception as e:
            return False, f"Database error: {str(e)}"

    # DONATION METHODS - ADDED FOR DONATION FUNCTIONALITY

    def create_donations_table(self):
        """Create donations table if it doesn't exist"""
        try:
            query = """
                CREATE TABLE IF NOT EXISTS donations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    donor_id VARCHAR(100) NOT NULL,
                    item_name VARCHAR(200) NOT NULL,
                    quantity INT NOT NULL,
                    donation_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (donor_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """
            self.execute_query(query)
            self.connection.commit()
            print("Donations table created/verified successfully!")
            
        except mysql.connector.Error as err:
            print(f"Error creating donations table: {err}")

    def create_donation(self, donor_id, item_name, quantity, donation_date):
        """Create a new donation record"""
        try:
            query = "INSERT INTO donations (donor_id, item_name, quantity, donation_date) VALUES (%s, %s, %s, %s)"
            params = (donor_id, item_name, quantity, donation_date)
            self.execute_query(query, params)
            self.connection.commit()
            
            # Get the donation ID of the newly created donation
            donation_id = self.cursor.lastrowid
            print(f"Donation {donation_id} created successfully!")
            return donation_id
            
        except mysql.connector.Error as err:
            print(f"Error creating donation: {err}")
            return None

    def get_donation_by_id(self, donation_id):
        """Get a specific donation by ID"""
        try:
            query = "SELECT id, donor_id, item_name, quantity, donation_date, created_at FROM donations WHERE id = %s"
            result = self.execute_query(query, (donation_id,))
            
            if result:
                donation_data = {
                    'id': result[0][0],
                    'donor_id': result[0][1],
                    'item_name': result[0][2],
                    'quantity': result[0][3],
                    'donation_date': str(result[0][4]),
                    'created_at': str(result[0][5])
                }
                return donation_data
            else:
                return None
                
        except mysql.connector.Error as err:
            print(f"Database error in get_donation_by_id: {err}")
            return None

    def get_donations_by_donor(self, donor_id):
        """Get all donations for a specific donor"""
        try:
            query = "SELECT id, donor_id, item_name, quantity, donation_date, created_at FROM donations WHERE donor_id = %s ORDER BY created_at DESC"
            result = self.execute_query(query, (donor_id,))
            
            donations = []
            if result:
                for row in result:
                    donation_data = {
                        'id': row[0],
                        'donor_id': row[1],
                        'item_name': row[2],
                        'quantity': row[3],
                        'donation_date': str(row[4]),
                        'created_at': str(row[5])
                    }
                    donations.append(donation_data)
            
            return donations
            
        except mysql.connector.Error as err:
            print(f"Database error in get_donations_by_donor: {err}")
            return []

    def get_all_donations(self):
        """Get all donations"""
        try:
            query = "SELECT id, donor_id, item_name, quantity, donation_date, created_at FROM donations ORDER BY created_at DESC"
            result = self.execute_query(query)
            
            donations = []
            if result:
                for row in result:
                    donation_data = {
                        'id': row[0],
                        'donor_id': row[1],
                        'item_name': row[2],
                        'quantity': row[3],
                        'donation_date': str(row[4]),
                        'created_at': str(row[5])
                    }
                    donations.append(donation_data)
            
            return donations
            
        except mysql.connector.Error as err:
            print(f"Database error in get_all_donations: {err}")
            return []