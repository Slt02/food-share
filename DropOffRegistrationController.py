from Database import Database
from GUI.WarningScreen import WarningScreen
from Users.DropOffAgent import DropOffAgent
from tkinter import messagebox

class DropOffRegistrationController:
    def __init__(self, root):
        self.root = root
        self.db = Database()

    # Handle the submission of the registration form
    def submit_form(self, name, surname, username, email, password, phone):
        if self.validate_form(name, surname, username, email, password, phone):
            # Create a new drop-off agent in the database
            drop_off_agent = DropOffAgent(
                username=username,
                name=name,
                surname=surname,
                email=email,
                password=password,
                phone_number=phone
            )
            success = self.db.create_drop_off_agent(drop_off_agent)
            if success:
                messagebox.showinfo("Account Created", "Drop-Off Agent account created successfully.")
            else:
                WarningScreen(self.root, "An account with this email or username already exists.").show_warning()
        else:
            warning_screen = WarningScreen(self.root, "All fields are required. Please fill in all fields.")
            warning_screen.show_warning()

    # Validate the form inputs
    def validate_form(self, name, surname, username, email, password, phone):
        if not name or not surname or not username or not email or not password or not phone:
            return False
        else:
            return True

