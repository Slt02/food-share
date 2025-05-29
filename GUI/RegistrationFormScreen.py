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
        self.root.geometry("500x550")
        self.root.configure(bg='#66BB6A')  # Light green background like login500x550")
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
        # Main container with light green background (like login form)
        main_container = tk.Frame(self.root, bg='#66BB6A')
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # White form area (like login form)
        form_frame = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Content inside white form
        content_frame = tk.Frame(form_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_label = tk.Label(content_frame, text="Register Donation", 
                              font=('Arial', 18, 'bold'), bg='white', fg='#2E7D32')
        title_label.pack(pady=(0, 20))
        
        # Item Name
        tk.Label(content_frame, text="Item Name:", 
                font=('Arial', 12, 'bold'), bg='white', fg='#2E7D32').pack(anchor=tk.W, pady=(10, 5))
        item_entry = tk.Entry(content_frame, textvariable=self.item_name_var, 
                             font=('Arial', 12), width=35, relief='solid', bd=1)
        item_entry.pack(fill=tk.X, pady=(0, 20))
        item_entry.focus()
        
        # Quantity
        tk.Label(content_frame, text="Quantity:", 
                font=('Arial', 12, 'bold'), bg='white', fg='#2E7D32').pack(anchor=tk.W, pady=(10, 5))
        quantity_entry = tk.Entry(content_frame, textvariable=self.quantity_var, 
                                 font=('Arial', 12), width=35, relief='solid', bd=1)
        quantity_entry.pack(fill=tk.X, pady=(0, 30))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(pady=20)
        
        # Register button (green like login)
        register_btn = tk.Button(button_frame, text="Register Donation", 
                               command=self.submit_donation, 
                               bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                               padx=20, pady=8, relief='flat', cursor='hand2')
        register_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Clear button
        clear_btn = tk.Button(button_frame, text="Clear Form", 
                            command=self.clear_form,
                            bg='#757575', fg='white', font=('Arial', 12),
                            padx=20, pady=8, relief='flat', cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Back button
        back_btn = tk.Button(button_frame, text="Back to Main", 
                           command=self.on_close,
                           bg='#757575', fg='white', font=('Arial', 12),
                           padx=20, pady=8, relief='flat', cursor='hand2')
        back_btn.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = tk.Label(content_frame, text="Ready to register donation",
                                   bg='white', fg='#666666', font=('Arial', 10))
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
            # Set current date and time (not just date)
            if 'donation_date' not in donation_data:
                donation_data['donation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
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
            # Validate donation (this includes checking details)
            validation_result = self.validate_donation(donation_data)
            if not validation_result['valid']:
                error_msg = "\n".join([f"• {error}" for error in validation_result['errors']])
                messagebox.showwarning("Validation Error", error_msg)
                self.status_label.config(text="Please fix errors", foreground='red')
                return
            
            # Create donation using Database class
            result = self.creating_donation(donation_data)
            
            if result['success']:
                # Simple success message without ID
                success_msg = (f"🎉 SUCCESS! 🎉\n\n"
                              f"Donation registered successfully!")
                
                messagebox.showinfo("Success", success_msg)
                self.status_label.config(text="Donation registered successfully!", foreground='green')
                self.clear_form()
            else:
                messagebox.showwarning("Error", f"Registration failed:\n{result['message']}")
                self.status_label.config(text="Registration failed", foreground='red')
        
        except Exception as e:
            messagebox.showwarning("Error", f"Unexpected error:\n{str(e)}")
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