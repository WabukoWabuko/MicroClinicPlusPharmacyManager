from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from db.database import Database
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
        self.db = Database()  # Initialize database
        self.current_user = None
        self.high_contrast = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MicroClinicPlus Pharmacy Manager")
        self.setMinimumSize(800, 600)

        # Central widget with stacked layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Initialize UI widgets
        self.login_widget = LoginWidget(self)
        self.patient_management = PatientManagementWidget(self)
        self.prescription_logging = PrescriptionLoggingWidget(self)
        self.inventory_management = InventoryManagementWidget(self)
        self.sales_management = SalesManagementWidget(self)
        self.user_management = UserManagementWidget(self)
        self.reporting_dashboard = ReportingDashboardWidget(self)
        self.menu_widget = self.create_menu_widget()

        # Add widgets to stack
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.menu_widget)
        self.stack.addWidget(self.patient_management)
        self.stack.addWidget(self.prescription_logging)
        self.stack.addWidget(self.inventory_management)
        self.stack.addWidget(self.sales_management)
        self.stack.addWidget(self.user_management)
        self.stack.addWidget(self.reporting_dashboard)

        # Show login screen initially
        self.show_login()

    def create_menu_widget(self):
        menu_widget = QWidget()
        layout = QVBoxLayout()
        menu_widget.setLayout(layout)

        # Menu buttons
        buttons = [
            ("Patient Management", self.show_patient_management, "#4CAF50"),
            ("Prescription Logging", self.show_prescription_logging, "#4CAF50"),
            ("Inventory Management", self.show_inventory_management, "#4CAF50"),
            ("Sales Management", self.show_sales_management, "#4CAF50"),
            ("User Management", self.show_user_management, "#4CAF50"),
            ("Reporting Dashboard", self.show_reporting_dashboard, "#4CAF50"),
            ("Toggle High Contrast", self.toggle_high_contrast, "#555555"),
            ("Logout", self.show_login, "#f44336")
        ]

        for text, slot, color in buttons:
            button = QPushButton(text)
            button.setToolTip(f"{text}")
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    margin: 5px;
                }}
                QPushButton:hover {{
                    background-color: {self.lighten_color(color)};
                }}
                QPushButton:pressed {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            button.clicked.connect(slot)
            layout.addWidget(button)

        layout.addStretch()
        return menu_widget

    def lighten_color(self, hex_color):
        color = int(hex_color[1:], 16)
        r = min(255, ((color >> 16) & 255) + 20)
        g = min(255, ((color >> 8) & 255) + 20)
        b = min(255, (color & 255) + 20)
        return f"#{r:02x}{g:02x}{b:02x}"

    def darken_color(self, hex_color):
        color = int(hex_color[1:], 16)
        r = max(0, ((color >> 16) & 255) - 20)
        g = max(0, ((color >> 8) & 255) - 20)
        b = max(0, (color & 255) - 20)
        return f"#{r:02x}{g:02x}{b:02x}"

    def show_login(self):
        self.current_user = None
        self.stack.setCurrentWidget(self.login_widget)

    def show_menu(self):
        if self.current_user:
            self.stack.setCurrentWidget(self.menu_widget)

    def show_patient_management(self):
        if self.current_user:
            self.stack.setCurrentWidget(self.patient_management)

    def show_prescription_logging(self):
        if self.current_user:
            self.stack.setCurrentWidget(self.prescription_logging)

    def show_inventory_management(self):
        if self.current_user:
            self.stack.setCurrentWidget(self.inventory_management)

    def show_sales_management(self):
        if self.current_user:
            self.stack.setCurrentWidget(self.sales_management)

    def show_user_management(self):
        if self.current_user:
            self.stack.setCurrentWidget(self.user_management)

    def show_reporting_dashboard(self):
        if self.current_user:
            self.stack.setCurrentWidget(self.reporting_dashboard)

    def toggle_high_contrast(self):
        self.high_contrast = not self.high_contrast
        if self.high_contrast:
            self.setStyleSheet("""
                QWidget {
                    background-color: black;
                    color: white;
                }
                QLineEdit, QComboBox, QTextEdit {
                    background-color: #333;
                    color: white;
                    border: 1px solid white;
                }
                QTableWidget {
                    background-color: #333;
                    color: white;
                    gridline-color: white;
                }
            """)
        else:
            self.setStyleSheet("")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
