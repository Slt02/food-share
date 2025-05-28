import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from InventoryDetailController import InventoryDetailController
import threading


class ManageInventoryScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("FoodShare - Manage Inventory Categories")
        self.root.geometry("1000x700")
        self.root.configure(bg='#E8F5E9')  # Light green background

        self.status_var = tk.StringVar()

        
    

        
        # Initialize the controller
        try:
            self.controller = InventoryDetailController()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            root.destroy()
            return
        
        # Main container
        main_container = tk.Frame(root, bg='#E8F5E9')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_container, text="Inventory Categories Management", 
                              font=('Arial', 22, 'bold'), bg='#E8F5E9', fg='#2E7D32')
        title_label.pack(pady=(0, 20))
        
        # Create main layout with two panels
        self.create_layout(main_container)
        
        # Load categories on startup
        self.load_categories()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, 
                             relief=tk.SUNKEN, anchor=tk.W, bg='#C8E6C9')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)



    
    
    def create_layout(self, parent):
        """Create the main layout with categories list and details panel"""
        # Main content frame
        content_frame = tk.Frame(parent, bg='#E8F5E9')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Categories list
        left_panel = tk.Frame(content_frame, bg='#F1F8E9', relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # Categories header
        header_frame = tk.Frame(left_panel, bg='#81C784')
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Food Categories", font=('Arial', 14, 'bold'), 
                bg='#81C784', fg='white').pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(header_frame, text="🔄 Refresh", font=('Arial', 10), 
                               bg='#4CAF50', fg='white', bd=0, padx=10, pady=5,
                               command=self.load_categories, cursor='hand2')
        refresh_btn.pack(pady=(0, 10))
        
        # Categories listbox with scrollbar
        list_frame = tk.Frame(left_panel, bg='#F1F8E9')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.categories_listbox = tk.Listbox(list_frame, font=('Arial', 12), 
                                            yscrollcommand=scrollbar.set,
                                            bg='white', selectbackground='#81C784',
                                            selectforeground='white', height=20)
        self.categories_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.categories_listbox.yview)
        
        # Bind selection event
        self.categories_listbox.bind('<<ListboxSelect>>', self.on_category_select)
        
        # Categories summary at bottom
        self.summary_label = tk.Label(left_panel, text="", font=('Arial', 10), 
                                     bg='#F1F8E9', fg='#424242')
        self.summary_label.pack(pady=10)
        
        # Right panel - Category details
        self.right_panel = tk.Frame(content_frame, bg='#F1F8E9', relief=tk.RAISED, bd=1)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initial message
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Show welcome message in the right panel"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        welcome_frame = tk.Frame(self.right_panel, bg='#F1F8E9')
        welcome_frame.pack(expand=True)
        
        tk.Label(welcome_frame, text="Welcome to Inventory Management", 
                font=('Arial', 18, 'bold'), bg='#F1F8E9', fg='#2E7D32').pack(pady=20)
        
        tk.Label(welcome_frame, text="Select a category from the list to view details", 
                font=('Arial', 12), bg='#F1F8E9', fg='#616161').pack()
        
        # Add icon or image (using text emoji for simplicity)
        tk.Label(welcome_frame, text="📦", font=('Arial', 48), bg='#F1F8E9').pack(pady=20)
    
    def load_categories(self):
        """Load all categories from the database"""
        try:
            # Clear current list
            self.categories_listbox.delete(0, tk.END)
            
            # Get categories
            categories = self.controller.get_all_categories()
            
            if categories:
                # Get summary for each category
                summaries = self.controller.get_all_categories_summary()
                category_info = {s['category']: s for s in summaries}
                
                # Add to listbox with item count
                for category in categories:
                    if category in category_info:
                        item_count = category_info[category]['item_count']
                        display_text = f"{category} ({item_count} items)"
                    else:
                        display_text = category
                    self.categories_listbox.insert(tk.END, display_text)
                
                # Update summary
                total_categories = len(categories)
                total_items = sum(s['item_count'] for s in summaries)
                self.summary_label.config(text=f"Total: {total_categories} categories, {total_items} items")
                self.status_var.set(f"Loaded {total_categories} categories")
            else:
                self.categories_listbox.insert(tk.END, "No categories found")
                self.summary_label.config(text="No data available")
                self.status_var.set("No categories in inventory")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories: {str(e)}")
            self.status_var.set("Error loading categories")
    
    def on_category_select(self, event):
        """Handle category selection"""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            category_text = self.categories_listbox.get(index)
            # Extract category name (remove item count)
            category = category_text.split(' (')[0]
            self.show_category_details(category)
    
    def show_category_details(self, category):
        """Display detailed information about the selected category"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        try:
            # Get category data
            details = self.controller.get_category_details(category)
            stats = self.controller.get_category_statistics(category)
            low_stock = self.controller.get_low_stock_items_by_category(category, threshold=15)
            
            if not details:
                tk.Label(self.right_panel, text="No data available", 
                        font=('Arial', 14), bg='#F1F8E9').pack(pady=20)
                return
            
            # Create scrollable frame
            canvas = tk.Canvas(self.right_panel, bg='#F1F8E9')
            scrollbar = ttk.Scrollbar(self.right_panel, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#F1F8E9')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Category header
            header_frame = tk.Frame(scrollable_frame, bg='#81C784', relief=tk.RAISED, bd=1)
            header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
            
            tk.Label(header_frame, text=f"Category: {category}", 
                    font=('Arial', 18, 'bold'), bg='#81C784', fg='white').pack(pady=10)
            
            # Statistics section
            stats_frame = tk.LabelFrame(scrollable_frame, text="Statistics", 
                                       font=('Arial', 12, 'bold'), bg='#F1F8E9', fg='#2E7D32')
            stats_frame.pack(fill=tk.X, padx=10, pady=5)
            
            stats_content = tk.Frame(stats_frame, bg='#F1F8E9')
            stats_content.pack(padx=20, pady=10)
            
            # Display statistics in grid
            stats_data = [
                ("Total Items:", f"{details['item_count']}"),
                ("Total Quantity:", f"{details['total_quantity']}"),
                
                ("Min/Max Quantity:", f"{stats['min_quantity']} / {stats['max_quantity']}"),
                
            ]
            
            for i, (label, value) in enumerate(stats_data):
                tk.Label(stats_content, text=label, font=('Arial', 11), 
                        bg='#F1F8E9', fg='#424242').grid(row=i, column=0, sticky='e', padx=5, pady=2)
                
                # Color code health status
                if label == "Inventory Health:":
                    color = self.get_health_color(value)
                    tk.Label(stats_content, text=value, font=('Arial', 11, 'bold'), 
                            bg='#F1F8E9', fg=color).grid(row=i, column=1, sticky='w', padx=5, pady=2)
                else:
                    tk.Label(stats_content, text=value, font=('Arial', 11), 
                            bg='#F1F8E9', fg='#212121').grid(row=i, column=1, sticky='w', padx=5, pady=2)
            
              

            



            
            # Items list
            items_frame = tk.LabelFrame(scrollable_frame, text="Items in Category", 
                                       font=('Arial', 12, 'bold'), bg='#F1F8E9', fg='#2E7D32')
            items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Create treeview for items
            tree_frame = tk.Frame(items_frame, bg='#F1F8E9')
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Configure treeview style
            style = ttk.Style()
            style.configure("Treeview", background="white", foreground="#424242")
            style.configure("Treeview.Heading", background="#81C784", foreground="white")
            
            # Create treeview
            columns = ('Name', 'Quantity', 'Status', 'Description')
            tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
            
            # Define headings
            tree.heading('Name', text='Item Name')
            tree.heading('Quantity', text='Quantity')
            tree.heading('Status', text='Status')
            tree.heading('Description', text='Description')
            
            # Configure columns
            tree.column('Name', width=150)
            tree.column('Quantity', width=80, anchor='center')
            tree.column('Status', width=80, anchor='center')
            tree.column('Description', width=300)
            
            # Add items
            for item in details['items']:
                status_display = self.get_status_display(item['status'])
                tree.insert('', tk.END, values=(
                    item['name'],
                    item['quantity'],
                    status_display,
                    item['description'][:50] + '...' if len(item['description']) > 50 else item['description']
                ))
            
            # Add scrollbar to treeview
            tree_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
            tree.configure(yscrollcommand=tree_scroll.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            self.status_var.set(f"Showing details for {category}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load category details: {str(e)}")
            self.status_var.set("Error loading details")
    
    def get_health_color(self, health):
        """Get color based on health status"""
        health_colors = {
            'Excellent': '#2E7D32',
            'Good': '#388E3C',
            'Fair': '#F57C00',
            'Needs attention': '#D32F2F',
            'No data': '#757575'
        }
        return health_colors.get(health, '#424242')
    
    def get_status_display(self, status):
        """Get formatted status display"""
        status_map = {
            'critical': '🔴 Critical',
            'low': '🟡 Low',
            'medium': '🟠 Medium',
            'good': '🟢 Good',
            'excellent': '💚 Excellent'
        }
        return status_map.get(status, status)
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if hasattr(self, 'controller'):
                self.controller.close()
            self.root.destroy()
    
    


def main():
    root = tk.Tk()
    app = ManageInventoryScreen(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()