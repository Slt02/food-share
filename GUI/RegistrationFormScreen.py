import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class RegistrationFormScreen:
    def __init__(self, parent=None, controller=None, user_id=None):
        # Handle parameters from MainScreenDonor
        self.parent = parent
        self.controller = controller  # DonationController from main screen (not used)
        self.donor_id = user_id  # This is the logged-in user ID
        
        # Create window as Toplevel if parent exists, otherwise as root
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
            
        self.root.title("Food Share - Donation Registration")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')
        
        # Handle window closing properly
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.item_name_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        
        # Initialize database connection using your existing Database class
        self.init_database()
        self.setup_ui()
    
    def init_database(self):
        """Initialize database connection using existing Database class"""
        try:
            from Database import Database
            # Use your existing database connection with foodshare database
            self.db = Database(host="localhost", user="root", password="", database="foodshare")
            
            # Create donations table if it doesn't exist
            self.db.create_donations_table()
            print("Database initialized successfully")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            self.db = None
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Register Donation", 
                 font=('Arial', 18, 'bold')).pack(pady=(0, 10))
        
        if self.donor_id:
            ttk.Label(main_frame, text=f"Logged in as: {self.donor_id}", 
                     font=('Arial', 10), foreground='blue').pack(pady=(0, 15))
        
        # Show database status
        if self.db:
            ttk.Label(main_frame, text="Connected to foodshare database", 
                     font=('Arial', 9), foreground='green').pack(pady=(0, 15))
        else:
            ttk.Label(main_frame, text="Database connection failed", 
                     font=('Arial', 9), foreground='red').pack(pady=(0, 15))
        
        ttk.Label(main_frame, text="Item Name:", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        item_entry = ttk.Entry(main_frame, textvariable=self.item_name_var, 
                              font=('Arial', 12), width=35)
        item_entry.pack(fill=tk.X, pady=(0, 20))
        item_entry.focus()
        
        ttk.Label(main_frame, text="Quantity:", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        quantity_entry = ttk.Entry(main_frame, textvariable=self.quantity_var, 
                                  font=('Arial', 12), width=35)
        quantity_entry.pack(fill=tk.X, pady=(0, 30))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Register Donation", 
                  command=self.submit_donation).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(button_frame, text="Clear Form", 
                  command=self.clear_form).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(button_frame, text="Back to Main", 
                  command=self.on_close).pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(main_frame, text="Ready to register donation")
        self.status_label.pack(pady=(20, 0))
        
        self.root.bind('<Return>', lambda e: self.submit_donation())
    
    def check_details(self, donation_data):
        """Check item name and quantity"""
        errors = []
        
        if 'item_name' not in donation_data or not donation_data['item_name']:
            errors.append("Item name is required")
        if 'quantity' not in donation_data or not donation_data['quantity']:
            errors.append("Quantity is required")
        else:
            try:
                quantity = int(donation_data['quantity'])
                if quantity <= 0:
                    errors.append("Quantity must be a positive number")
            except (ValueError, TypeError):
                errors.append("Quantity must be a valid number")
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    def validate_donation(self, donation_data):
        """Validate the donation"""
        return self.check_details(donation_data)
    
    def creating_donation(self, donation_data):
        """Create donation using Database class"""
        try:
            if 'donation_date' not in donation_data:
                donation_data['donation_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Use Database class method to create donation
            donation_id = self.db.create_donation(
                donor_id=donation_data['donor_id'],
                item_name=donation_data['item_name'],
                quantity=int(donation_data['quantity']),
                donation_date=donation_data['donation_date']
            )
            
            if donation_id:
                # Get the created donation using Database class method
                created_donation = self.db.get_donation_by_id(donation_id)
                
                return {
                    'success': True,
                    'donation': created_donation,
                    'message': f"Donation registered successfully with ID: {donation_id}"
                }
            else:
                return {
                    'success': False,
                    'error': 'Database error',
                    'message': "Failed to create donation in database"
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create donation: {str(e)}"
            }
    
    def submit_donation(self):
        """Submit donation using Database class"""
        if not self.db:
            messagebox.showerror("Database Error", "No database connection available")
            return
            
        if not self.donor_id:
            messagebox.showerror("Authentication Error", "No donor logged in")
            return
            
        self.status_label.config(text="Processing...", foreground='orange')
        self.root.update()
        
        donation_data = {
            'donor_id': self.donor_id,
            'item_name': self.item_name_var.get().strip(),
            'quantity': self.quantity_var.get().strip()
        }
        
        try:
            # Check details
            check_result = self.check_details(donation_data)
            if not check_result['valid']:
                error_msg = "\n".join([f"• {error}" for error in check_result['errors']])
                messagebox.showwarning("Validation Error", error_msg)
                self.status_label.config(text="Please fix errors", foreground='red')
                return
            
            # Validate donation
            validation_result = self.validate_donation(donation_data)
            if not validation_result['valid']:
                error_msg = "\n".join([f"• {error}" for error in validation_result['errors']])
                messagebox.showwarning("Validation Failed", error_msg)
                self.status_label.config(text="Validation failed", foreground='red')
                return
            
            # Create donation using Database class
            result = self.creating_donation(donation_data)
            
            if result['success']:
                donation = result['donation']
                success_msg = (f"🎉 SUCCESS! 🎉\n\n"
                              f"Donation registered successfully!\n\n"
                              f"ID: {donation['id']}\n"
                              f"Donor: {donation['donor_id']}\n"
                              f"Item: {donation['item_name']}\n"
                              f"Quantity: {donation['quantity']}\n"
                              f"Date: {donation['donation_date']}")
                
                messagebox.showinfo("Success", success_msg)
                self.status_label.config(text="Donation registered successfully!", foreground='green')
                self.clear_form()
            else:
                messagebox.showerror("Error", f"Registration failed:\n{result['message']}")
                self.status_label.config(text="Registration failed", foreground='red')
        
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{str(e)}")
            self.status_label.config(text="Error occurred", foreground='red')
    
    def clear_form(self):
        """Clear the form"""
        self.item_name_var.set("")
        self.quantity_var.set("")
        self.status_label.config(text="Form cleared - ready for new donation", foreground='gray')
    
    def on_close(self):
        """Handle window closing - return to parent window"""
        if self.parent:
            self.parent.deiconify()  # Show the parent window
        self.root.destroy()  # Close this window
    
    def display(self):
        """Display method called by MainScreenDonor"""
        self.root.mainloop()