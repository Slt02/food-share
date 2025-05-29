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
        
        # Title
        title = tk.Label(self.window, text="My Donations", font=("Arial", 18, "bold"))
        title.pack(pady=10)
        
        # Create scrollable list
        self.create_donations_list()
        
        # Refresh button
        refresh_btn = tk.Button(self.window, text="Refresh", command=self.load_donations)
        refresh_btn.pack(pady=10)
        
        self.load_donations()
        
        if not self.parent:
            self.window.mainloop()
    
    def create_donations_list(self):
        """Create scrollable donations list"""
        # Frame for the treeview and scrollbar
        list_frame = tk.Frame(self.window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create treeview with scrollbar
        self.tree = ttk.Treeview(list_frame, columns=("Item", "Quantity", "Date"), show="headings")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.tree.heading("Item", text="Item Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Date", text="Date")
        
        self.tree.column("Item", width=200)
        self.tree.column("Quantity", width=100)
        self.tree.column("Date", width=150)
        
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
        
        # Simple details popup
        popup = tk.Toplevel(self.window)
        popup.title("Donation Details")
        popup.geometry("300x200")
        
        tk.Label(popup, text=f"Item: {details['item_name']}", font=("Arial", 12)).pack(pady=5)
        tk.Label(popup, text=f"Quantity: {details['quantity']}").pack(pady=5)
        tk.Label(popup, text=f"Date: {details['donation_date']}").pack(pady=5)
        tk.Label(popup, text=f"ID: {details['donation_id']}").pack(pady=5)
        
        tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)