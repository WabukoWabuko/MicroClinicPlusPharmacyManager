from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from db.database import Database

class LoginWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Form layout for login fields
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)

        # Login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)

        # Add to main layout
        layout.addLayout(form_layout)
        layout.addWidget(login_button)
        layout.addStretch()

    def login(self):
        """Authenticate user and switch to main menu if successful."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        user = self.db.authenticate_user(username, password)
        if user:
            self.main_window.current_user = user
            self.main_window.show_menu()
            self.clear_form()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def clear_form(self):
        """Clear login inputs."""
        self.username_input.clear()
        self.password_input.clear()
