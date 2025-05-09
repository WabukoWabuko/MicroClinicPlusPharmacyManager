import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from ui.patient_management import PatientManagementWidget
from ui.prescription_logging import PrescriptionLoggingWidget
from ui.inventory_management import InventoryManagementWidget
from ui.sales_management import SalesManagementWidget
from ui.login import LoginWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MicroClinicPlusPharmacyManager")
        self.setGeometry(100, 100, 800, 600)
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        # Main widget and stacked widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout()
        main_widget.setLayout(self.main_layout)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Create pages
        self.login = LoginWidget(self)
        self.menu_widget = QWidget()
        self.patient_management = PatientManagementWidget(self)
        self.prescription_logging = PrescriptionLoggingWidget(self)
        self.inventory_management = InventoryManagementWidget(self)
        self.sales_management = SalesManagementWidget(self)

        # Menu page
        menu_layout = QVBoxLayout()
        self.menu_widget.setLayout(menu_layout)
        patient_button = QPushButton("Patient Management")
        prescription_button = QPushButton("Prescription Logging")
        inventory_button = QPushButton("Inventory Management")
        sales_button = QPushButton("Sales Management")
        logout_button = QPushButton("Logout")
        patient_button.clicked.connect(self.show_patient_management)
        prescription_button.clicked.connect(self.show_prescription_logging)
        inventory_button.clicked.connect(self.show_inventory_management)
        sales_button.clicked.connect(self.show_sales_management)
        logout_button.clicked.connect(self.logout)
        menu_layout.addWidget(patient_button)
        menu_layout.addWidget(prescription_button)
        menu_layout.addWidget(inventory_button)
        menu_layout.addWidget(sales_button)
        menu_layout.addWidget(logout_button)
        menu_layout.addStretch()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.addWidget(self.menu_widget)
        self.stacked_widget.addWidget(self.patient_management)
        self.stacked_widget.addWidget(self.prescription_logging)
        self.stacked_widget.addWidget(self.inventory_management)
        self.stacked_widget.addWidget(self.sales_management)

        # Set initial page to login
        self.stacked_widget.setCurrentWidget(self.login)

    def show_patient_management(self):
        self.stacked_widget.setCurrentWidget(self.patient_management)

    def show_prescription_logging(self):
        self.stacked_widget.setCurrentWidget(self.prescription_logging)

    def show_inventory_management(self):
        self.stacked_widget.setCurrentWidget(self.inventory_management)

    def show_sales_management(self):
        self.stacked_widget.setCurrentWidget(self.sales_management)

    def show_menu(self):
        self.stacked_widget.setCurrentWidget(self.menu_widget)

    def logout(self):
        self.current_user = None
        self.stacked_widget.setCurrentWidget(self.login)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
