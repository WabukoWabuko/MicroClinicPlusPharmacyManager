import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from ui.patient_management import PatientManagementWidget
from ui.prescription_logging import PrescriptionLoggingWidget
from ui.inventory_management import InventoryManagementWidget
from ui.sales_management import SalesManagementWidget
from ui.login import LoginWidget
from ui.reporting_dashboard import ReportingDashboardWidget
from ui.user_management import UserManagementWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MicroClinicPlusPharmacyManager")
        self.setGeometry(100, 100, 800, 600)
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout()
        main_widget.setLayout(self.main_layout)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.login = LoginWidget(self)
        self.menu_widget = QWidget()
        self.patient_management = PatientManagementWidget(self)
        self.prescription_logging = PrescriptionLoggingWidget(self)
        self.inventory_management = InventoryManagementWidget(self)
        self.sales_management = SalesManagementWidget(self)
        self.reporting_dashboard = ReportingDashboardWidget(self)
        self.user_management = UserManagementWidget(self)

        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.addWidget(self.menu_widget)
        self.stacked_widget.addWidget(self.patient_management)
        self.stacked_widget.addWidget(self.prescription_logging)
        self.stacked_widget.addWidget(self.inventory_management)
        self.stacked_widget.addWidget(self.sales_management)
        self.stacked_widget.addWidget(self.reporting_dashboard)
        self.stacked_widget.addWidget(self.user_management)

        self.stacked_widget.setCurrentWidget(self.login)

    def setup_menu(self):
        """Set up the menu based on the user's role."""
        # Clear existing menu layout
        old_layout = self.menu_widget.layout()
        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.menu_widget.setLayout(None)

        # Create new layout
        menu_layout = QVBoxLayout()
        self.menu_widget.setLayout(menu_layout)

        # Common buttons for all roles
        patient_button = QPushButton("Patient Management")
        prescription_button = QPushButton("Prescription Logging")
        sales_button = QPushButton("Sales Management")
        patient_button.clicked.connect(self.show_patient_management)
        prescription_button.clicked.connect(self.show_prescription_logging)
        sales_button.clicked.connect(self.show_sales_management)
        menu_layout.addWidget(patient_button)
        menu_layout.addWidget(prescription_button)
        menu_layout.addWidget(sales_button)

        # Admin-only buttons
        if self.current_user['role'] == 'admin':
            inventory_button = QPushButton("Inventory Management")
            reporting_button = QPushButton("Reporting Dashboard")
            user_management_button = QPushButton("User Management")
            inventory_button.clicked.connect(self.show_inventory_management)
            reporting_button.clicked.connect(self.show_reporting_dashboard)
            user_management_button.clicked.connect(self.show_user_management)
            menu_layout.addWidget(inventory_button)
            menu_layout.addWidget(reporting_button)
            menu_layout.addWidget(user_management_button)

        # Logout button
        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.logout)
        menu_layout.addWidget(logout_button)
        menu_layout.addStretch()

    def show_patient_management(self):
        self.stacked_widget.setCurrentWidget(self.patient_management)

    def show_prescription_logging(self):
        self.stacked_widget.setCurrentWidget(self.prescription_logging)

    def show_inventory_management(self):
        if self.current_user['role'] == 'admin':
            self.stacked_widget.setCurrentWidget(self.inventory_management)

    def show_sales_management(self):
        self.stacked_widget.setCurrentWidget(self.sales_management)

    def show_reporting_dashboard(self):
        if self.current_user['role'] == 'admin':
            self.stacked_widget.setCurrentWidget(self.reporting_dashboard)

    def show_user_management(self):
        if self.current_user['role'] == 'admin':
            self.stacked_widget.setCurrentWidget(self.user_management)

    def show_menu(self):
        self.setup_menu()
        self.stacked_widget.setCurrentWidget(self.menu_widget)

    def logout(self):
        self.current_user = None
        self.stacked_widget.setCurrentWidget(self.login)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
