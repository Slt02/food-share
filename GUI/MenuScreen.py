import tkinter as tk
from tkinter import messagebox
from MenuController import MenuController
from GUI.OrderFormScreen import OrderFormScreen



class MenuScreen:
    def __init__(self, parent=None, customer_id=None):
        self.parent = parent
        self.menu_controller = MenuController()
        self.window = None
        self.available_items = []
        self.cart = {}
        self.customer_id = customer_id  # Store customer ID if provided
        
    def show(self):
        """Display the menu screen"""
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title("Food Share - Menu")
        self.window.geometry("800x700")
        self.window.configure(bg="#9AFF9A")
        
        # Title
        title = tk.Label(
            self.window,
            text="🍽️ Available Menu",
            font=("Arial", 24, "bold"),
            bg="#9AFF9A",
            fg="#1f2937"
        )
        title.pack(pady=30)
        
        # Menu area
        self.create_menu_area()
        
        # Refresh button
        refresh_btn = tk.Button(
            self.window,
            text="🔄 Refresh",
            font=("Arial", 12, "bold"),
            bg="#4f46e5",
            fg="white",
            padx=20,
            pady=10,
            command=self.refresh_menu
        )
        refresh_btn.pack(pady=20)

        # View Cart button
        view_cart_btn = tk.Button(
            self.window,
            text="🛒 View Cart",
            font=("Arial", 12, "bold"),
            bg="#10b981",
            fg="white",
            padx=20,
            pady=10,
            command=self.click_cart
        )
        view_cart_btn.pack(pady=10)

        # Clear cart button
        clear_cart_btn = tk.Button(
            self.window,
            text="🗑️ Clear Cart",
            font=("Arial", 12, "bold"),
            bg="#ef4444",
            fg="white",
            padx=20,
            pady=10,
            command=lambda: self.cart.clear()
        )
        clear_cart_btn.pack(pady=10)
        
        self.load_menu()
        
        if not self.parent:
            self.window.mainloop()
    
    def create_menu_area(self):
        """Create scrollable menu area"""
        # Frame for menu items
        self.menu_frame = tk.Frame(self.window, bg="#9AFF9A")
        self.menu_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
    
    def load_menu(self):
        """Load menu items"""
        # Clear existing items
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        
        # Get items from controller
        self.available_items = self.menu_controller.check_availability()
        
        if not self.available_items:
            self.show_no_items()
        else:
            self.display_items()
    
    def show_no_items(self):
        """Show no items message"""
        no_items = tk.Label(
            self.menu_frame,
            text="🍽️\n\nNo Items Available\n\nCheck back soon!",
            font=("Arial", 16),
            bg="#ffffff",
            fg="#6b7280",
            relief=tk.RAISED,
            bd=1,
            padx=40,
            pady=40
        )
        no_items.pack(pady=50)
        
        messagebox.showwarning("Notice", "No food items are currently available.")
    
    def display_items(self):
        """Display menu items"""
        for item_name, quantity in self.available_items:
            self.create_food_card(item_name)
    
    def create_food_card(self, item_name):
        """Create food item card"""
        # Card frame
        card = tk.Frame(
            self.menu_frame,
            bg="white",
            relief=tk.RAISED,
            bd=1,
            cursor="hand2"
        )
        card.pack(fill=tk.X, pady=10, padx=20)
        
        # Card content
        content = tk.Frame(card, bg="white")
        content.pack(fill=tk.X, padx=30, pady=20)
        
        # Icon and name
        tk.Label(
            content,
            text="🍽️",
            font=("Arial", 20),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(
            content,
            text=item_name,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(side=tk.LEFT)
        
        # Status
        tk.Label(
            content,
            text="● Available",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#10b981"
        ).pack(side=tk.RIGHT)
        
        # Click event
        def on_click(event, name=item_name):
            self.show_food_info(name)
        
        card.bind("<Button-1>", on_click)
        content.bind("<Button-1>", on_click)
        
        # Hover effect
        def on_enter(event):
            card.configure(bg="#f8fafc")
            content.configure(bg="#f8fafc")
        
        def on_leave(event):
            card.configure(bg="white")
            content.configure(bg="white")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
    
    def show_food_info(self, item_name):
        """Show food information popup"""
        # Check if still available
        current_quantity = self.menu_controller.get_item_quantity(item_name)
        
        if current_quantity <= 0:
            messagebox.showwarning("Sorry", f"{item_name} is no longer available.")
            self.refresh_menu()
            return
        
        # Get item details
        item_details = self.menu_controller.get_item_details(item_name)
        self.show_info_popup(item_name, item_details)
    
    def show_info_popup(self, item_name, item_details):
        """Display info popup"""
        popup = tk.Toplevel(self.window)
        popup.title("Food Details")
        popup.geometry("400x450")
        popup.configure(bg="#9AFF9A")
        popup.transient(self.window)
        popup.grab_set()
        
        # Title
        tk.Label(
            popup,
            text="🍽️",
            font=("Arial", 30),
            bg="#9AFF9A"
        ).pack(pady=(30, 10))
        
        tk.Label(
            popup,
            text=item_name,
            font=("Arial", 20, "bold"),
            bg="#9AFF9A",
            fg="#1f2937"
        ).pack(pady=(0, 30))
        
        # Details frame
        details = tk.Frame(popup, bg="#9AFF9A", relief=tk.GROOVE, bd=1)
        details.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        # Get category and description
        category = item_details.get('category', 'Not specified') if item_details else 'Not specified'
        description = item_details.get('description', 'No description available') if item_details else 'No description available'
        
        # Category
        tk.Label(
            details,
            text="Category",
            font=("Arial", 12, "bold"),
            bg="#9AFF9A",
            fg="#1f2937"
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        tk.Label(
            details,
            text=category,
            font=("Arial", 11),
            bg="#9AFF9A",
            fg="#6b7280"
        ).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Description
        tk.Label(
            details,
            text="Description",
            font=("Arial", 12, "bold"),
            bg="#9AFF9A",
            fg="#1f2937"
        ).pack(anchor="w", padx=20, pady=(0, 5))
        
        tk.Label(
            details,
            text=description,
            font=("Arial", 11),
            bg="#9AFF9A",
            fg="#6b7280",
            wraplength=320,
            justify=tk.LEFT
        ).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Status
        tk.Label(
            details,
            text="✅ Available Now",
            font=("Arial", 11, "bold"),
            bg="#9AFF9A",
            fg="#10b981"
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(popup, bg="#9AFF9A")
        btn_frame.pack(fill=tk.X, padx=30, pady=(0, 30))
        
        tk.Button(
            btn_frame,
            text="📦 Add to Order",
            font=("Arial", 11, "bold"),
            bg="#10b981",
            fg="white",
            padx=15,
            pady=8,
            command=lambda: self.add_to_order(item_name, popup)
        ).pack(side=tk.LEFT)
        
        tk.Button(
            btn_frame,
            text="Close",
            font=("Arial", 11),
            bg="#6b7280",
            fg="white",
            padx=15,
            pady=8,
            command=popup.destroy
        ).pack(side=tk.RIGHT)
    
    def add_to_order(self, item_name, popup):
        """Add to order placeholder"""
        print(f"Adding {item_name} to order")
        if( item_name in self.cart):
            self.cart[item_name] += 1
        else:
            self.cart[item_name] = 1

        popup.destroy()
    
    def click_cart(self):
        """Handle cart click"""
        if not self.cart:
            messagebox.showinfo("Cart", "Your cart is empty.")
            return
        
        # Create OrderFormScreen with selected items
        order_form = OrderFormScreen(self.window, self.cart, self.customer_id)
        order_form.showOrderForm()

        # Clear the Cart
        #self.cart.clear()

    def refresh_menu(self):
        """Refresh menu"""
        self.load_menu()