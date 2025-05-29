from Database import Database

class OrderStatusController:
    def __init__(self):
        self.db = Database()
    
    def clicksMonitorDeliveries(self):
        """
        Handler for when the user clicks to monitor deliveries.
        Triggers the request to check for orders with pending deliveries.
        """
        return self.requestOrdersWithPendingDeliveries()
    
    def requestOrdersWithPendingDeliveries(self):
        """
        Requests all orders from the database where delivery_status is 'Not Delivered/Pending'.
        Returns a list of orders or None if no pending deliveries found.
        """
        try:
            # Query to get all orders with delivery_status = 'Not Delivered/Pending'
            query = """
                SELECT id, customer_id, delivery_address, number_of_people, 
                       status, delivery_status, created_at 
                FROM food_requests 
                WHERE delivery_status = 'Not Delivered/Pending'
                ORDER BY created_at DESC
            """
            
            results = self.db.execute_query(query)
            
            if not results:
                return None  # No pending deliveries found
            
            # Convert results to list of dictionaries for easier handling
            orders_with_pending_deliveries = []
            for row in results:
                order = {
                    'id': row[0],
                    'customer_id': row[1],
                    'delivery_address': row[2],
                    'number_of_people': row[3],
                    'status': row[4],
                    'delivery_status': row[5],
                    'created_at': row[6]
                }
                orders_with_pending_deliveries.append(order)
            
            return orders_with_pending_deliveries
            
        except Exception as e:
            print(f"Error retrieving orders with pending deliveries: {e}")
            return None
    
    def showOrdersWithPendingDeliveries(self, orders):
        """
        This method will be called to display the orders.
        For now, it just returns the orders list.
        The actual UI implementation will be done later.
        
        Args:
            orders: List of orders with pending deliveries
        
        Returns:
            The orders list (to be used by the UI later)
        """
        return orders
    
    def showOrderStatus(self, order_id):
        """
        Shows the status of a specific order.
        This will be implemented with the UI later.
        
        Args:
            order_id: ID of the order to check
        
        Returns:
            Order details including delivery status
        """
        try:
            query = """
                SELECT id, customer_id, delivery_address, number_of_people, 
                       status, delivery_status, created_at 
                FROM food_requests 
                WHERE id = %s
            """
            
            result = self.db.execute_query(query, (order_id,))
            
            if result:
                row = result[0]
                order = {
                    'id': row[0],
                    'customer_id': row[1],
                    'delivery_address': row[2],
                    'number_of_people': row[3],
                    'status': row[4],
                    'delivery_status': row[5],
                    'created_at': row[6]
                }
                return order
            else:
                return None
                
        except Exception as e:
            print(f"Error retrieving order status: {e}")
            return None
    
    def checkOrdersWithPendingDeliveries(self):
        """
        Main method to check for orders with pending deliveries.
        Returns True if there are pending deliveries, False otherwise.
        This can be used for the warning popup logic.
        """
        orders = self.requestOrdersWithPendingDeliveries()
        return orders is not None and len(orders) > 0
    
    def getPendingDeliveriesCount(self):
        """
        Returns the count of orders with pending deliveries.
        Useful for displaying in UI or notifications.
        """
        try:
            query = """
                SELECT COUNT(*) 
                FROM food_requests 
                WHERE delivery_status = 'Not Delivered/Pending'
            """
            
            result = self.db.execute_query(query)
            
            if result:
                return result[0][0]
            else:
                return 0
                
        except Exception as e:
            print(f"Error counting pending deliveries: {e}")
            return 0
    
    def close(self):
        """
        Close the database connection when done.
        """
        if self.db:
            self.db.close()


# Example usage (for testing purposes)
if __name__ == "__main__":
    controller = OrderStatusController()
    
    # Check if there are orders with pending deliveries
    if controller.checkOrdersWithPendingDeliveries():
        print("Found orders with pending deliveries!")
        orders = controller.requestOrdersWithPendingDeliveries()
        print(f"Number of pending deliveries: {len(orders)}")
        
        # Display order details
        for order in orders:
            print(f"Order ID: {order['id']}, Customer: {order['customer_id']}, "
                  f"Delivery Status: {order['delivery_status']}")
    else:
        print("No orders with pending deliveries found.")
        # This is where you would show the warning popup
    
    controller.close()