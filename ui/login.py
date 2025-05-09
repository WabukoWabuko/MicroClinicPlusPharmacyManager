from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from db.database import Database

class LoginWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        layout.addLayout(form_layout)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        layout.addStretch()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        user = self.db.authenticate_user(username, password)
        if user:
            self.main_window.current_user = user
            self.main_window.show_menu()
            self.username_input.clear()
            self.password_input.clear()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
