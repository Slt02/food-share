import tkinter as tk
from tkinter import messagebox

class LoginScreen:
    def __init__(self):
        self.root = tk.Tk()
        
        from CredentialController import CredentialController
        self.credential_controller = CredentialController()
        self.current_user = None
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("FoodShare - Login")
        self.root.geometry("400x600")  
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Configure colors
        self.bg_color = "#f0f8ff"
        self.primary_color = "#2e86de"
        self.success_color = "#2ecc71"
        self.error_color = "#e74c3c"
        
        self.root.configure(bg=self.bg_color)
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main container - Reduced padding to fit Register button
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=40, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Login form
        self.create_login_form(main_frame)
        
    def create_header(self, parent):
        """Create the header section"""
        # App title
        title_label = tk.Label(parent, text="FoodShare", 
                              font=("Arial", 24, "bold"), 
                              fg=self.primary_color, bg=self.bg_color)
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(parent, text="Login to your account", 
                                 font=("Arial", 12), 
                                 fg="gray", bg=self.bg_color)
        subtitle_label.pack(pady=(0, 30))
        
    def create_login_form(self, parent):
        """Create the login form"""
        # Form container
        form_frame = tk.Frame(parent, bg="white", relief="solid", bd=2)
        form_frame.pack(fill="x")
        
        # Form padding - Reduced to make room for Register button
        form_inner = tk.Frame(form_frame, bg="white", padx=30, pady=20)
        form_inner.pack(fill="both", expand=True)
        
        # Email field
        email_label = tk.Label(form_inner, text="Email:", 
                              font=("Arial", 11, "bold"), 
                              fg="black", bg="white", anchor="w")
        email_label.pack(fill="x", pady=(0, 5))
        
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(form_inner, textvariable=self.email_var,
                                   font=("Arial", 12), relief="solid", bd=1)
        self.email_entry.pack(fill="x", ipady=8, pady=(0, 15))
        self.email_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        # Password field
        password_label = tk.Label(form_inner, text="Password:", 
                                 font=("Arial", 11, "bold"), 
                                 fg="black", bg="white", anchor="w")
        password_label.pack(fill="x", pady=(0, 5))
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(form_inner, textvariable=self.password_var,
                                      font=("Arial", 12), show="*", relief="solid", bd=1)
        self.password_entry.pack(fill="x", ipady=8, pady=(0, 20))
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Login button
        self.login_button = tk.Button(form_inner, text="Login", 
                                     command=self.handle_login,
                                     font=("Arial", 12, "bold"),
                                     bg=self.primary_color, fg="white",
                                     relief="flat", bd=0, pady=12,
                                     cursor="hand2")
        self.login_button.pack(fill="x", pady=(0, 10))
        
        # Register button
        self.register_button = tk.Button(form_inner, text="Register", 
                                        command=self.handle_register,
                                        font=("Arial", 12, "bold"),
                                        bg="#f8f9fa", fg=self.primary_color,
                                        relief="solid", bd=2, pady=12,
                                        cursor="hand2")
        self.register_button.pack(fill="x", pady=(10, 20))
        
        # Status message area
        self.status_label = tk.Label(form_inner, text="", 
                                    font=("Arial", 10), bg="white", wraplength=300)
        self.status_label.pack()
        
    def clear_status(self):
        """Clear status message"""
        self.status_label.config(text="", fg="black")
        
    def show_status(self, message, is_error=False):
        """Show status message"""
        color = self.error_color if is_error else self.success_color
        self.status_label.config(text=message, fg=color)
        
    def handle_login(self):
        """Handle login button click"""
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        
        # Clear previous messages
        self.clear_status()
        
        # Basic validation
        if not email:
            error_msg = "Please enter your email address."
            self.show_status(error_msg, True)
            # Show popup warning for empty email
            messagebox.showwarning("Missing Email", error_msg)
            self.email_entry.focus()
            return
            
        if not password:
            error_msg = "Please enter your password."
            self.show_status(error_msg, True)
            # Show popup warning for empty password
            messagebox.showwarning("Missing Password", error_msg)
            self.password_entry.focus()
            return
        
        # Disable login button during processing
        self.login_button.config(state="disabled", text="Logging in...")
        self.root.update()
        
        try:
            # Attempt login using CredentialController
            success, message, user_data = self.credential_controller.login(email, password)
            
            if success:
                self.current_user = user_data
                self.show_status(f"Login successful! Welcome {user_data['name']}", False)
                
                # Show success message with user role
                messagebox.showinfo("Login Successful", 
                                  f"Welcome {user_data['name']}!\n"
                                  f"Role: {user_data['role'].title()}\n"
                                  f"Email: {user_data['email']}")
                
                # Here you would navigate to the appropriate screen based on role
                self.navigate_to_main_screen(user_data)
                
            else:
                # Show error message both on screen and as popup warning
                self.show_status(message, True)
                
                # Show popup warning for invalid credentials
                messagebox.showerror("Login Failed", 
                                   f"{message}\n\n"
                                   f"Please check your credentials and try again.")
                
        except Exception as e:
            error_msg = f"System error: {str(e)}"
            self.show_status(error_msg, True)
            
            # Show popup warning for system errors
            messagebox.showerror("System Error", 
                               f"Login failed due to system error.\n\n"
                               f"Error details: {str(e)}\n\n"
                               f"Please try again or contact support.")
            print(f"Login error: {e}")  # For debugging
            
        finally:
            # Re-enable login button
            self.login_button.config(state="normal", text="Login")
            
    def handle_register(self):
        """Handle register button click"""
        messagebox.showinfo("Register", 
                           "Registration feature will be implemented soon!\n\n"
                           "For now, please contact an administrator to create your account.")
        
    def navigate_to_main_screen(self, user_data):
        """Navigate to main screen based on user role"""
        role = user_data['role']
        
        # Hide the login screen
        self.root.withdraw()
        
        try:
            # Use CredentialController to open the appropriate main screen
            success = self.credential_controller.open_user_main_screen(user_data)
            
            if not success:
                # If screen opening failed, show error and restore login screen
                messagebox.showerror("Navigation Error", 
                                   f"Failed to open {role} main screen.\n"
                                   f"Please contact support.")
                self.show_login_screen()
        
        except Exception as e:
            # Handle any navigation errors
            messagebox.showerror("Navigation Error", 
                               f"Error opening main screen: {str(e)}\n"
                               f"Please contact support.")
            self.show_login_screen()
    
    def show_login_screen(self):
        """Show the login screen again"""
        self.root.deiconify()
        self.logout()
        
    def logout(self):
        """Clear form and reset for new login"""
        self.email_var.set("")
        self.password_var.set("")
        self.clear_status()
        self.current_user = None
        self.email_entry.focus()
        
    def run(self):
        """Start the application"""
        self.email_entry.focus()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Handle window closing"""
        self.root.destroy()

def main():
    """Main function"""
    try:
        app = LoginScreen()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Application Error", f"Failed to start application:\n{e}")

if __name__ == "__main__":
    main()