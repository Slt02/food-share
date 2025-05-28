import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ..ModificationValidator import ModificationValidator
import threading


class ManagementControlScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("FoodShare - Inventory Management Control")
        self.root.geometry("900x700")
        self.root.configure(bg='#E8F5E9')  # Light green background
        
        # Initialize the validator
        try:
            self.validator = ModificationValidator()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            root.destroy()
            return
        
        # Create the main container
        main_container = tk.Frame(root, bg='#E8F5E9')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_container, text="Inventory Management System", 
                              font=('Arial', 20, 'bold'), bg='#E8F5E9', fg='#2E7D32')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.add_item_tab = tk.Frame(self.notebook, bg='#F1F8E9')
        self.update_item_tab = tk.Frame(self.notebook, bg='#F1F8E9')
        self.view_inventory_tab = tk.Frame(self.notebook, bg='#F1F8E9')
        
        self.notebook.add(self.add_item_tab, text="Add New Item")
        self.notebook.add(self.update_item_tab, text="Update Item")
        self.notebook.add(self.view_inventory_tab, text="View Inventory")
        
        # Setup each tab
        self.setup_add_item_tab()
        self.setup_update_item_tab()
        self.setup_view_inventory_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, 
                             relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load inventory on startup
        self.refresh_inventory_view()
    
    def setup_add_item_tab(self):
        """Setup the Add New Item tab"""
        # Main frame
        main_frame = tk.Frame(self.add_item_tab, bg='#F1F8E9', padx=40, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(main_frame, text="Add New Item to Inventory", 
                font=('Arial', 16, 'bold'), bg='#F1F8E9', fg='#2E7D32').grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Item Name
        tk.Label(main_frame, text="Item Name:", font=('Arial', 12), bg='#F1F8E9', fg='#1B5E20').grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.add_item_name = tk.Entry(main_frame, font=('Arial', 12), width=30, bg='#FFFFFF', relief=tk.SOLID, bd=1)
        self.add_item_name.grid(row=1, column=1, padx=10, pady=10)
        
        # Description
        tk.Label(main_frame, text="Description:", font=('Arial', 12), bg='#F1F8E9', fg='#1B5E20').grid(row=2, column=0, sticky='ne', padx=10, pady=10)
        self.add_description = tk.Text(main_frame, font=('Arial', 12), width=30, height=3, bg='#FFFFFF', relief=tk.SOLID, bd=1)
        self.add_description.grid(row=2, column=1, padx=10, pady=10)
        
        # Category - Changed to Entry instead of Combobox
        tk.Label(main_frame, text="Category:", font=('Arial', 12), bg='#F1F8E9', fg='#1B5E20').grid(row=3, column=0, sticky='e', padx=10, pady=10)
        self.add_category = tk.Entry(main_frame, font=('Arial', 12), width=30, bg='#FFFFFF', relief=tk.SOLID, bd=1)
        self.add_category.grid(row=3, column=1, padx=10, pady=10)
        
        # Quantity
        tk.Label(main_frame, text="Quantity:", font=('Arial', 12), bg='#F1F8E9', fg='#1B5E20').grid(row=4, column=0, sticky='e', padx=10, pady=10)
        self.add_quantity = tk.Entry(main_frame, font=('Arial', 12), width=30, bg='#FFFFFF', relief=tk.SOLID, bd=1)
        self.add_quantity.grid(row=4, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#F1F8E9')
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        add_btn = tk.Button(button_frame, text="Add Item", font=('Arial', 12), 
                           bg='#4CAF50', fg='white', padx=20, pady=10,
                           command=self.add_item, cursor='hand2')
        add_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="Clear", font=('Arial', 12), 
                             bg='#f44336', fg='white', padx=20, pady=10,
                             command=self.clear_add_form, cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def setup_update_item_tab(self):
        """Setup the Update Item tab"""
        # Main frame
        main_frame = tk.Frame(self.update_item_tab, bg='#F1F8E9', padx=40, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(main_frame, text="Update Existing Item", 
                font=('Arial', 16, 'bold'), bg='#F1F8E9', fg='#2E7D32').grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Item Name to Update
        tk.Label(main_frame, text="Item Name:", font=('Arial', 12), bg='#F1F8E9', fg='#1B5E20').grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.update_item_name = tk.Entry(main_frame, font=('Arial', 12), width=30, bg='#FFFFFF', relief=tk.SOLID, bd=1)
        self.update_item_name.grid(row=1, column=1, padx=10, pady=10)
        
        # Load button
        load_btn = tk.Button(main_frame, text="Load Item", font=('Arial', 10), 
                            bg='#2196F3', fg='white', padx=10, cursor='hand2',
                            command=self.load_item_details)
        load_btn.grid(row=1, column=2, padx=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=2, column=0, columnspan=3, sticky='ew', pady=20)
        
        # New values (optional)
        tk.Label(main_frame, text="New Values (leave empty to keep current):", 
                font=('Arial', 12, 'italic'), bg='#F1F8E9', fg='#388E3C').grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # New Description
        tk.Label(main_frame, text="New Description:", font=('Arial', 12), bg='#F1F8E9', fg='#1B5E20').grid(row=4, column=0, sticky='ne', padx=10, pady=10)
        self.update_description = tk.Text(main_frame, font=('Arial', 12), width=30, height=3, bg='#FFFFFF', relief=tk.SOLID, bd=1)
        self.update_description.grid(row=4, column=1, padx=10, pady=10)
        
        # New Category - Changed to Entry
        tk.Label(main_frame, text="New Category:", font=('Arial', 12), bg='#F1F8E9', fg='#1B5E20').grid(row=5, column=0, sticky='e', padx=10, pady=10)
        self.update_category = tk.Entry(main_frame, font=('Arial', 12), width=30, bg='#FFFFFF', relief=tk.SOLID, bd=1)
        self.update_category.grid(row=5, column=1, padx=10, pady=10)
        
        # New Quantity
        tk.Label(main_frame, text="New Quantity:", font=('Arial', 12), bg='#F1F8E9', fg='#1B5E20').grid(row=6, column=0, sticky='e', padx=10, pady=10)
        self.update_quantity = tk.Entry(main_frame, font=('Arial', 12), width=30, bg='#FFFFFF', relief=tk.SOLID, bd=1)
        self.update_quantity.grid(row=6, column=1, padx=10, pady=10)
        
        # Current values display
        self.current_values_frame = tk.LabelFrame(main_frame, text="Current Values", 
                                                 font=('Arial', 12), bg='#F1F8E9', fg='#1B5E20', padx=20, pady=10)
        self.current_values_frame.grid(row=7, column=0, columnspan=2, pady=20, sticky='ew')
        
        self.current_values_text = tk.Label(self.current_values_frame, text="Load an item to see current values", 
                                           font=('Arial', 10), bg='#F1F8E9', fg='#424242', justify=tk.LEFT)
        self.current_values_text.pack()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#F1F8E9')
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        update_btn = tk.Button(button_frame, text="Update Item", font=('Arial', 12), 
                              bg='#FF9800', fg='white', padx=20, pady=10,
                              command=self.update_item, cursor='hand2')
        update_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="Clear", font=('Arial', 12), 
                             bg='#f44336', fg='white', padx=20, pady=10,
                             command=self.clear_update_form, cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def setup_view_inventory_tab(self):
        """Setup the View Inventory tab"""
        # Main frame
        main_frame = tk.Frame(self.view_inventory_tab, bg='#F1F8E9', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title and refresh button
        title_frame = tk.Frame(main_frame, bg='#F1F8E9')
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(title_frame, text="Current Inventory", 
                font=('Arial', 16, 'bold'), bg='#F1F8E9', fg='#2E7D32').pack(side=tk.LEFT)
        
        refresh_btn = tk.Button(title_frame, text="Refresh", font=('Arial', 10), 
                               bg='#2196F3', fg='white', padx=15, cursor='hand2',
                               command=self.refresh_inventory_view)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Create Treeview for inventory display
        tree_frame = tk.Frame(main_frame, bg='#F1F8E9')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style for treeview
        style = ttk.Style()
        style.configure("Treeview", background="#FFFFFF", foreground="#424242", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", background="#81C784", foreground="#1B5E20", font=('Arial', 10, 'bold'))
        
        # Create Treeview for inventory display
        tree_frame = tk.Frame(main_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        self.inventory_tree = ttk.Treeview(tree_frame, 
                                          columns=('Name', 'Description', 'Category', 'Quantity'),
                                          show='headings',
                                          yscrollcommand=vsb.set,
                                          xscrollcommand=hsb.set)
        
        vsb.config(command=self.inventory_tree.yview)
        hsb.config(command=self.inventory_tree.xview)
        
        # Configure columns
        self.inventory_tree.heading('Name', text='Item Name')
        self.inventory_tree.heading('Description', text='Description')
        self.inventory_tree.heading('Category', text='Category')
        self.inventory_tree.heading('Quantity', text='Quantity')
        
        self.inventory_tree.column('Name', width=150)
        self.inventory_tree.column('Description', width=300)
        self.inventory_tree.column('Category', width=100)
        self.inventory_tree.column('Quantity', width=80)
        
        # Pack everything
        self.inventory_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def add_item(self):
        """Handle adding a new item"""
        # Get values
        item_name = self.add_item_name.get()
        description = self.add_description.get("1.0", tk.END).strip()
        category = self.add_category.get()
        quantity = self.add_quantity.get()
        
        # Validate inputs are not empty
        if not all([item_name, description, category, quantity]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Call validator
        success, message = self.validator.add_item(item_name, description, category, quantity)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_add_form()
            self.refresh_inventory_view()
            self.status_var.set(f"Added: {item_name}")
        else:
            messagebox.showerror("Error", message)
    
    def update_item(self):
        """Handle updating an item"""
        # Get values
        item_name = self.update_item_name.get()
        
        if not item_name:
            messagebox.showerror("Error", "Please enter an item name to update!")
            return
        
        # Get new values (only if provided)
        new_description = self.update_description.get("1.0", tk.END).strip()
        new_category = self.update_category.get()
        new_quantity = self.update_quantity.get()
        
        # Prepare update parameters
        update_params = {}
        if new_description:
            update_params['new_description'] = new_description
        if new_category:
            update_params['new_category'] = new_category
        if new_quantity:
            update_params['new_quantity'] = new_quantity
        
        if not update_params:
            messagebox.showerror("Error", "No updates provided!")
            return
        
        # Call validator
        success, message = self.validator.update_item(item_name, **update_params)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_update_form()
            self.refresh_inventory_view()
            self.status_var.set(f"Updated: {item_name}")
        else:
            messagebox.showerror("Error", message)
    
    def load_item_details(self):
        """Load current item details for update"""
        item_name = self.update_item_name.get()
        
        if not item_name:
            messagebox.showerror("Error", "Please enter an item name!")
            return
        
        details = self.validator.get_item_details(item_name)
        
        if details:
            info_text = f"Description: {details['description']}\n"
            info_text += f"Category: {details['category']}\n"
            info_text += f"Quantity: {details['quantity']}"
            self.current_values_text.config(text=info_text)
            self.status_var.set(f"Loaded: {item_name}")
        else:
            self.current_values_text.config(text="Item not found!")
            messagebox.showerror("Error", f"Item '{item_name}' not found in inventory!")
    
    def refresh_inventory_view(self):
        """Refresh the inventory treeview"""
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Get all inventory items
        try:
            # Direct database query to get all items
            query = "SELECT item_name, description, category, quantity FROM inventory ORDER BY item_name"
            results = self.validator.db.execute_query(query)
            
            if results:
                for row in results:
                    self.inventory_tree.insert('', tk.END, values=row)
                self.status_var.set(f"Loaded {len(results)} items")
            else:
                self.status_var.set("No items in inventory")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load inventory: {str(e)}")
            self.status_var.set("Error loading inventory")
    
    def clear_add_form(self):
        """Clear the add item form"""
        self.add_item_name.delete(0, tk.END)
        self.add_description.delete("1.0", tk.END)
        self.add_category.delete(0, tk.END)  # Changed from set('') to delete()
        self.add_quantity.delete(0, tk.END)
    
    def clear_update_form(self):
        """Clear the update item form"""
        self.update_item_name.delete(0, tk.END)
        self.update_description.delete("1.0", tk.END)
        self.update_category.delete(0, tk.END)  # Changed from set('') to delete()
        self.update_quantity.delete(0, tk.END)
        self.current_values_text.config(text="Load an item to see current values")
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if hasattr(self, 'validator'):
                self.validator.close()
            self.root.destroy()


def main():
    root = tk.Tk()
    app = ManagementControlScreen(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()