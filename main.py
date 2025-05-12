import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt
from ui.login import LoginWidget
from ui.patient_management import PatientManagementWidget
from ui.prescription_logging import PrescriptionLoggingWidget
from ui.inventory_management import InventoryManagementWidget
from ui.sales_management import SalesManagementWidget
from ui.user_management import UserManagementWidget
from ui.reporting_dashboard import ReportingDashboardWidget
from ui.settings import SettingsWidget
from db.database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MicroClinicPlus Pharmacy Manager")
        self.db = Database()
        self.current_user = None
        self.is_high_contrast = False
        self.init_ui()

    def init_ui(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_widget = LoginWidget(self)
        self.menu_widget = QWidget()
        self.patient_management_widget = PatientManagementWidget(self)
        self.prescription_logging_widget = PrescriptionLoggingWidget(self)
        self.inventory_management_widget = InventoryManagementWidget(self)
        self.sales_management_widget = SalesManagementWidget(self)
        self.user_management_widget = UserManagementWidget(self)
        self.reporting_dashboard_widget = ReportingDashboardWidget(self)
        self.settings_widget = SettingsWidget(self)

        self.central_widget.addWidget(self.login_widget)
        self.central_widget.addWidget(self.menu_widget)
        self.central_widget.addWidget(self.patient_management_widget)
        self.central_widget.addWidget(self.prescription_logging_widget)
        self.central_widget.addWidget(self.inventory_management_widget)
        self.central_widget.addWidget(self.sales_management_widget)
        self.central_widget.addWidget(self.user_management_widget)
        self.central_widget.addWidget(self.reporting_dashboard_widget)
        self.central_widget.addWidget(self.settings_widget)

        self.setup_menu()
        self.central_widget.setCurrentWidget(self.login_widget)
        self.setMinimumSize(800, 600)

    def setup_menu(self):
        layout = QVBoxLayout()
        self.menu_widget.setLayout(layout)

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """

        logout_button_style = """
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c11307;
            }
        """

        contrast_button_style = """
            QPushButton {
                background-color: #555555;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """

        buttons = [
            ("Patient Management", self.show_patient_management, button_style),
            ("Prescription Logging", self.show_prescription_logging, button_style),
            ("Inventory Management", self.show_inventory_management, button_style),
            ("Sales Management", self.show_sales_management, button_style),
            ("User Management", self.show_user_management, button_style),
            ("Reporting Dashboard", self.show_reporting_dashboard, button_style),
            ("Settings", self.show_settings, button_style),
            ("Logout", self.logout, logout_button_style),
            ("Toggle High Contrast", self.toggle_high_contrast, contrast_button_style)
        ]

        for text, slot, style in buttons:
            button = QPushButton(text)
            button.setStyleSheet(style)
            button.clicked.connect(slot)
            layout.addWidget(button)

        layout.addStretch()

    def show_menu(self):
        self.central_widget.setCurrentWidget(self.menu_widget)

    def show_patient_management(self):
        self.central_widget.setCurrentWidget(self.patient_management_widget)

    def show_prescription_logging(self):
        self.central_widget.setCurrentWidget(self.prescription_logging_widget)

    def show_inventory_management(self):
        self.central_widget.setCurrentWidget(self.inventory_management_widget)

    def show_sales_management(self):
        self.central_widget.setCurrentWidget(self.sales_management_widget)

    def show_user_management(self):
        self.central_widget.setCurrentWidget(self.user_management_widget)

    def show_reporting_dashboard(self):
        self.central_widget.setCurrentWidget(self.reporting_dashboard_widget)

    def show_settings(self):
        self.central_widget.setCurrentWidget(self.settings_widget)

    def logout(self):
        self.current_user = None
        self.central_widget.setCurrentWidget(self.login_widget)

    def toggle_high_contrast(self):
        self.is_high_contrast = not self.is_high_contrast
        style = """
            QWidget {
                background-color: black;
                color: white;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #222222;
                color: white;
                border: 1px solid white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """ if self.is_high_contrast else ""
        self.setStyleSheet(style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
