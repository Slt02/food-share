import tkinter as tk
from tkinter import ttk, messagebox
from PendingOrdersController import PendingOrdersController
import datetime


class PendingOrdersScreen:
    def __init__(self, root, user_role="admin"):
        self.root = root
        self.user_role = user_role
        self.controller = PendingOrdersController()
        
        # Light green theme colors
        self.bg_color = "#E8F5E9"  # Light green background
        self.header_color = "#C8E6C9"  # Slightly darker green
        self.button_color = "#66BB6A"  # Medium green for buttons
        self.button_hover = "#4CAF50"  # Darker green for hover
        self.text_color = "#1B5E20"  # Dark green for text
        self.white = "#FFFFFF"
        self.table_select = "#81C784"  # Selection color
        
        # Configure the main window
        self.root.title("Pending Orders - FoodShare")
        self.root.geometry("1200x600")
        self.root.configure(bg=self.bg_color)
        
        # Create the main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create UI elements
        self.create_header()
        self.create_table()
        self.create_buttons()
        
        # Load pending orders
        self.refresh_orders()
    
    def create_header(self):
        """Create the header section with title and refresh button"""
        header_frame = tk.Frame(self.main_frame, bg=self.header_color, relief=tk.RAISED, bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Inner frame for padding
        inner_frame = tk.Frame(header_frame, bg=self.header_color)
        inner_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Title
        title_label = tk.Label(
            inner_frame,
            text="🍽️ Pending Orders",
            font=("Arial", 24, "bold"),
            bg=self.header_color,
            fg=self.text_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Order count label
        self.count_label = tk.Label(
            inner_frame,
            text="Total: 0 orders",
            font=("Arial", 14),
            bg=self.header_color,
            fg=self.text_color
        )
        self.count_label.pack(side=tk.LEFT, padx=30)
        
        # Refresh button
        refresh_btn = tk.Button(
            inner_frame,
            text="🔄 Refresh",
            command=self.refresh_orders,
            font=("Arial", 12, "bold"),
            bg=self.button_color,
            fg=self.white,
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            activebackground=self.button_hover
        )
        refresh_btn.pack(side=tk.RIGHT)
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(bg=self.button_hover))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(bg=self.button_color))
    
    def create_table(self):
        """Create the table to display pending orders"""
        # Create frame for table with light green border
        table_frame = tk.Frame(self.main_frame, bg=self.button_color, relief=tk.RAISED, bd=2)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Inner frame for white background
        inner_table_frame = tk.Frame(table_frame, bg=self.white)
        inner_table_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Create Treeview widget
        columns = ("Order ID", "Customer ID", "Delivery Address", "People", "Status", "Date & Time")
        
        self.tree = ttk.Treeview(
            inner_table_frame,
            columns=columns,
            show="headings",
            height=15,
            selectmode="browse"
        )
        
        # Define column headings and widths
        self.tree.heading("Order ID", text="Order ID")
        self.tree.heading("Customer ID", text="Customer ID")
        self.tree.heading("Delivery Address", text="Delivery Address")
        self.tree.heading("People", text="People")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Date & Time", text="Date & Time")
        
        # Configure column widths
        self.tree.column("Order ID", width=80, anchor="center")
        self.tree.column("Customer ID", width=100, anchor="center")
        self.tree.column("Delivery Address", width=400, anchor="w")
        self.tree.column("People", width=80, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("Date & Time", width=180, anchor="center")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(inner_table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(inner_table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack elements
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        inner_table_frame.grid_rowconfigure(0, weight=1)
        inner_table_frame.grid_columnconfigure(0, weight=1)
        
        # Style the treeview with green theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background=self.white,
                       foreground=self.text_color,
                       rowheight=35,
                       fieldbackground=self.white,
                       font=("Arial", 11))
        style.configure("Treeview.Heading",
                       font=("Arial", 12, "bold"),
                       background=self.header_color,
                       foreground=self.text_color)
        style.map("Treeview", 
                 background=[("selected", self.table_select)],
                 foreground=[("selected", self.white)])
        
        # Bind double-click event
        self.tree.bind("<Double-Button-1>", self.on_order_double_click)
        
        # Add alternating row colors
        self.tree.tag_configure("oddrow", background="#F1F8E9")
        self.tree.tag_configure("evenrow", background=self.white)
    
    def create_buttons(self):
        """Create action buttons at the bottom"""
        button_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # View Details button
        self.view_btn = tk.Button(
            button_frame,
            text="👁️ View Details",
            command=self.view_order_details,
            font=("Arial", 11, "bold"),
            bg=self.button_color,
            fg=self.white,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED,
            activebackground=self.button_hover
        )
        self.view_btn.pack(side=tk.LEFT, padx=5)
        
        # Process Order button (for admin/staff)
        if self.user_role in ["admin", "dropoffagent"]:
            self.process_btn = tk.Button(
                button_frame,
                text="✅ Process Order",
                command=self.process_order,
                font=("Arial", 11, "bold"),
                bg="#388E3C",  # Darker green
                fg=self.white,
                relief=tk.FLAT,
                padx=20,
                pady=10,
                cursor="hand2",
                state=tk.DISABLED,
                activebackground="#2E7D32"
            )
            self.process_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="❌ Close",
            command=self.close_screen,
            font=("Arial", 11, "bold"),
            bg="#D32F2F",
            fg=self.white,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground="#C62828"
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
        
        # Add hover effects
        self.add_button_hover_effect(self.view_btn, self.button_color, self.button_hover)
        if hasattr(self, 'process_btn'):
            self.add_button_hover_effect(self.process_btn, "#388E3C", "#2E7D32")
        self.add_button_hover_effect(close_btn, "#D32F2F", "#C62828")
        
        # Bind selection event to enable/disable buttons
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
    
    def add_button_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to buttons"""
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))
    
    def refresh_orders(self):
        """Refresh the pending orders list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get pending orders
        has_orders, orders = self.controller.check_pending_orders()
        
        if has_orders:
            # Populate the table
            for index, order in enumerate(orders):
                # Format date and time
                if isinstance(order.made, datetime.datetime):
                    date_time = order.made.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    date_time = str(order.made)
                
                # Determine row tag for alternating colors
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                
                # Insert order into table
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        order.request_id,
                        order.customer_id,
                        order.delivery_address,
                        order.number_of_people,
                        order.status,
                        date_time
                    ),
                    tags=(tag,)
                )
            
            # Update count label
            self.count_label.config(text=f"Total: {len(orders)} orders")
        else:
            # Update count label
            self.count_label.config(text="Total: 0 orders")
    
    def on_select(self, event):
        """Handle row selection"""
        selection = self.tree.selection()
        if selection:
            self.view_btn.config(state=tk.NORMAL)
            if hasattr(self, 'process_btn'):
                self.process_btn.config(state=tk.NORMAL)
        else:
            self.view_btn.config(state=tk.DISABLED)
            if hasattr(self, 'process_btn'):
                self.process_btn.config(state=tk.DISABLED)
    
    def on_order_double_click(self, event):
        """Handle double-click on order"""
        self.view_order_details()
    
    def view_order_details(self):
        """View detailed information about selected order"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Get selected order data
        item = selection[0]
        values = self.tree.item(item)['values']
        order_id = values[0]
        
        # Get full order details
        _, orders = self.controller.check_pending_orders()
        selected_order = None
        for order in orders:
            if order.request_id == order_id:
                selected_order = order
                break
        
        if selected_order:
            # Create details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Order Details - #{order_id}")
            details_window.geometry("600x500")
            details_window.configure(bg=self.bg_color)
            
            # Details frame
            details_frame = tk.Frame(details_window, bg=self.white, relief=tk.RAISED, bd=1)
            details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(
                details_frame,
                text=f"Order #{order_id} Details",
                font=("Arial", 18, "bold"),
                bg=self.white,
                fg=self.text_color
            )
            title_label.pack(pady=10)
            
            # Order information
            info_frame = tk.Frame(details_frame, bg=self.white)
            info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Display order details
            details = [
                ("Order ID:", order_id),
                ("Customer ID:", selected_order.customer_id),
                ("Customer Name:", getattr(selected_order, 'customer_name', 'N/A')),
                ("Customer Email:", getattr(selected_order, 'customer_email', 'N/A')),
                ("Customer Phone:", getattr(selected_order, 'customer_phone', 'N/A')),
                ("Delivery Address:", selected_order.delivery_address),
                ("Number of People:", selected_order.number_of_people),
                ("Status:", selected_order.status),
                ("Created At:", selected_order.made)
            ]
            
            for label, value in details:
                row_frame = tk.Frame(info_frame, bg=self.white)
                row_frame.pack(fill=tk.X, pady=5)
                
                tk.Label(
                    row_frame,
                    text=label,
                    font=("Arial", 11, "bold"),
                    bg=self.white,
                    fg=self.text_color,
                    width=15,
                    anchor="w"
                ).pack(side=tk.LEFT)
                
                tk.Label(
                    row_frame,
                    text=str(value),
                    font=("Arial", 11),
                    bg=self.white,
                    fg="#424242",
                    anchor="w"
                ).pack(side=tk.LEFT)
            
            # Items section
            items_label = tk.Label(
                info_frame,
                text="Items Ordered:",
                font=("Arial", 12, "bold"),
                bg=self.white,
                fg=self.text_color
            )
            items_label.pack(pady=(20, 10), anchor="w")
            
            # Items list
            items_frame = tk.Frame(info_frame, bg=self.header_color, relief=tk.GROOVE, bd=1)
            items_frame.pack(fill=tk.BOTH, expand=True)
            
            for item, quantity in selected_order.items.items():
                item_label = tk.Label(
                    items_frame,
                    text=f"• {item}: {quantity}",
                    font=("Arial", 11),
                    bg=self.header_color,
                    fg=self.text_color,
                    anchor="w"
                )
                item_label.pack(padx=10, pady=3, anchor="w")
            
            # Close button
            close_btn = tk.Button(
                details_window,
                text="Close",
                command=details_window.destroy,
                font=("Arial", 11, "bold"),
                bg=self.button_color,
                fg=self.white,
                relief=tk.FLAT,
                padx=20,
                pady=8,
                cursor="hand2"
            )
            close_btn.pack(pady=10)
            self.add_button_hover_effect(close_btn, self.button_color, self.button_hover)
    
    def process_order(self):
        """Process selected order (change status to Processing)"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Get selected order ID
        item = selection[0]
        values = self.tree.item(item)['values']
        order_id = values[0]
        
        # Confirm action
        result = messagebox.askyesno(
            "Process Order",
            f"Are you sure you want to process Order #{order_id}?\nThis will change its status to 'Processing'.",
            parent=self.root
        )
        
        if result:
            # Update order status
            success = self.controller.update_order_status(order_id, 'Processing')
            
            if success:
                messagebox.showinfo(
                    "Success",
                    f"Order #{order_id} has been marked as 'Processing'.",
                    parent=self.root
                )
                # Refresh the table
                self.refresh_orders()
            else:
                messagebox.showerror(
                    "Error",
                    f"Failed to process Order #{order_id}.",
                    parent=self.root
                )
    
    def close_screen(self):
        """Close the screen"""
        self.controller.close_connection()
        self.root.destroy()


# Test the screen
if __name__ == "__main__":
    root = tk.Tk()
    app = PendingOrdersScreen(root, user_role="admin")
    root.mainloop()