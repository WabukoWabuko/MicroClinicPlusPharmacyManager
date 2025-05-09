import sys
import qtawesome as qta
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from ui.login import LoginWidget
from ui.patient_management import PatientManagementWidget
from ui.prescription_logging import PrescriptionLoggingWidget
from ui.inventory_management import InventoryManagementWidget
from ui.sales_management import SalesManagementWidget
from ui.user_management import UserManagementWidget
from ui.reporting_dashboard import ReportingDashboardWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.high_contrast = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MicroClinicPlus Pharmacy Manager")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Initialize widgets
        self.login_widget = LoginWidget(self)
        self.patient_management = PatientManagementWidget(self)
        self.prescription_logging = PrescriptionLoggingWidget(self)
        self.inventory_management = InventoryManagementWidget(self)
        self.sales_management = SalesManagementWidget(self)
        self.user_management = UserManagementWidget(self)
        self.reporting_dashboard = ReportingDashboardWidget(self)

        # Apply stylesheet
        self.apply_stylesheet()

        # Show login
        self.show_login()

    def apply_stylesheet(self):
        """Apply global stylesheet based on contrast mode."""
        normal_style = """
            QWidget {
                font-family: Roboto, sans-serif;
                font-size: 14px;
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QLineEdit:invalid, QTextEdit:invalid {
                border: 1px solid red;
            }
            QTableWidget {
                gridline-color: #ccc;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
            }
            QLabel {
                color: #333;
            }
        """
        high_contrast_style = """
            QWidget {
                font-family: Roboto, sans-serif;
                font-size: 14px;
                background-color: black;
                color: white;
            }
            QPushButton {
                background-color: #00ff00;
                color: black;
                border: 2px solid white;
                border-radius: 5px;
                padding: 8px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
            QLineEdit, QTextEdit, QComboBox {
                border: 2px solid white;
                border-radius: 4px;
                padding: 5px;
                background-color: black;
                color: white;
            }
            QLineEdit:invalid, QTextEdit:invalid {
                border: 2px solid red;
            }
            QTableWidget {
                gridline-color: white;
                background-color: black;
                color: white;
            }
            QHeaderView::section {
                background-color: #00ff00;
                color: black;
                padding: 5px;
                border: 1px solid white;
            }
            QLabel {
                color: white;
            }
        """
        self.setStyleSheet(high_contrast_style if self.high_contrast else normal_style)

    def toggle_high_contrast(self):
        """Toggle high-contrast mode."""
        self.high_contrast = not self.high_contrast
        self.apply_stylesheet()
        # Re-apply current widget to refresh
        current_widget = self.layout.itemAt(0).widget()
        if current_widget:
            self.layout.removeWidget(current_widget)
            self.layout.addWidget(current_widget)

    def show_login(self):
        self.clear_layout()
        self.layout.addWidget(self.login_widget)

    def show_menu(self):
        self.clear_layout()
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)

        # Menu buttons with icons
        patient_button = QPushButton("Patient Management")
        patient_button.setIcon(qta.icon('mdi.account-plus'))
        patient_button.clicked.connect(self.show_patient_management)

        prescription_button = QPushButton("Prescription Logging")
        prescription_button.setIcon(qta.icon('mdi.prescription'))
        prescription_button.clicked.connect(self.show_prescription_logging)

        inventory_button = QPushButton("Inventory Management")
        inventory_button.setIcon(qta.icon('mdi.warehouse'))
        inventory_button.clicked.connect(self.show_inventory_management)

        sales_button = QPushButton("Sales & Receipts")
        sales_button.setIcon(qta.icon('mdi.cash-register'))
        sales_button.clicked.connect(self.show_sales_management)

        user_button = QPushButton("User Management")
        user_button.setIcon(qta.icon('mdi.account-group'))
        user_button.clicked.connect(self.show_user_management)

        report_button = QPushButton("Reports")
        report_button.setIcon(qta.icon('mdi.chart-bar'))
        report_button.clicked.connect(self.show_reporting_dashboard)

        contrast_button = QPushButton("Toggle High Contrast")
        contrast_button.setIcon(qta.icon('mdi.contrast'))
        contrast_button.clicked.connect(self.toggle_high_contrast)

        logout_button = QPushButton("Logout")
        logout_button.setIcon(qta.icon('mdi.logout'))
        logout_button.clicked.connect(self.show_login)

        # Role-based access
        if self.current_user['role'] == 'admin':
            menu_layout.addWidget(patient_button)
            menu_layout.addWidget(prescription_button)
            menu_layout.addWidget(inventory_button)
            menu_layout.addWidget(sales_button)
            menu_layout.addWidget(user_button)
            menu_layout.addWidget(report_button)
        else:  # staff
            menu_layout.addWidget(patient_button)
            menu_layout.addWidget(prescription_button)
            menu_layout.addWidget(sales_button)
            menu_layout.addWidget(report_button)

        menu_layout.addWidget(contrast_button)
        menu_layout.addWidget(logout_button)
        menu_layout.addStretch()

        self.layout.addWidget(menu_widget)
        self.check_low_stock_alerts()

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

    def show_patient_management(self):
        self.clear_layout()
        self.layout.addWidget(self.patient_management)

    def show_prescription_logging(self):
        self.clear_layout()
        self.layout.addWidget(self.prescription_logging)

    def show_inventory_management(self):
        if self.current_user['role'] == 'admin':
            self.clear_layout()
            self.layout.addWidget(self.inventory_management)
        else:
            QMessageBox.warning(self, "Access Denied", "Only admins can access inventory management.")

    def show_sales_management(self):
        self.clear_layout()
        self.layout.addWidget(self.sales_management)

    def show_user_management(self):
        if self.current_user['role'] == 'admin':
            self.clear_layout()
            self.layout.addWidget(self.user_management)
        else:
            QMessageBox.warning(self, "Access Denied", "Only admins can access user management.")

    def show_reporting_dashboard(self):
        self.clear_layout()
        self.layout.addWidget(self.reporting_dashboard)

    def check_low_stock_alerts(self):
        if self.current_user['role'] == 'admin':
            low_stock_drugs = self.inventory_management.db.get_low_stock_drugs()
            if low_stock_drugs:
                drugs_list = "\n".join([f"{drug['name']} (Qty: {drug['quantity']})" for drug in low_stock_drugs])
                QMessageBox.warning(self, "Low Stock Alert", f"The following drugs are low in stock:\n{drugs_list}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
