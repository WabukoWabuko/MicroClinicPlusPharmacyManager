from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from datetime import datetime, timedelta
import pytz

class LoginWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.quotes = [
            '"Health is wealth - Prioritize your well-being"',
            '"A healthy outside starts from the inside."',
            '"The greatest wealth is health."',
            '"Take care of your body, it’s the only place you have to live."',
            '"Good health and good sense are two of life’s greatest blessings."',
            '"To keep the body in good health is a duty."',
            '"Health is not valued till sickness comes."'
        ]
        self.current_quote_index = 0
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        # Title
        self.set_title("Login")
        title = QLabel("MicroClinic Plus Pharmacy Manager")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; margin: 20px;")
        main_layout.addWidget(title)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            logo_label.setText("Clinic Logo")
            logo_label.setStyleSheet("font-size: 18px; color: #4CAF50; margin: 20px;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(logo_label)

        # Dynamic Quote
        self.quote_label = QLabel(self.quotes[self.current_quote_index])
        self.quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quote_label.setStyleSheet("font-size: 14px; color: #FFFFFF; font-style: italic; margin: 10px;")
        main_layout.addWidget(self.quote_label)

        # Username
        username_layout = QHBoxLayout()
        username_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
                min-width: 250px;
            }
        """)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        main_layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        password_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
                min-width: 250px;
            }
        """)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)

        # Activation Code Input (shown if not activated and demo expired)
        self.activation_layout = QHBoxLayout()
        self.activation_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        activation_label = QLabel("Activation Code:")
        activation_label.setStyleSheet("font-size: 16px; color: #FFFFFF; padding: 5px;")
        self.activation_input = QLineEdit()
        self.activation_input.setPlaceholderText("Enter activation code")
        self.activation_input.setEchoMode(QLineEdit.EchoMode.Password)  # Conceal with asterisks
        self.activation_input.setToolTip("Enter the activation code to unlock the system")
        self.activation_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                font-size: 16px;
                background-color: #2E2E2E;
                color: #FFFFFF;
                min-width: 250px;
            }
        """)
        self.activation_layout.addWidget(activation_label)
        self.activation_layout.addWidget(self.activation_input)

        # Only add activation layout if needed
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            main_layout.addLayout(self.activation_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
                margin: 5px;
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
                margin: 5px;
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
                margin: 5px;
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

        # Activate Button (shown if not activated and demo expired)
        self.activate_button = QPushButton("Activate")
        self.activate_button.setToolTip("Activate the system with the code")
        self.activate_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: #FFFFFF;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #1e88e5;
            }
            QPushButton:pressed {
                background-color: #1976d2;
            }
        """)
        self.activate_button.clicked.connect(self.activate_system)
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            button_layout.addWidget(self.activate_button)

        main_layout.addLayout(button_layout)

        # Set up a QTimer to change quotes every minute (60 seconds)
        self.quote_timer = QTimer(self)
        self.quote_timer.timeout.connect(self.update_quote)
        self.quote_timer.start(60000)

        main_layout.addStretch()

        # Schedule the demo period warning to appear after a short delay (1 second)
        QTimer.singleShot(1000, self.show_demo_warning)

    def show_demo_warning(self):
        """Show a warning about the remaining demo period if applicable."""
        if not self.main_window.db.is_system_activated() and self.main_window.db.is_demo_period_active():
            config = self.main_window.db.load_config()
            first_launch_str = config.get("first_launch_date")
            if first_launch_str:
                try:
                    first_launch = datetime.strptime(first_launch_str, "%Y-%m-%d %H:%M:%S")
                    first_launch = pytz.timezone('Africa/Nairobi').localize(first_launch)
                    current_time = datetime.now(pytz.timezone('Africa/Nairobi'))
                    demo_duration = timedelta(days=7)
                    demo_end = first_launch + demo_duration
                    remaining_time = demo_end - current_time
                    if remaining_time.total_seconds() > 0:  # Only show if demo hasn't expired
                        days = remaining_time.days
                        hours = remaining_time.seconds // 3600
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Demo Period Warning")
                        msg.setText(f"Demo period active. {days} days and {hours} hours remaining.")
                        msg.setIcon(QMessageBox.Icon.Warning)  # Set warning icon
                        msg.setStyleSheet("""
                            QMessageBox {
                                background-color: #808080;  /* Gray background */
                                color: #FFFFFF;  /* White text */
                            }
                            QLabel {
                                color: #FFFFFF;  /* White text for the message */
                            }
                            QAbstractButton {
                                background-color: #555555;  /* Dark gray button background */
                                color: #FFFFFF;  /* White button text */
                                border: 1px solid #FFFFFF;  /* White border */
                                border-radius: 5px;
                                padding: 5px 10px;
                            }
                            QAbstractButton:hover {
                                background-color: #FF0000;  /* Red background on hover */
                            }
                            QAbstractButton:pressed {
                                background-color: #CC0000;  /* Darker red when pressed */
                            }
                            .QMessageBox QLabel[objectName="qt_msgbox_label"] {
                                qproperty-alignment: AlignCenter;  /* Center the text */
                            }
                            .QMessageBox QAbstractButton#warning {
                                background-color: #FF0000;  /* Red warning icon */
                                border: 1px solid #FF0000;
                                border-radius: 5px;
                            }
                        """)
                        msg.setStandardButtons(QMessageBox.StandardButton.Close)  # Add a Close button
                        msg.show()
                        QTimer.singleShot(5000, msg.close)  # Close after 5 seconds if not dismissed manually
                except ValueError as e:
                    print(f"Error parsing first_launch_date for demo warning: {e}")

    def update_quote(self):
        """Update the quote to the next one in the list, cycling through."""
        self.current_quote_index = (self.current_quote_index + 1) % len(self.quotes)
        self.quote_label.setText(self.quotes[self.current_quote_index])

    def set_title(self, title):
        self.main_window.set_title(title)

    def login(self):
        # Check demo period and activation status
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            msg = QMessageBox(self)
            msg.setWindowTitle("Demo Expired")
            msg.setText("The demo period has expired. Please enter the activation code to continue.")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #F44336;  /* Red background for critical */
                    color: #FFFFFF;  /* White text */
                }
                QLabel {
                    color: #FFFFFF;  /* White text for the message */
                }
                QAbstractButton {
                    background-color: #555555;  /* Dark gray button background */
                    color: #FFFFFF;  /* White button text */
                    border: 1px solid #FFFFFF;  /* White border */
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QAbstractButton:hover {
                    background-color: #FF0000;  /* Red background on hover */
                }
                QAbstractButton:pressed {
                    background-color: #CC0000;  /* Darker red when pressed */
                }
            """)
            msg.setStandardButtons(QMessageBox.StandardButton.Close)
            msg.show()
            QTimer.singleShot(5000, msg.close)
            return

        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            msg = QMessageBox(self)
            msg.setWindowTitle("Input Error")
            msg.setText("Username and password cannot be empty.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #FF9800;  /* Orange background for warning */
                    color: #212121;  /* Dark text */
                }
                QLabel {
                    color: #212121;  /* Dark text for the message */
                }
                QAbstractButton {
                    background-color: #555555;  /* Dark gray button background */
                    color: #FFFFFF;  /* White button text */
                    border: 1px solid #FFFFFF;  /* White border */
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QAbstractButton:hover {
                    background-color: #FF0000;  /* Red background on hover */
                }
                QAbstractButton:pressed {
                    background-color: #CC0000;  /* Darker red when pressed */
                }
            """)
            msg.setStandardButtons(QMessageBox.StandardButton.Close)
            msg.show()
            QTimer.singleShot(5000, msg.close)
            return

        user = self.main_window.db.authenticate_user(username, password)
        if user:
            self.main_window.current_user = user
            self.main_window.show_menu()
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle("Login Failed")
            msg.setText("Invalid username or password.")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #F44336;  /* Red background for critical */
                    color: #FFFFFF;  /* White text */
                }
                QLabel {
                    color: #FFFFFF;  /* White text for the message */
                }
                QAbstractButton {
                    background-color: #555555;  /* Dark gray button background */
                    color: #FFFFFF;  /* White button text */
                    border: 1px solid #FFFFFF;  /* White border */
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QAbstractButton:hover {
                    background-color: #FF0000;  /* Red background on hover */
                }
                QAbstractButton:pressed {
                    background-color: #CC0000;  /* Darker red when pressed */
                }
            """)
            msg.setStandardButtons(QMessageBox.StandardButton.Close)
            msg.show()
            QTimer.singleShot(5000, msg.close)
            self.clear_fields()

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()
        if hasattr(self, "activation_input"):
            self.activation_input.clear()

    def activate_system(self):
        code = self.activation_input.text().strip()
        if not code:
            msg = QMessageBox(self)
            msg.setWindowTitle("Input Error")
            msg.setText("Activation code cannot be empty.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #FF9800;  /* Orange background for warning */
                    color: #212121;  /* Dark text */
                }
                QLabel {
                    color: #212121;  /* Dark text for the message */
                }
                QAbstractButton {
                    background-color: #555555;  /* Dark gray button background */
                    color: #FFFFFF;  /* White button text */
                    border: 1px solid #FFFFFF;  /* White border */
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QAbstractButton:hover {
                    background-color: #FF0000;  /* Red background on hover */
                }
                QAbstractButton:pressed {
                    background-color: #CC0000;  /* Darker red when pressed */
                }
            """)
            msg.setStandardButtons(QMessageBox.StandardButton.Close)
            msg.show()
            QTimer.singleShot(5000, msg.close)
            return

        if self.main_window.db.activate_system(code):
            msg = QMessageBox(self)
            msg.setWindowTitle("Success")
            msg.setText("System activated successfully! Please log in again.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #4CAF50;  /* Green background for success */
                    color: #FFFFFF;  /* White text */
                }
                QLabel {
                    color: #FFFFFF;  /* White text for the message */
                }
                QAbstractButton {
                    background-color: #555555;  /* Dark gray button background */
                    color: #FFFFFF;  /* White button text */
                    border: 1px solid #FFFFFF;  /* White border */
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QAbstractButton:hover {
                    background-color: #FF0000;  /* Red background on hover */
                }
                QAbstractButton:pressed {
                    background-color: #CC0000;  /* Darker red when pressed */
                }
            """)
            msg.setStandardButtons(QMessageBox.StandardButton.Close)
            msg.show()
            QTimer.singleShot(5000, msg.close)
            # Remove activation input and button
            for i in reversed(range(self.activation_layout.count())):
                self.activation_layout.itemAt(i).widget().setParent(None)
            self.activate_button.setParent(None)
            self.main_window.show_login()
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle("Activation Failed")
            msg.setText("Invalid activation code.")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #F44336;  /* Red background for critical */
                    color: #FFFFFF;  /* White text */
                }
                QLabel {
                    color: #FFFFFF;  /* White text for the message */
                }
                QAbstractButton {
                    background-color: #555555;  /* Dark gray button background */
                    color: #FFFFFF;  /* White button text */
                    border: 1px solid #FFFFFF;  /* White border */
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QAbstractButton:hover {
                    background-color: #FF0000;  /* Red background on hover */
                }
                QAbstractButton:pressed {
                    background-color: #CC0000;  /* Darker red when pressed */
                }
            """)
            msg.setStandardButtons(QMessageBox.StandardButton.Close)
            msg.show()
            QTimer.singleShot(5000, msg.close)
            self.clear_fields()
