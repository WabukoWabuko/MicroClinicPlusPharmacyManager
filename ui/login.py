from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

class LoginWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = self.main_window.db  # Access database from MainWindow
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Username and password inputs
        form_layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setToolTip("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setToolTip("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)

        form_layout.addWidget(QLabel("Username:"))
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(QLabel("Password:"))
        form_layout.addWidget(self.password_input)
        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        login_button = QPushButton("Login")
        login_button.setToolTip("Log in to the system")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        toggle_contrast_button = QPushButton("Toggle High Contrast")
        toggle_contrast_button.setToolTip("Switch to high-contrast mode")
        toggle_contrast_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        login_button.clicked.connect(self.login)
        toggle_contrast_button.clicked.connect(self.main_window.toggle_high_contrast)
        button_layout.addWidget(login_button)
        button_layout.addWidget(toggle_contrast_button)
        main_layout.addLayout(button_layout)

        main_layout.addStretch()

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
            QMessageBox.warning(self, "Error", "Invalid username or password.")
