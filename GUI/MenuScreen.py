import tkinter as tk
from tkinter import ttk, messagebox

class MenuScreen:
    def __init__(self, parent=None, customer_id=None, database=None):
        self.parent = parent
        self.customer_id = customer_id
        self.database = database
        
        # Create window
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
            
        self.root.title("Food Share - Menu")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Initialize database
        if not self.database:
            self.init_database()
        else:
            self.db = self.database
        
        # Load available items
        self.available_items = []
        self.load_available_items()
        
        # Show warning if no items available
        if not self.available_items:
            self.show_no_items_warning()
        
        self.setup_ui()
    
    def init_database(self):
        """Initialize database connection"""
        try:
            from Database import Database
            self.db = Database()
        except Exception as e:
            self.db = None
    
    def load_available_items(self):
        """Load available items from inventory table"""
        if not self.db:
            return
        
        try:
            query = "SELECT item_name, description, category, quantity FROM inventory WHERE quantity > 0"
            result = self.db.execute_query(query)
            
            if result:
                self.available_items = []
                for row in result:
                    item_name, description, category, quantity = row
                    self.available_items.append({
                        'name': item_name,
                        'description': description or f"Fresh {item_name}",
                        'category': category or "General",
                        'quantity': quantity
                    })
            else:
                self.available_items = []
                
        except Exception as e:
            self.available_items = []
    
    def show_no_items_warning(self):
        """Show warning popup when no items available"""
        messagebox.showwarning(
            "No Items Available",
            "NO FOOD ITEMS AVAILABLE\n\n"
            "Sorry, there are currently no food items available.\n\n"
            "Please try again later or contact support."
        )
    
    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Food Menu", 
                font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50').pack(expand=True)
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        if self.available_items:
            title_text = "Available Items"
        else:
            title_text = "No items currently available"
        
        tk.Label(main_frame, text=title_text, font=('Arial', 16, 'bold'), 
                bg='#f0f0f0', fg='#2c3e50').pack(pady=(0, 20))
        
        # Items display
        if self.available_items:
            self.create_items_display(main_frame)
        else:
            self.create_empty_display(main_frame)
        
        # Back button
        tk.Button(main_frame, text="⬅️ Back to Main", command=self.on_close,
                 bg='#95a5a6', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=8).pack(pady=20)
    
    def create_items_display(self, parent):
        """Create display for available items"""
        # Scrollable frame
        canvas = tk.Canvas(parent, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind("<Configure>", 
                            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create item cards
        row = 0
        col = 0
        max_cols = 3
        
        for item in self.available_items:
            # Item card
            card = tk.Frame(scrollable_frame, bg='white', relief=tk.RAISED, 
                           bd=2, cursor='hand2')
            card.grid(row=row, column=col, padx=10, pady=10, sticky='ew', 
                     ipadx=15, ipady=15)
            
            # Make card clickable
            card.bind("<Button-1>", lambda e, item=item: self.show_item_info(item))
            
            # Item name
            name_label = tk.Label(card, text=f"🍽️ {item['name']}", 
                                font=('Arial', 14, 'bold'), bg='white', fg='#2c3e50',
                                cursor='hand2')
            name_label.pack(anchor='w')
            name_label.bind("<Button-1>", lambda e, item=item: self.show_item_info(item))
            

            
            # Category
            cat_label = tk.Label(card, text=f"📂 {item['category']}", 
                               font=('Arial', 10), bg='white', fg='#7f8c8d',
                               cursor='hand2')
            cat_label.pack(anchor='w', pady=(3, 0))
            cat_label.bind("<Button-1>", lambda e, item=item: self.show_item_info(item))
            
            # Next position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Configure grid
        for i in range(max_cols):
            scrollable_frame.grid_columnconfigure(i, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_empty_display(self, parent):
        """Create display when no items available"""
        empty_frame = tk.Frame(parent, bg='#f0f0f0')
        empty_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(empty_frame, text="🍽️", font=('Arial', 64), bg='#f0f0f0').pack()
        tk.Label(empty_frame, text="No items currently available", 
                font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#7f8c8d').pack(pady=15)
        tk.Label(empty_frame, text="Please check back later", 
                font=('Arial', 12), bg='#f0f0f0', fg='#95a5a6').pack()
    
    def show_item_info(self, item):
        """Show item details in popup message box"""
        details = f"🍽️ {item['name']}\n\n"
        details += f"📝 Description:\n{item['description']}\n\n"
        details += f"📂 Category: {item['category']}"
        
        messagebox.showinfo(f"Item Details - {item['name']}", details)
    
    def on_close(self):
        """Close MenuScreen and return to parent"""
        if self.parent:
            self.parent.deiconify()
        self.root.destroy()
    
    def display(self):
        """Display the MenuScreen"""
        self.root.mainloop()

# Test function
def test_menu_screen():
    try:
        menu = MenuScreen(None, "test_customer", None)
        menu.display()
    except Exception as e:
        print(f"Test error: {e}")

if __name__ == "__main__":
    test_menu_screen()