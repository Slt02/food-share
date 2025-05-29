from Database import Database
from FoodRequest import FoodRequest
import tkinter as tk
from tkinter import messagebox


class PendingOrdersController:
    def __init__(self):
        """Initialize the PendingOrdersController with database connection"""
        self.db = Database()
        self.pending_orders = []
    
    def get_all_pending_orders(self):
        """
        Retrieve all pending orders from the database.
        Returns a list of FoodRequest objects with status 'Pending'
        """
        try:
            # Query to get all pending food requests
            query = """
                SELECT id, customer_id, delivery_address, number_of_people, status, created_at 
                FROM food_requests 
                WHERE status = 'Pending'
                ORDER BY created_at DESC
            """
            
            orders_data = self.db.execute_query(query)
            
            if not orders_data:
                return []
            
            # Clear previous pending orders
            self.pending_orders = []
            
            # Process each pending order
            for order in orders_data:
                request_id, customer_id, delivery_address, number_of_people, status, created_at = order
                
                # Get items for this order
                items_query = "SELECT item_name, quantity FROM food_request_items WHERE request_id = %s"
                items_data = self.db.execute_query(items_query, (request_id,))
                
                # Convert items to dictionary
                items = {}
                if items_data:
                    for item_name, quantity in items_data:
                        items[item_name] = quantity
                
                # Get customer information
                customer_info = self.db.get_user_by_id(customer_id)
                
                # Create FoodRequest object with additional customer info
                food_request = FoodRequest(
                    request_id=request_id,
                    customer_id=customer_id,
                    delivery_address=delivery_address,
                    number_of_people=number_of_people,
                    items=items,
                    status=status,
                    made=created_at
                )
                
                # Add customer info as attributes for display purposes
                if customer_info:
                    food_request.customer_name = f"{customer_info['name']} {customer_info['surname']}"
                    food_request.customer_email = customer_info['email']
                    food_request.customer_phone = customer_info['phone']
                else:
                    food_request.customer_name = "Unknown Customer"
                    food_request.customer_email = ""
                    food_request.customer_phone = ""
                
                self.pending_orders.append(food_request)
            
            return self.pending_orders
            
        except Exception as e:
            print(f"Error retrieving pending orders: {e}")
            return []
    
    def check_pending_orders(self):
        """
        Check if there are any pending orders.
        Shows appropriate UI based on whether orders exist.
        """
        pending_orders = self.get_all_pending_orders()
        
        if pending_orders:
            # Return True and the list of pending orders for the UI to display
            print(f"Found {len(pending_orders)} pending orders")
            return True, pending_orders
        else:
            # Show warning popup if no pending orders
            self.show_no_pending_orders_warning()
            return False, []
    
    def show_no_pending_orders_warning(self):
        """Display a warning popup when no pending orders are found"""
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        messagebox.showwarning(
            "No Pending Orders",
            "There are currently no pending orders to process."
        )
        
        root.destroy()
    
    def get_pending_orders_count(self):
        """Get the count of pending orders"""
        try:
            query = "SELECT COUNT(*) FROM food_requests WHERE status = 'Pending'"
            result = self.db.execute_query(query)
            
            if result:
                return result[0][0]
            return 0
            
        except Exception as e:
            print(f"Error counting pending orders: {e}")
            return 0
    
    def update_order_status(self, request_id, new_status):
        """
        Update the status of a food request
        
        Args:
            request_id: The ID of the food request
            new_status: The new status (e.g., 'Processing', 'Ready', 'Delivered')
        """
        try:
            query = "UPDATE food_requests SET status = %s WHERE id = %s"
            params = (new_status, request_id)
            self.db.execute_query(query, params)
            self.db.connection.commit()
            
            print(f"Order {request_id} status updated to {new_status}")
            return True
            
        except Exception as e:
            print(f"Error updating order status: {e}")
            return False
    
    def get_pending_orders_by_filter(self, filter_type=None, filter_value=None):
        """
        Get pending orders with optional filtering
        
        Args:
            filter_type: Type of filter ('customer', 'date', 'address')
            filter_value: Value to filter by
        """
        try:
            base_query = """
                SELECT id, customer_id, delivery_address, number_of_people, status, created_at 
                FROM food_requests 
                WHERE status = 'Pending'
            """
            
            params = []
            
            if filter_type == 'customer' and filter_value:
                base_query += " AND customer_id = %s"
                params.append(filter_value)
            elif filter_type == 'date' and filter_value:
                base_query += " AND DATE(created_at) = %s"
                params.append(filter_value)
            elif filter_type == 'address' and filter_value:
                base_query += " AND delivery_address LIKE %s"
                params.append(f"%{filter_value}%")
            
            base_query += " ORDER BY created_at DESC"
            
            if params:
                orders_data = self.db.execute_query(base_query, tuple(params))
            else:
                orders_data = self.db.execute_query(base_query)
            
            return self._process_orders_data(orders_data)
            
        except Exception as e:
            print(f"Error filtering pending orders: {e}")
            return []
    
    def process_orders_data(self, orders_data):
        """Helper method to process raw order data into FoodRequest objects"""
        if not orders_data:
            return []
        
        processed_orders = []
        
        for order in orders_data:
            request_id, customer_id, delivery_address, number_of_people, status, created_at = order
            
            # Get items for this order
            items_query = "SELECT item_name, quantity FROM food_request_items WHERE request_id = %s"
            items_data = self.db.execute_query(items_query, (request_id,))
            
            items = {}
            if items_data:
                for item_name, quantity in items_data:
                    items[item_name] = quantity
            
            # Get customer information
            customer_info = self.db.get_user_by_id(customer_id)
            
            # Create FoodRequest object
            food_request = FoodRequest(
                request_id=request_id,
                customer_id=customer_id,
                delivery_address=delivery_address,
                number_of_people=number_of_people,
                items=items,
                status=status,
                made=created_at
            )
            
            # Add customer info
            if customer_info:
                food_request.customer_name = f"{customer_info['name']} {customer_info['surname']}"
                food_request.customer_email = customer_info['email']
                food_request.customer_phone = customer_info['phone']
            else:
                food_request.customer_name = "Unknown Customer"
                food_request.customer_email = ""
                food_request.customer_phone = ""
            
            processed_orders.append(food_request)
        
        return processed_orders
    
    def close(self):
        """Close the database connection"""
        if self.db:
            self.db.close()


# Example usage:
if __name__ == "__main__":
    # Create controller instance
    controller = PendingOrdersController()
    
    # Check for pending orders
    has_orders, orders = controller.check_pending_orders()
    
    if has_orders:
        print("\n=== PENDING ORDERS ===")
        for order in orders:
            print(f"\nOrder ID: {order.request_id}")
            print(f"Customer: {order.customer_name} (ID: {order.customer_id})")
            print(f"Delivery Address: {order.delivery_address}")
            print(f"Number of People: {order.number_of_people}")
            print(f"Items:")
            for item, quantity in order.items.items():
                print(f"  - {item}: {quantity}")
            print(f"Created at: {order.made}")
            print("-" * 40)
    
    # Example of updating order status
    # if orders:
    #     controller.update_order_status(orders[0].request_id, 'Processing')
    
    # Close connection when done
    controller.close_connection()