import tkinter as tk
from tkinter import ttk, messagebox
from OrderStatusController import OrderStatusController
from datetime import datetime


class PendingDeliveriesScreen:
    def __init__(self, parent_window=None):
        self.controller = OrderStatusController()
        
        # Create main window
        if parent_window:
            self.root = tk.Toplevel(parent_window)
        else:
            self.root = tk.Tk()
        
        self.root.title("Pending Deliveries Monitor")
        self.root.geometry("950x600")
        
        # Light green theme colors
        self.bg_color = "#E8F5E9"  # Very light green
        self.header_color = "#A5D6A7"  # Light green
        self.button_color = "#81C784"  # Medium light green
        self.button_hover = "#66BB6A"  # Slightly darker green
        self.text_color = "#1B5E20"  # Dark green for text
        self.white = "#FFFFFF"
        
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
        self.load_pending_orders()
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header frame
        header_frame = tk.Frame(main_frame, bg=self.header_color, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Header label
        header_label = tk.Label(
            header_frame,
            text="Pending Deliveries",
            font=("Arial", 24, "bold"),
            bg=self.header_color,
            fg=self.text_color
        )
        header_label.pack(expand=True)
        
        # Content frame with scrollbar
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview with scrollbar
        tree_frame = tk.Frame(content_frame, bg=self.bg_color)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for orders
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Customer ID", "Delivery Address", "Number of People", "Delivery Status", "Created At"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        
        # Configure scrollbar
        scrollbar.config(command=self.tree.yview)
        
        # Define headings
        self.tree.heading("ID", text="Order ID")
        self.tree.heading("Customer ID", text="Customer ID")
        self.tree.heading("Delivery Address", text="Delivery Address")
        self.tree.heading("Number of People", text="People")
        self.tree.heading("Delivery Status", text="Delivery Status")
        self.tree.heading("Created At", text="Created At")
        
        # Configure column widths
        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("Customer ID", width=90, anchor="center")
        self.tree.column("Delivery Address", width=250, anchor="w")
        self.tree.column("Number of People", width=70, anchor="center")
        self.tree.column("Delivery Status", width=180, anchor="center")
        self.tree.column("Created At", width=160, anchor="center")
        
        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.white, foreground=self.text_color,
                       rowheight=30, fieldbackground=self.white)
        style.configure("Treeview.Heading", background=self.header_color, 
                       foreground=self.text_color, font=("Arial", 11, "bold"))
        style.map("Treeview", background=[("selected", self.button_color)])
        
        # Bind click event
        self.tree.bind("<Double-Button-1>", self.on_order_click)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bottom frame for buttons and info
        bottom_frame = tk.Frame(main_frame, bg=self.bg_color)
        bottom_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Info label
        self.info_label = tk.Label(
            bottom_frame,
            text="",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.info_label.pack(side=tk.LEFT)
        
        # Close button
        close_btn = tk.Button(
            bottom_frame,
            text="Close",
            command=self.close_window,
            bg=self.button_color,
            fg=self.white,
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Bind hover effects
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg=self.button_hover))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg=self.button_color))
    
    def load_pending_orders(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load orders from controller
        orders = self.controller.requestOrdersWithPendingDeliveries()
        
        if orders:
            for order in orders:
                # Format the created_at date
                created_at = order['created_at']
                if isinstance(created_at, datetime):
                    formatted_date = created_at.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    formatted_date = str(created_at)
                
                # Insert into treeview
                self.tree.insert("", "end", values=(
                    order['id'],
                    order['customer_id'],
                    order['delivery_address'],
                    order['number_of_people'],
                    order['delivery_status'],
                    formatted_date
                ))
            
            # Update info label
            self.info_label.config(text=f"Total pending deliveries: {len(orders)}")
        else:
            # Show warning if no pending deliveries
            self.info_label.config(text="No pending deliveries found")
            messagebox.showinfo(
                "No Pending Deliveries",
                "There are no orders with 'Not Delivered/Pending' status.",
                parent=self.root
            )
    
    def on_order_click(self, event):
        # Get selected item
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            order_id = item['values'][0]
            
            # Get order details
            order = self.controller.showOrderStatus(order_id)
            
            if order:
                # Show popup with order status (not delivery_status)
                self.show_status_popup(order)
    
    def show_status_popup(self, order):
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"Order #{order['id']} Status")
        popup.geometry("400x200")
        popup.configure(bg=self.bg_color)
        
        # Make popup modal
        popup.transient(self.root)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(popup, bg=self.bg_color, padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text=f"Order #{order['id']}",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg=self.header_color, padx=20, pady=20)
        status_frame.pack(fill=tk.X)
        
        # Status label
        status_label = tk.Label(
            status_frame,
            text="Order Status:",
            font=("Arial", 12),
            bg=self.header_color,
            fg=self.text_color
        )
        status_label.pack()
        
        # Status value
        status_value = tk.Label(
            status_frame,
            text=order['status'],
            font=("Arial", 18, "bold"),
            bg=self.header_color,
            fg=self.text_color
        )
        status_value.pack()
        
        # OK button
        ok_btn = tk.Button(
            main_frame,
            text="OK",
            command=popup.destroy,
            bg=self.button_color,
            fg=self.white,
            font=("Arial", 12, "bold"),
            padx=30,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT
        )
        ok_btn.pack(pady=(20, 0))
        
        # Bind hover effects
        ok_btn.bind("<Enter>", lambda e: ok_btn.config(bg=self.button_hover))
        ok_btn.bind("<Leave>", lambda e: ok_btn.config(bg=self.button_color))
    
    def close_window(self):
        self.controller.close()
        self.root.destroy()
    
    #def run(self):
        #.root.mainloop()


# Example usage
if __name__ == "__main__":
    app = PendingDeliveriesScreen()
    app.run()