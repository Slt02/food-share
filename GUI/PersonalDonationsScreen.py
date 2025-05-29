import tkinter as tk
from tkinter import ttk, messagebox
from PersonalDonationsController import PersonalDonationsController


class PersonalDonationsScreen:
    """Simple GUI screen to display donor's personal donations"""
    
    def __init__(self, parent=None, donor_id=None):
        self.parent = parent
        self.donor_id = donor_id
        self.controller = PersonalDonationsController()
        self.window = None
        
        if not self.donor_id:
            raise ValueError("Donor ID is required")
        
    def show(self):
        """Display the personal donations screen"""
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title("My Donations")
        self.window.geometry("600x500")
        self.window.configure(bg='#66BB6A')  # Light green background like login
        
        # Main container
        main_container = tk.Frame(self.window, bg='#66BB6A')
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # White content area
        content_frame = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = tk.Frame(content_frame, bg='white')
        title_frame.pack(fill=tk.X, pady=(20, 10))
        
        title = tk.Label(title_frame, text="My Donations", 
                        font=("Arial", 18, "bold"), bg='white', fg='#2E7D32')
        title.pack()
        
        # Create scrollable list
        self.create_donations_list(content_frame)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(pady=20)
        
        # Refresh button (green like login)
        refresh_btn = tk.Button(button_frame, text="Refresh", command=self.load_donations,
                               bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                               padx=20, pady=8, relief='flat', cursor='hand2')
        refresh_btn.pack()
        
        self.load_donations()
        
        if not self.parent:
            self.window.mainloop()
    
    def create_donations_list(self, parent_frame):
        """Create scrollable donations list"""
        # Frame for the treeview and scrollbar
        list_frame = tk.Frame(parent_frame, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create treeview with scrollbar
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), foreground='#2E7D32')
        style.configure("Treeview", font=('Arial', 11))
        
        self.tree = ttk.Treeview(list_frame, columns=("Item", "Quantity", "Date"), show="headings")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.tree.heading("Item", text="Item Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Date", text="Date & Time")
        
        self.tree.column("Item", width=200)
        self.tree.column("Quantity", width=100)
        self.tree.column("Date", width=200)
        
        # Pack treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click to show details
        self.tree.bind("<Double-1>", self.show_details)
    
    def load_donations(self):
        """Load donations from controller"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get donations from controller
        donations = self.controller.find_personal_donations(self.donor_id)
        
        if not donations:
            messagebox.showinfo("Info", "No donations found")
            return
        
        # Add donations to tree
        for donation in donations:
            donation_id, item_name, quantity, date = donation
            self.tree.insert("", "end", values=(item_name, quantity, date), tags=(donation_id,))
    
    def show_details(self, event):
        """Show donation details"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        donation_id = item['tags'][0]
        
        details = self.controller.get_donation_details(donation_id)
        if not details:
            messagebox.showerror("Error", "Could not get donation details")
            return
        
        # Green-themed details popup
        popup = tk.Toplevel(self.window)
        popup.title("Donation Details")
        popup.geometry("350x250")
        popup.configure(bg='#66BB6A')
        
        # White content frame
        content = tk.Frame(popup, bg='white', relief='raised', bd=2)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(content, text="Donation Details", 
                font=("Arial", 16, "bold"), bg='white', fg='#2E7D32').pack(pady=(15, 20))
        
        # Details
        tk.Label(content, text=f"Item: {details['item_name']}", 
                font=("Arial", 12), bg='white', fg='#333333').pack(pady=5)
        tk.Label(content, text=f"Quantity: {details['quantity']}", 
                font=("Arial", 12), bg='white', fg='#333333').pack(pady=5)
        tk.Label(content, text=f"Date & Time: {details['donation_date']}", 
                font=("Arial", 12), bg='white', fg='#333333').pack(pady=5)
        tk.Label(content, text=f"ID: {details['donation_id']}", 
                font=("Arial", 12), bg='white', fg='#333333').pack(pady=5)
        
        # Close button
        close_btn = tk.Button(content, text="Close", command=popup.destroy,
                             bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                             padx=20, pady=8, relief='flat', cursor='hand2')
        close_btn.pack(pady=15)