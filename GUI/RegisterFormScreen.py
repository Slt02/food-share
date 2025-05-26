import tkinter as tk
from tkinter import messagebox
from CredentialController import CredentialController


class RegisterFormScreen:
    def __init__(self, role, parent_window=None):
        self.role = role
        self.parent_window = parent_window
        self.credential_controller = CredentialController()
        
        self.root = tk.Toplevel() if parent_window else tk.Tk()
        self.root.title(f"Register as {role.title()} - FoodShare")
        self.root.geometry("450x700")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(True, True)
        
        self.is_fullscreen = False
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.setup_ui()
    
    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        return "break"
    
    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes('-fullscreen', False)
        return "break"
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        content_frame = tk.Frame(main_frame, bg="#2c3e50")
        content_frame.pack(expand=True)
        
        title_frame = tk.Frame(content_frame, bg="#2c3e50")
        title_frame.pack(pady=(0, 20))
        
        role_color = "#27ae60" if self.role == "customer" else "#e74c3c"
        role_description = "Receive Food Donations" if self.role == "customer" else "Donate Food to Others"
        
        title_label = tk.Label(
            title_frame,
            text=f"Register as {self.role.title()}",
            font=("Arial", 22, "bold"),
            bg="#2c3e50",
            fg=role_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text=role_description,
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        subtitle_label.pack(pady=(5, 0))
        
        form_frame = tk.Frame(content_frame, bg="#34495e", relief="raised", bd=2)
        form_frame.pack(fill="x")
        
        form_header = tk.Label(
            form_frame,
            text="Create Your Account",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        form_header.pack(pady=12)
        
        self.name_entry = self._create_form_field(form_frame, "First Name")
        self.surname_entry = self._create_form_field(form_frame, "Last Name")
        self.email_entry = self._create_form_field(form_frame, "Email Address")
        self.password_entry = self._create_form_field(form_frame, "Password", show="*")
        self.phone_entry = self._create_form_field(form_frame, "Phone Number (10 digits)")
        
        
        
        
        
        
       
        
        buttons_frame = tk.Frame(form_frame, bg="#34495e")
        buttons_frame.pack(fill="x", padx=20, pady=12)
        
        register_button = tk.Button(
            buttons_frame,
            text=f"Create {self.role.title()} Account",
            font=("Arial", 13, "bold"),
            bg=role_color,
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.handle_register
        )
        register_button.pack(fill="x", pady=(0, 8))
        
        back_button = tk.Button(
            buttons_frame,
            text="Back to Login",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            command=self.back_to_login
        )
        back_button.pack(fill="x")
        
        notice_label = tk.Label(
            content_frame,
            text="All fields are required",
            font=("Arial", 9),
            bg="#2c3e50",
            fg="#7f8c8d"
        )
        notice_label.pack(pady=(10, 0))
    
    def _create_form_field(self, parent, label_text, show=None):
        field_frame = tk.Frame(parent, bg="#34495e")
        field_frame.pack(fill="x", padx=20, pady=6)
        
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
            font=("Arial", 11),
            relief="solid",
            borderwidth=1,
            bg="#ecf0f1",
            fg="#2c3e50",
            show=show
        )
        entry.pack(fill="x", ipady=6)
        
        return entry
    
    def handle_register(self):
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not all([name, surname, email, password, phone]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        try:
            success, message, user_data = self.credential_controller.register(
                name=name,
                surname=surname,
                email=email,
                password=password,
                phone=phone,
                role=self.role
            )
            
            if success:
                messagebox.showinfo("Success", f"Account created successfully!\n\n{message}\n\nYou can now login with your credentials.")
                self.back_to_login()
            else:
                messagebox.showerror("Registration Failed", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def back_to_login(self):
        self.root.destroy()
        if self.parent_window:
            self.parent_window.deiconify()
    
    def on_close(self):
        self.back_to_login()
    
    def display(self):
        self.root.mainloop()


