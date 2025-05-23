import mysql.connector

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
        query = "INSERT INTO food_requests (customer_id, delivery_address, number_of_people, status, created_at) VALUES (%s, %s, %s, %s, %s)"
        params = (food_request.customer_id, food_request.delivery_address, food_request.number_of_people, food_request.status, food_request.made)
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
            print(f"No pending order found for customer {customer_id}")
            return None

        # Get the order details from the database
        query = "SELECT item_name, quantity FROM food_request_items WHERE request_id = %s"
        params = (order_data[0][0],)
        items_data = self.execute_query(query, params)
        print(f"Order data: {order_data}")
        print(f"Items data: {items_data}")

        return order_data, items_data # Return the order data and items data