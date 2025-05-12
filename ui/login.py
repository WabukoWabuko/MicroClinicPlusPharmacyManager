from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

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
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF; margin: 10px;")
        main_layout.addWidget(title)

        # Logo and Quote Card
        card = QWidget()
        card_layout = QVBoxLayout(card)
        card.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        logo_label = QLabel("Clinic Logo")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("font-size: 14px; color: #4CAF50; margin: 10px;")
        card_layout.addWidget(logo_label)
        quote_label = QLabel('"Health is wealth - Prioritize your well-being"')
        quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quote_label.setStyleSheet("font-size: 12px; color: #FFFFFF; italic; margin: 10px;")
        card_layout.addWidget(quote_label)
        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

        # Login Form Card
        form_card = QWidget()
        form_layout = QVBoxLayout(form_card)
        form_card.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-size: 14px; color: #FFFFFF;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setToolTip("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                font-size: 14px;
                background-color: #2E2E2E;
                color: #FFFFFF;
                max-width: 200px;
            }
        """)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        username_layout.addStretch()
        form_layout.addLayout(username_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-size: 14px; color: #FFFFFF;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setToolTip("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                font-size: 14px;
                background-color: #2E2E2E;
                color: #FFFFFF;
                max-width: 200px;
            }
        """)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        password_layout.addStretch()
        form_layout.addLayout(password_layout)

        main_layout.addWidget(form_card, alignment=Qt.AlignmentFlag.AlignCenter)

        # Buttons Card
        button_card = QWidget()
        button_layout = QHBoxLayout(button_card)
        button_card.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        login_button = QPushButton("Login")
        login_button.setToolTip("Log in to the application")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 120px;
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
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 120px;
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
        button_layout.addStretch()
        main_layout.addWidget(button_card, alignment=Qt.AlignmentFlag.AlignCenter)

        # Toggle Contrast Card
        toggle_card = QWidget()
        toggle_layout = QHBoxLayout(toggle_card)
        toggle_card.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        toggle_contrast_button = QPushButton("Toggle High Contrast")
        toggle_contrast_button.setToolTip("Toggle high contrast mode")
        toggle_contrast_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        toggle_contrast_button.clicked.connect(self.main_window.toggle_contrast)
        toggle_layout.addWidget(toggle_contrast_button)
        toggle_layout.addStretch()
        main_layout.addWidget(toggle_card, alignment=Qt.AlignmentFlag.AlignCenter)

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
