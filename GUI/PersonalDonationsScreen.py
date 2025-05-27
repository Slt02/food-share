import tkinter as tk
from tkinter import messagebox
from PersonalDonationsController import PersonalDonationsController


class PersonalDonationsScreen:
    """GUI screen to display donor's personal donations"""
    
    def __init__(self, parent=None, donor_id=None):
        self.parent = parent
        self.donor_id = donor_id  # This comes from the logged-in donor's session
        self.controller = PersonalDonationsController()
        self.window = None
        self.donations = []
        
        # Validate that donor_id is provided (from login session)
        if not self.donor_id:
            raise ValueError("Donor ID is required - must be provided from login session")
        
    def show(self):
        """Display the personal donations screen"""
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title("My Donations")
        self.window.geometry("800x600")
        self.window.configure(bg="#f5f7fa")
        
        # Title
        title = tk.Label(
            self.window,
            text="📋 My Donations",
            font=("Arial", 24, "bold"),
            bg="#f5f7fa",
            fg="#1f2937"
        )
        title.pack(pady=30)
        
        # Menu area
        self.create_donations_area()
        
        # Refresh button
        refresh_btn = tk.Button(
            self.window,
            text="🔄 Refresh",
            font=("Arial", 12, "bold"),
            bg="#4f46e5",
            fg="white",
            padx=20,
            pady=10,
            command=self.refresh_donations
        )
        refresh_btn.pack(pady=20)
        
        self.load_donations()
        
        if not self.parent:
            self.window.mainloop()
    
    def create_donations_area(self):
        """Create scrollable donations area"""
        self.donations_frame = tk.Frame(self.window, bg="#f5f7fa")
        self.donations_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
    
    def load_donations(self):
        """Load donations from controller"""
        if not self.donor_id:
            self.show_error("No donor ID provided")
            return
            
        # Clear existing items
        for widget in self.donations_frame.winfo_children():
            widget.destroy()
        
        # Get donations from controller
        self.donations = self.controller.find_personal_donations(self.donor_id)
        
        if not self.donations:
            self.show_no_donations()
        else:
            self.display_donations()
    
    def show_no_donations(self):
        """Show no donations message"""
        no_donations = tk.Label(
            self.donations_frame,
            text="📋\n\nNo Donations Found\n\nYou haven't made any donations yet.\nStart sharing food to help your community!",
            font=("Arial", 16),
            bg="#ffffff",
            fg="#6b7280",
            relief=tk.RAISED,
            bd=1,
            padx=40,
            pady=40
        )
        no_donations.pack(pady=50)
        
        # Show warning popup
        self.show_warning("You haven't made any donations yet.")
    
    def display_donations(self):
        """Display donation items"""
        for donation in self.donations:
            self.create_donation_card(donation)
    
    def create_donation_card(self, donation):
        """Create donation item card"""
        donation_id, item_name, quantity, date, status, location, description = donation
        
        # Card frame
        card = tk.Frame(
            self.donations_frame,
            bg="white",
            relief=tk.RAISED,
            bd=1,
            cursor="hand2"
        )
        card.pack(fill=tk.X, pady=10, padx=20)
        
        # Card content
        content = tk.Frame(card, bg="white")
        content.pack(fill=tk.X, padx=25, pady=20)
        
        # Top row - Item name and status
        top_row = tk.Frame(content, bg="white")
        top_row.pack(fill=tk.X, pady=(0, 10))
        
        # Item name
        tk.Label(
            top_row,
            text=f"📦 {item_name}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(side=tk.LEFT)
        
        # Status badge
        status_color = self.get_status_color(status)
        tk.Label(
            top_row,
            text=f"● {status.upper()}",
            font=("Arial", 10, "bold"),
            bg="white",
            fg=status_color
        ).pack(side=tk.RIGHT)
        
        # Middle row - Quantity and date
        middle_row = tk.Frame(content, bg="white")
        middle_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            middle_row,
            text=f"Quantity: {quantity}",
            font=("Arial", 12),
            bg="white",
            fg="#6b7280"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            middle_row,
            text=f"Date: {date}",
            font=("Arial", 12),
            bg="white",
            fg="#6b7280"
        ).pack(side=tk.RIGHT)
        
        # Bottom row - Location
        if location:
            tk.Label(
                content,
                text=f"📍 {location}",
                font=("Arial", 11),
                bg="white",
                fg="#9ca3af"
            ).pack(anchor="w")
        
        # Click hint
        tk.Label(
            content,
            text="Click to view details →",
            font=("Arial", 10, "italic"),
            bg="white",
            fg="#3b82f6"
        ).pack(anchor="w", pady=(5, 0))
        
        # Click event
        def on_click(event, d_id=donation_id):
            self.show_donation_info(d_id)
        
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
    
    def get_status_color(self, status):
        """Get color for donation status"""
        status_colors = {
            'pending': '#f59e0b',    # Yellow
            'approved': '#10b981',   # Green
            'collected': '#3b82f6',  # Blue
            'delivered': '#8b5cf6',  # Purple
            'cancelled': '#ef4444',  # Red
            'expired': '#6b7280'     # Gray
        }
        return status_colors.get(status.lower(), '#6b7280')
    
    def show_donation_info(self, donation_id):
        """Show detailed donation information"""
        donation_details = self.controller.get_donation_details(donation_id)
        
        if not donation_details:
            messagebox.showerror("Error", "Could not retrieve donation details.")
            return
        
        self.show_info_popup(donation_details)
    
    def show_info_popup(self, details):
        """Display donation info popup"""
        popup = tk.Toplevel(self.window)
        popup.title("Donation Details")
        popup.geometry("450x500")
        popup.configure(bg="white")
        popup.transient(self.window)
        popup.grab_set()
        
        # Title
        tk.Label(
            popup,
            text="📦",
            font=("Arial", 30),
            bg="white"
        ).pack(pady=(30, 10))
        
        tk.Label(
            popup,
            text=details['item_name'],
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(pady=(0, 20))
        
        # Details frame
        details_frame = tk.Frame(popup, bg="#f8f9fa", relief=tk.GROOVE, bd=1)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        # Donation ID
        self.create_detail_row(details_frame, "Donation ID", f"#{details['donation_id']}")
        
        # Quantity
        self.create_detail_row(details_frame, "Quantity", str(details['quantity']))
        
        # Status
        status_color = self.get_status_color(details['status'])
        status_frame = tk.Frame(details_frame, bg="#f8f9fa")
        status_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            status_frame,
            text="Status",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            fg="#1f2937"
        ).pack(anchor="w")
        
        tk.Label(
            status_frame,
            text=f"● {details['status'].upper()}",
            font=("Arial", 11, "bold"),
            bg="#f8f9fa",
            fg=status_color
        ).pack(anchor="w", pady=(2, 10))
        
        # Date
        self.create_detail_row(details_frame, "Donation Date", str(details['donation_date']))
        
        # Location
        if details['pickup_location']:
            self.create_detail_row(details_frame, "Pickup Location", details['pickup_location'])
        
        # Expiry date
        if details['expiry_date']:
            self.create_detail_row(details_frame, "Expiry Date", str(details['expiry_date']))
        
        # Description
        if details['description']:
            desc_frame = tk.Frame(details_frame, bg="#f8f9fa")
            desc_frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(
                desc_frame,
                text="Description",
                font=("Arial", 12, "bold"),
                bg="#f8f9fa",
                fg="#1f2937"
            ).pack(anchor="w")
            
            tk.Label(
                desc_frame,
                text=details['description'],
                font=("Arial", 11),
                bg="#f8f9fa",
                fg="#6b7280",
                wraplength=350,
                justify=tk.LEFT
            ).pack(anchor="w", pady=(2, 10))
        
        # Close button
        tk.Button(
            popup,
            text="Close",
            font=("Arial", 11),
            bg="#6b7280",
            fg="white",
            padx=20,
            pady=8,
            command=popup.destroy
        ).pack(pady=(0, 30))
    
    def create_detail_row(self, parent, label, value):
        """Create a detail row in the popup"""
        row_frame = tk.Frame(parent, bg="#f8f9fa")
        row_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            row_frame,
            text=label,
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            fg="#1f2937"
        ).pack(anchor="w")
        
        tk.Label(
            row_frame,
            text=value,
            font=("Arial", 11),
            bg="#f8f9fa",
            fg="#6b7280"
        ).pack(anchor="w", pady=(2, 10))
    
    def show_warning(self, message):
        """Show warning popup"""
        messagebox.showwarning("Notice", message)
    
    def show_error(self, message):
        """Show error popup"""
        messagebox.showerror("Error", message)
    
    def refresh_donations(self):
        """Refresh donations list"""
        self.load_donations()
