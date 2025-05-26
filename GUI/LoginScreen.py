import tkinter as tk
from tkinter import messagebox
from CredentialController import CredentialController
from GUI.RegisterFormScreen import RegisterFormScreen


class LoginScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FoodShare - Login")
        self.root.geometry("400x650")  
        self.root.configure(bg="#2c3e50")
        self.root.resizable(True, True)  
        
        # Add fullscreen capability
        self.is_fullscreen = False
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        # Initialize credential controller
        self.credential_controller = CredentialController()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container - centered content that works in both windowed and fullscreen
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Content container - max width to prevent stretching in fullscreen
        content_frame = tk.Frame(main_frame, bg="#2c3e50")
        content_frame.pack(expand=True)  # Center the content)
        
        # Title with fullscreen hint
        title_frame = tk.Frame(content_frame, bg="#2c3e50")
        title_frame.pack(pady=(0, 40))
        
        title_label = tk.Label(
            title_frame,
            text="FoodShare",
            font=("Arial", 28, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title_label.pack()
        
        # Login form
        login_frame = tk.Frame(content_frame, bg="#34495e", relief="raised", bd=2)
        login_frame.pack(fill="x", pady=(0, 30))  # Increased bottom padding
        
        login_title = tk.Label(
            login_frame,
            text="Login",
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        login_title.pack(pady=15)
        
        # Email field
        self.email_entry = self._create_form_field(login_frame, "Email")
        
        # Password field
        self.password_entry = self._create_form_field(login_frame, "Password", show="*")
        
        # Login button
        login_button = tk.Button(
            login_frame,
            text="Login",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            relief="flat",
            padx=30,
            pady=10,
            command=self.handle_login
        )
        login_button.pack(pady=(15, 20))  # Added bottom padding
        
        # Registration section
        register_frame = tk.Frame(content_frame, bg="#2c3e50")
        register_frame.pack(fill="x", expand=False)  # Don't expand, fixed positioning
        
        register_label = tk.Label(
            register_frame,
            text="New User?",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        register_label.pack(pady=(0, 15))
        
        # Register buttons
        customer_button = tk.Button(
            register_frame,
            text="Register as Customer",
            font=("Arial", 12),
            bg="#27ae60",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            command=self.register_as_customer
        )
        customer_button.pack(pady=5, fill="x")
        
        donor_button = tk.Button(
            register_frame,
            text="Register as Donor",
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            command=self.register_as_donor
        )
        donor_button.pack(pady=5, fill="x")
    
    def _create_form_field(self, parent, label_text, show=None):
        """Helper method to create form fields"""
        field_frame = tk.Frame(parent, bg="#34495e")
        field_frame.pack(fill="x", padx=20, pady=8)
        
        label = tk.Label(
            field_frame,
            text=label_text,
            font=("Arial", 11),
            bg="#34495e",
            fg="#ecf0f1"
        )
        label.pack(anchor="w", pady=(0, 3))
        
        entry = tk.Entry(
            field_frame,
            font=("Arial", 12),
            relief="solid",
            borderwidth=1,
            bg="#ecf0f1",
            fg="#2c3e50",
            show=show
        )
        entry.pack(fill="x", ipady=8)
        
        return entry
    
    def handle_login(self):
        """Handle the login process"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        try:
            success, message, user_data = self.credential_controller.login(email, password)
            
            if success:
                messagebox.showinfo("Success", "Login successful!")
                self.root.destroy()
                self.credential_controller.open_user_main_screen(user_data)
            else:
                messagebox.showerror("Login Failed", message)
                self.password_entry.delete(0, tk.END)
                
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
    
    def register_as_customer(self):
        """Open registration form for customer role"""
        try:
            print("Attempting to import RegisterFormScreen...")
            from GUI.RegisterFormScreen import RegisterFormScreen
            print("Import successful!")
            
            print("Hiding login window...")
            self.root.withdraw()
            
            print("Creating RegisterFormScreen...")
            register_screen = RegisterFormScreen(role="customer", parent_window=self.root)
            
            print("Displaying RegisterFormScreen...")
            register_screen.display()
            
        except ImportError as e:
            error_msg = f"Cannot import RegisterFormScreen: {e}"
            print(f" {error_msg}")
            messagebox.showerror("Import Error", error_msg)
        except Exception as e:
            error_msg = f"Error opening registration: {e}"
            print(f"{error_msg}")
            messagebox.showerror("Error", error_msg)
    
    def register_as_donor(self):
        """Open registration form for donor role"""
        try:
            print("Attempting to import RegisterFormScreen...")
            from GUI.RegisterFormScreen import RegisterFormScreen
            print("Import successful!")
            
            print("Hiding login window...")
            self.root.withdraw()
            
            print("Creating RegisterFormScreen...")
            register_screen = RegisterFormScreen(role="donor", parent_window=self.root)
            
            print("Displaying RegisterFormScreen...")
            register_screen.display()
            
        except ImportError as e:
            error_msg = f"Cannot import RegisterFormScreen: {e}"
            print(f"{error_msg}")
            messagebox.showerror("Import Error", error_msg)
        except Exception as e:
            error_msg = f"Error opening registration: {e}"
            print(f" {error_msg}")
            messagebox.showerror("Error", error_msg)
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        
        if self.is_fullscreen:
            
            self.root.configure(bg="#2c3e50")
        
        return "break"
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        self.is_fullscreen = False
        self.root.attributes('-fullscreen', False)
        return "break"
    
    def display(self):
        """Display the login screen"""
        self.root.mainloop()


