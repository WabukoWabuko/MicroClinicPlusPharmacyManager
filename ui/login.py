from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class LoginWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title
        self.set_title("Login")
        title = QLabel("MicroClinic Plus Pharmacy Manager")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; margin: 30px;")
        main_layout.addWidget(title)

        # Logo and Quote
        logo_label = QLabel()
        pixmap = QPixmap("database/logo.png")  # Replace with your image path
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            logo_label.setText("Clinic Logo")
            logo_label.setStyleSheet("font-size: 18px; color: #4CAF50; margin: 20px;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(logo_label)

        quote_label = QLabel('"Health is wealth - Prioritize your well-being"')
        quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quote_label.setStyleSheet("font-size: 14px; color: #FFFFFF; font-style: italic; margin: 20px;")
        main_layout.addWidget(quote_label)

        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-size: 16px; color: #FFFFFF; padding: 5px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setToolTip("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                font-size: 16px;
                background-color: #2E2E2E;
                color: #FFFFFF;
                min-width: 300px;
            }
        """)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        username_layout.addStretch()
        main_layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-size: 16px; color: #FFFFFF; padding: 5px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setToolTip("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                font-size: 16px;
                background-color: #2E2E2E;
                color: #FFFFFF;
                min-width: 300px;
            }
        """)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        password_layout.addStretch()
        main_layout.addLayout(password_layout)

        # Buttons
        button_layout = QHBoxLayout()
        login_button = QPushButton("Login")
        login_button.setToolTip("Log in to the application")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        login_button.clicked.connect(self.login)
        button_layout.addWidget(login_button)

        clear_button = QPushButton("Clear")
        clear_button.setToolTip("Clear username and password fields")
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: #FFFFFF;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c1170a;
            }
        """)
        clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(clear_button)

        toggle_contrast_button = QPushButton("Toggle High Contrast")
        toggle_contrast_button.setToolTip("Toggle high contrast mode")
        toggle_contrast_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        toggle_contrast_button.clicked.connect(self.main_window.toggle_contrast)
        button_layout.addWidget(toggle_contrast_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        main_layout.addStretch()

    def set_title(self, title):
        self.main_window.set_title(title)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")
            return
        user = self.main_window.db.authenticate_user(username, password)
        if user:
            self.main_window.current_user = user
            self.main_window.show_menu()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
            self.clear_fields()

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()
