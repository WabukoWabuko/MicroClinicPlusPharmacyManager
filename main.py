from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from ui.login import LoginWidget
from ui.patient_management import PatientManagementWidget
from ui.inventory_management import InventoryManagementWidget
from ui.prescription_logging import PrescriptionLoggingWidget
from ui.sales_management import SalesManagementWidget
from ui.user_management import UserManagementWidget
from ui.settings import SettingsWidget
from ui.reporting_dashboard import ReportingDashboardWidget
from db.database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MicroClinic Plus Pharmacy Manager")
        self.setGeometry(100, 100, 800, 600)
        self.db = Database()
        self.config = self.db.load_config()
        self.current_user = None
        self.is_high_contrast = False
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.layout.addWidget(self.content_widget)

        self.show_login()

    def show_login(self):
        self.clear_content()
        login_widget = LoginWidget(self)
        self.content_layout.addWidget(login_widget)
        self.set_title("Login")

    def show_menu(self):
        self.clear_content()
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)

        self.set_title("Menu")
        title = QLabel("MicroClinic Plus Pharmacy Manager")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF; margin: 10px;")
        menu_layout.addWidget(title)

        card = QWidget()
        card_layout = QVBoxLayout(card)
        card.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            }
        """)

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 200px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """

        patient_button = QPushButton("Patient Management")
        patient_button.setStyleSheet(button_style)
        patient_button.setToolTip("Manage patient records")
        patient_button.clicked.connect(self.show_patient_management)
        card_layout.addWidget(patient_button)

        inventory_button = QPushButton("Inventory Management")
        inventory_button.setStyleSheet(button_style)
        inventory_button.setToolTip("Manage drug inventory")
        inventory_button.clicked.connect(self.show_inventory_management)
        card_layout.addWidget(inventory_button)

        prescription_button = QPushButton("Prescription Logging")
        prescription_button.setStyleSheet(button_style)
        prescription_button.setToolTip("Log prescriptions")
        prescription_button.clicked.connect(self.show_prescription_logging)
        card_layout.addWidget(prescription_button)

        sales_button = QPushButton("Sales Management")
        sales_button.setStyleSheet(button_style)
        sales_button.setToolTip("Manage sales")
        sales_button.clicked.connect(self.show_sales_management)
        card_layout.addWidget(sales_button)

        if self.current_user and self.current_user['role'] == 'admin':
            user_button = QPushButton("User Management")
            user_button.setStyleSheet(button_style)
            user_button.setToolTip("Manage users (Admin only)")
            user_button.clicked.connect(self.show_user_management)
            card_layout.addWidget(user_button)

        settings_button = QPushButton("Settings")
        settings_button.setStyleSheet(button_style)
        settings_button.setToolTip("Configure application settings")
        settings_button.clicked.connect(self.show_settings)
        card_layout.addWidget(settings_button)

        dashboard_button = QPushButton("Reporting Dashboard")
        dashboard_button.setStyleSheet(button_style)
        dashboard_button.setToolTip("View reports and analytics")
        dashboard_button.clicked.connect(self.show_dashboard)
        card_layout.addWidget(dashboard_button)

        contrast_button = QPushButton("Toggle High Contrast")
        contrast_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 200px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        contrast_button.setToolTip("Toggle high contrast mode")
        contrast_button.clicked.connect(self.toggle_contrast)
        card_layout.addWidget(contrast_button)

        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 200px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c1170a;
            }
        """)
        logout_button.setToolTip("Log out of the application")
        logout_button.clicked.connect(self.show_login)
        card_layout.addWidget(logout_button)

        card_layout.addStretch()
        menu_layout.addWidget(card)
        self.content_layout.addWidget(menu_widget)

    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_patient_management(self):
        self.clear_content()
        widget = PatientManagementWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Patient Management")

    def show_inventory_management(self):
        self.clear_content()
        widget = InventoryManagementWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Inventory Management")

    def show_prescription_logging(self):
        self.clear_content()
        widget = PrescriptionLoggingWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Prescription Logging")

    def show_sales_management(self):
        self.clear_content()
        widget = SalesManagementWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Sales Management")

    def show_user_management(self):
        self.clear_content()
        widget = UserManagementWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("User Management")

    def show_settings(self):
        self.clear_content()
        widget = SettingsWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Settings")

    def show_dashboard(self):
        self.clear_content()
        widget = ReportingDashboardWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Reporting Dashboard")

    def toggle_contrast(self):
        self.is_high_contrast = not self.is_high_contrast
        if self.is_high_contrast:
            self.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        else:
            self.setStyleSheet("")
        self.show_menu()

    def set_title(self, title):
        self.setWindowTitle(f"MicroClinic Plus Pharmacy Manager - {title}")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.setStyleSheet("background-color: #000000; color: #FFFFFF;")
    window.show()
    app.exec()
