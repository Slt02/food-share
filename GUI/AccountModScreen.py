import tkinter as tk
from tkinter import messagebox


class AccountModScreen:
    def __init__(self, parent_window=None, role=None, user_data=None):
        """Account Modification Screen with ALL required elements"""
        
        # Handle different calling patterns
        if isinstance(parent_window, dict):
            self.user_data = parent_window
            self.parent_window = role
            self.role = self.user_data.get('role') if self.user_data else None
        else:
            self.parent_window = parent_window
            self.role = role
            self.user_data = user_data
        
        # Import CredentialController
        from CredentialController import CredentialController
        self.credential_controller = CredentialController()
        
        self.root = tk.Toplevel() if self.parent_window else tk.Tk()
        self.root.title("Account Settings - FoodShare")
        self.root.state('zoomed')
        self.root.configure(bg="#f0f0f0")
        
        if self.parent_window:
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        if self.user_data:
            self.setup_ui()

    def displayAccountModScreen(self, user_id=None):
        """Display the account screen and fetch user data if needed"""
        if not self.user_data and user_id:
            try:
                user_data = self.credential_controller.Database.get_user_by_id(user_id)
                if user_data:
                    self.user_data = user_data
                else:
                    messagebox.showerror("Error", "Could not load user data")
                    return
            except Exception as e:
                print(f"Error fetching user data: {e}")
                messagebox.showerror("Error", "Could not load user data")
                return
        
        if not hasattr(self, '_ui_setup'):
            self.setup_ui()
        
        self.root.deiconify()
        self.root.lift()
        self.root.focus_set()

    def setup_ui(self):
        """Setup the complete UI with ALL elements"""
        self._ui_setup = True
        
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # MAIN CONTAINER with scrollable canvas
        canvas = tk.Canvas(self.root, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")

        # TITLE
        title_label = tk.Label(
            scrollable_frame,
            text="Account Settings",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 10))

        # CURRENT USER
        user_label = tk.Label(
            scrollable_frame,
            text=f"Current User: {self.user_data.get('name', '')} {self.user_data.get('surname', '')}",
            font=("Arial", 14),
            bg="#f0f0f0",
            fg="#34495e"
        )
        user_label.pack(pady=(0, 20))

        # FORM CONTAINER
        form_container = tk.Frame(scrollable_frame, bg="#ffffff", relief="solid", bd=2)
        form_container.pack(fill="x", pady=20)

        # ALL FORM FIELDS
        fields_container = tk.Frame(form_container, bg="#ffffff")
        fields_container.pack(fill="x", padx=30, pady=30)

        # NAME FIELD
        tk.Label(fields_container, text="Name:", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w")
        self.name_entry = tk.Entry(fields_container, font=("Arial", 12), width=40)
        self.name_entry.pack(fill="x", pady=(5, 15), ipady=5)

        # SURNAME FIELD
        tk.Label(fields_container, text="Surname:", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w")
        self.surname_entry = tk.Entry(fields_container, font=("Arial", 12), width=40)
        self.surname_entry.pack(fill="x", pady=(5, 15), ipady=5)

        # USERNAME FIELD
        tk.Label(fields_container, text="Username:", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w")
        self.username_entry = tk.Entry(fields_container, font=("Arial", 12), width=40)
        self.username_entry.pack(fill="x", pady=(5, 15), ipady=5)

        # EMAIL FIELD
        tk.Label(fields_container, text="Email:", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w")
        self.email_entry = tk.Entry(fields_container, font=("Arial", 12), width=40)
        self.email_entry.pack(fill="x", pady=(5, 15), ipady=5)

        # PHONE FIELD
        tk.Label(fields_container, text="Phone:", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w")
        self.phone_entry = tk.Entry(fields_container, font=("Arial", 12), width=40)
        self.phone_entry.pack(fill="x", pady=(5, 15), ipady=5)

        # PASSWORD FIELD
        tk.Label(fields_container, text="Password:", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w")
        self.password_entry = tk.Entry(fields_container, font=("Arial", 12), width=40, show="*")
        self.password_entry.pack(fill="x", pady=(5, 30), ipady=5)

        # BUTTONS CONTAINER
        buttons_container = tk.Frame(fields_container, bg="#ffffff")
        buttons_container.pack(fill="x", pady=20)

        # SUBMIT BUTTON
        submit_btn = tk.Button(
            buttons_container,
            text="SUBMIT CHANGES",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            width=25,
            height=2,
            command=self.submit_changes
        )
        submit_btn.pack(pady=10)

        # MAIN SCREEN BUTTON
        main_screen_btn = tk.Button(
            buttons_container,
            text="BACK TO MAIN SCREEN",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            width=25,
            height=2,
            command=self.back_to_main
        )
        main_screen_btn.pack(pady=10)

        # POPULATE FIELDS WITH CURRENT DATA
        self._populate_fields()

    def _populate_fields(self):
        """Fill fields with current user data"""
        if self.user_data:
            self.name_entry.insert(0, self.user_data.get('name', ''))
            self.surname_entry.insert(0, self.user_data.get('surname', ''))
            self.username_entry.insert(0, self.user_data.get('username', ''))
            self.email_entry.insert(0, self.user_data.get('email', ''))
            self.phone_entry.insert(0, self.user_data.get('phone', ''))
            # Show current password
            current_password = self.user_data.get('password', '')
            if current_password:
                self.password_entry.insert(0, current_password)

    def submit_changes(self):
        """Save all changes to database"""
        print("SUBMIT CHANGES CLICKED!")  # Debug
        
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()
        
        updates = {}
        if name: updates["name"] = name
        if surname: updates["surname"] = surname
        if username: updates["username"] = username
        if email: updates["email"] = email
        if phone: updates["phone"] = phone
        if password: updates["password"] = password
        
        if not updates:
            messagebox.showwarning("No Changes", "Please enter information to update")
            return
        
        try:
            success, message = self.credential_controller.update(self.user_data['id'], updates)
            if success:
                messagebox.showinfo("Success", "Account updated successfully!")
                self.back_to_main()
            else:
                messagebox.showerror("Update Failed", message)
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {str(e)}")

    def back_to_main(self):
        """Return to main screen"""
        print("BACK TO MAIN CLICKED!")  # Debug
        self.root.destroy()
        if self.parent_window:
            self.parent_window.deiconify()
            self.parent_window.focus_set()

    def on_close(self):
        """Handle window closing"""
        self.back_to_main()

    def display(self):
        """Display the screen"""
        if hasattr(self, 'root'):
            self.root.mainloop()