from Database import Database
from datetime import datetime
import json


class InventoryDetailController:
    """
    Controller class for managing inventory details by food categories.
    Provides detailed information about items in each category.
    """
    
    def __init__(self):
        self.db = Database()
    
    def get_all_categories(self):
        """
        Retrieves all unique categories from the inventory.
        
        Returns:
            list: List of unique category names
        """
        try:
            query = "SELECT DISTINCT category FROM inventory ORDER BY category"
            results = self.db.execute_query(query)
            
            if results:
                categories = [row[0] for row in results if row[0] is not None]
                return categories
            return []
            
        except Exception as e:
            print(f"Error retrieving categories: {e}")
            return []
    
    def get_category_details(self, category):
        """
        Gets detailed information about a specific category.
        
        Args:
            category (str): The category name
            
        Returns:
            dict: Category details including item count, total quantity, and items
        """
        try:
            # Get all items in the category
            query = """
                SELECT item_name, description, quantity 
                FROM inventory 
                WHERE category = %s 
                ORDER BY item_name
            """
            results = self.db.execute_query(query, (category,))
            
            if not results:
                return {
                    'category': category,
                    'item_count': 0,
                    'total_quantity': 0,
                    'items': [],
                    'status': 'empty'
                }
            
            # Process results
            items = []
            total_quantity = 0
            
            for row in results:
                item = {
                    'name': row[0],
                    'description': row[1],
                    'quantity': row[2],
                    'status': self._get_quantity_status(row[2])
                }
                items.append(item)
                total_quantity += row[2]
            
            return {
                'category': category,
                'item_count': len(items),
                'total_quantity': total_quantity,
                'average_quantity': total_quantity // len(items) if items else 0,
                'items': items,
                'status': 'active'
            }
            
        except Exception as e:
            print(f"Error getting category details: {e}")
            return None
    
    def get_items_by_category(self, category):
        """
        Gets all items in a specific category.
        
        Args:
            category (str): The category name
            
        Returns:
            list: List of items in the category
        """
        try:
            query = """
                SELECT item_name, description, quantity 
                FROM inventory 
                WHERE category = %s 
                ORDER BY quantity DESC, item_name
            """
            results = self.db.execute_query(query, (category,))
            
            items = []
            if results:
                for row in results:
                    items.append({
                        'item_name': row[0],
                        'description': row[1],
                        'quantity': row[2],
                        'status': self._get_quantity_status(row[2])
                    })
            
            return items
            
        except Exception as e:
            print(f"Error getting items by category: {e}")
            return []
    
    def get_category_statistics(self, category):
        """
        Gets statistical information about a category.
        
        Args:
            category (str): The category name
            
        Returns:
            dict: Statistics including min, max, average quantities
        """
        try:
            query = """
                SELECT 
                    COUNT(*) as item_count,
                    SUM(quantity) as total_quantity,
                    AVG(quantity) as avg_quantity,
                    MIN(quantity) as min_quantity,
                    MAX(quantity) as max_quantity
                FROM inventory 
                WHERE category = %s
            """
            result = self.db.execute_query(query, (category,))
            
            if result and result[0][0] > 0:
                return {
                    'category': category,
                    'item_count': result[0][0],
                    'total_quantity': result[0][1] or 0,
                    'average_quantity': float(result[0][2] or 0),
                    'min_quantity': result[0][3] or 0,
                    'max_quantity': result[0][4] or 0,
                    'inventory_health': self._calculate_inventory_health(result[0][2], result[0][3])
                }
            else:
                return {
                    'category': category,
                    'item_count': 0,
                    'total_quantity': 0,
                    'average_quantity': 0,
                    'min_quantity': 0,
                    'max_quantity': 0,
                    'inventory_health': 'No items'
                }
                
        except Exception as e:
            print(f"Error getting category statistics: {e}")
            return None
    
    def get_low_stock_items_by_category(self, category, threshold=10):
        """
        Gets items with low stock in a specific category.
        
        Args:
            category (str): The category name
            threshold (int): Quantity threshold for low stock
            
        Returns:
            list: List of low stock items
        """
        try:
            query = """
                SELECT item_name, quantity 
                FROM inventory 
                WHERE category = %s AND quantity <= %s
                ORDER BY quantity ASC
            """
            results = self.db.execute_query(query, (category, threshold))
            
            low_stock_items = []
            if results:
                for row in results:
                    low_stock_items.append({
                        'item_name': row[0],
                        'quantity': row[1],
                        'status': 'critical' if row[1] <= 5 else 'low'
                    })
            
            return low_stock_items
            
        except Exception as e:
            print(f"Error getting low stock items: {e}")
            return []
    
    def get_all_categories_summary(self):
        """
        Gets a summary of all categories in the inventory.
        
        Returns:
            list: List of category summaries
        """
        try:
            query = """
                SELECT 
                    category,
                    COUNT(*) as item_count,
                    SUM(quantity) as total_quantity,
                    AVG(quantity) as avg_quantity
                FROM inventory 
                GROUP BY category
                ORDER BY category
            """
            results = self.db.execute_query(query)
            
            summaries = []
            if results:
                for row in results:
                    summaries.append({
                        'category': row[0],
                        'item_count': row[1],
                        'total_quantity': row[2] or 0,
                        'average_quantity': float(row[3] or 0),
                        'health': self._calculate_inventory_health(row[3], None)
                    })
            
            return summaries
            
        except Exception as e:
            print(f"Error getting categories summary: {e}")
            return []
    
    def search_items_in_category(self, category, search_term):
        """
        Searches for items within a specific category.
        
        Args:
            category (str): The category name
            search_term (str): Term to search for in item names or descriptions
            
        Returns:
            list: List of matching items
        """
        try:
            search_pattern = f"%{search_term}%"
            query = """
                SELECT item_name, description, quantity 
                FROM inventory 
                WHERE category = %s 
                AND (item_name LIKE %s OR description LIKE %s)
                ORDER BY item_name
            """
            results = self.db.execute_query(query, (category, search_pattern, search_pattern))
            
            items = []
            if results:
                for row in results:
                    items.append({
                        'item_name': row[0],
                        'description': row[1],
                        'quantity': row[2],
                        'status': self._get_quantity_status(row[2])
                    })
            
            return items
            
        except Exception as e:
            print(f"Error searching items: {e}")
            return []
    
    def get_category_report(self, category):
        """
        Generates a comprehensive report for a category.
        
        Args:
            category (str): The category name
            
        Returns:
            dict: Comprehensive category report
        """
        try:
            # Get basic details
            details = self.get_category_details(category)
            if not details:
                return None
            
            # Get statistics
            stats = self.get_category_statistics(category)
            
            # Get low stock items
            low_stock = self.get_low_stock_items_by_category(category)
            
            # Build report
            report = {
                'category': category,
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'summary': {
                    'total_items': details['item_count'],
                    'total_quantity': details['total_quantity'],
                    'average_quantity': stats['average_quantity'] if stats else 0,
                    'min_quantity': stats['min_quantity'] if stats else 0,
                    'max_quantity': stats['max_quantity'] if stats else 0
                },
                'inventory_health': stats['inventory_health'] if stats else 'Unknown',
                'low_stock_alert': {
                    'count': len(low_stock),
                    'items': low_stock
                },
                'items': details['items']
            }
            
            return report
            
        except Exception as e:
            print(f"Error generating category report: {e}")
            return None
    
    def _get_quantity_status(self, quantity):
        """
        Determines the status based on quantity.
        
        Args:
            quantity (int): The item quantity
            
        Returns:
            str: Status (critical, low, medium, good, excellent)
        """
        if quantity <= 5:
            return 'critical'
        elif quantity <= 10:
            return 'low'
        elif quantity <= 25:
            return 'medium'
        elif quantity <= 50:
            return 'good'
        else:
            return 'excellent'
    
    def _calculate_inventory_health(self, avg_quantity, min_quantity):
        """
        Calculates overall inventory health for a category.
        
        Args:
            avg_quantity: Average quantity in the category
            min_quantity: Minimum quantity in the category
            
        Returns:
            str: Health status
        """
        if not avg_quantity:
            return 'No data'
        
        avg_quantity = float(avg_quantity)
        
        if avg_quantity >= 30:
            return 'Excellent'
        elif avg_quantity >= 20:
            return 'Good'
        elif avg_quantity >= 10:
            return 'Fair'
        else:
            return 'Needs attention'
    
    def export_category_data(self, category):
        """
        Exports category data in a format suitable for reporting.
        
        Args:
            category (str): The category name
            
        Returns:
            dict: Exportable category data
        """
        try:
            report = self.get_category_report(category)
            if report:
                # Format for export (could be JSON, CSV, etc.)
                export_data = {
                    'export_date': datetime.now().isoformat(),
                    'category_report': report
                }
                return export_data
            return None
            
        except Exception as e:
            print(f"Error exporting category data: {e}")
            return None
    
    def close(self):
        """
        Closes the database connection.
        """
        if self.db:
            self.db.close()


# Example usage
if __name__ == "__main__":
    controller = InventoryDetailController()
    
    # Get all categories
    print("All Categories:")
    categories = controller.get_all_categories()
    for cat in categories:
        print(f"  - {cat}")
    
    # Get details for a specific category
    if categories:
        category = categories[0]
        print(f"\nDetails for '{category}' category:")
        details = controller.get_category_details(category)
        if details:
            print(f"  Items: {details['item_count']}")
            print(f"  Total Quantity: {details['total_quantity']}")
            
        # Get statistics
        print(f"\nStatistics for '{category}':")
        stats = controller.get_category_statistics(category)
        if stats:
            print(f"  Average Quantity: {stats['average_quantity']:.2f}")
            print(f"  Min/Max: {stats['min_quantity']}/{stats['max_quantity']}")
            print(f"  Health: {stats['inventory_health']}")

    # Get all categories summary
    print("\nAll Categories Summary:")
    summaries = controller.get_all_categories_summary()
    for summary in summaries:
        print(f"  {summary['category']}: {summary['item_count']} items, "
              f"Total: {summary['total_quantity']}, Health: {summary['health']}")
    
    controller.close()