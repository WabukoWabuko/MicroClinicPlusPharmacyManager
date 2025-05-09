from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from db.database import Database
from utils.validation import is_valid_username, is_valid_password
import qtawesome as qta

class LoginWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setToolTip("Enter your username")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setToolTip("Enter your password (min 8 characters)")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Login button
        login_button = QPushButton("Login")
        login_button.setIcon(qta.icon('mdi.login'))
        login_button.setToolTip("Log in to the system")
        login_button.clicked.connect(self.login)
        login_button.setDefault(True)  # Enable Enter key
        layout.addWidget(login_button)

        layout.addStretch()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        self.username_input.setStyleSheet("")
        self.password_input.setStyleSheet("")

        is_valid, error = is_valid_username(username)
        if not is_valid:
            self.username_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_password(password)
        if not is_valid:
            self.password_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        user = self.db.authenticate_user(username, password)
        if user:
            self.main_window.current_user = user
            self.main_window.show_menu()
        else:
            self.username_input.setStyleSheet("border: 1px solid red;")
            self.password_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", "Invalid username or password.")
