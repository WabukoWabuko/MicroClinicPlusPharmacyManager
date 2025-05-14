import subprocess
import socket
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt6.QtCore import Qt, QTimer
from ui.login import LoginWidget
from ui.patient_management import PatientManagementWidget
from ui.inventory_management import InventoryManagementWidget
from ui.prescription_logging import PrescriptionLoggingWidget
from ui.sales_management import SalesManagementWidget
from ui.supplier_management import SupplierManagementWidget
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

        # Title
        self.title = QLabel("MicroClinic Plus Pharmacy Manager")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 19px; font-weight: bold; color: #FFFFFF; margin: 10px;")
        self.layout.addWidget(self.title)

        # Online/offline label
        self.status_label = QLabel("● Checking...")
        self.status_label.setStyleSheet("font-size: 20px; color: #FFFF00; margin: 10px;")
        self.layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.layout.addWidget(self.content_widget)

        # Timer for network status
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status_dot)
        self.status_timer.start(5000)

        self.show_login()

    def is_connected(self):
        """Cross-platform, fast, safe check for internet connection."""
        try:
            socket.create_connection(("1.1.1.1", 53), timeout=2)
            return True
        except OSError:
            return False

    def update_status_dot(self):
        try:
            is_online = self.is_connected()
        except Exception:
            is_online = False

        color = "#00FF00" if is_online else "#FF0000"
        status_text = "Online" if is_online else "Offline"
        self.status_label.setText(f"● {status_text}")
        self.status_label.setStyleSheet(f"font-size: 20px; color: {color}; margin: 10px;")

    def show_login(self):
        self.clear_content()
        login_widget = LoginWidget(self)
        self.content_layout.addWidget(login_widget)
        self.set_title("Login")
        self.update_status_dot()

    def show_menu(self):
        if not self.db.is_system_activated() and not self.db.is_demo_period_active():
            self.show_login()
            return

        self.clear_content()
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)
        self.set_title("Menu")

        button_grid = QGridLayout()
        button_grid.setSpacing(10)

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                width: 120px;
                height: 120px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """

        buttons = [
            ("Patient\nManagement", self.show_patient_management),
            ("Inventory\nManagement", self.show_inventory_management),
            ("Prescription\nLogging", self.show_prescription_logging),
            ("Sales\nManagement", self.show_sales_management),
            ("Supplier\nManagement", self.show_supplier_management),
        ]

        if self.current_user and self.current_user['role'] == 'admin':
            buttons.append(("User\nManagement", self.show_user_management))

        buttons.extend([
            ("Settings", self.show_settings),
            ("Reporting\nDashboard", self.show_dashboard),
        ])

        row, col = 0, 0
        for text, action in buttons:
            button = QPushButton(text)
            button.setStyleSheet(button_style)
            button.setToolTip(f"Navigate to {text.replace(chr(10), ' ')}")
            button.clicked.connect(action)
            button_grid.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        menu_layout.addLayout(button_grid)

        bottom_buttons_layout = QHBoxLayout()

        contrast_button = QPushButton("Toggle High Contrast")
        contrast_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                width: 150px;
                margin: 5px;
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
        bottom_buttons_layout.addWidget(contrast_button)

        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                width: 150px;
                margin: 5px;
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
        bottom_buttons_layout.addWidget(logout_button)

        menu_layout.addLayout(bottom_buttons_layout)
        menu_layout.addStretch()
        self.content_layout.addWidget(menu_widget)
        self.update_status_dot()

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
        self.update_status_dot()

    def show_inventory_management(self):
        self.clear_content()
        widget = InventoryManagementWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Inventory Management")
        self.update_status_dot()

    def show_prescription_logging(self):
        self.clear_content()
        widget = PrescriptionLoggingWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Prescription Logging")
        self.update_status_dot()

    def show_sales_management(self):
        self.clear_content()
        widget = SalesManagementWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Sales Management")
        self.update_status_dot()

    def show_supplier_management(self):
        self.clear_content()
        widget = SupplierManagementWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Supplier Management")
        self.update_status_dot()

    def show_user_management(self):
        self.clear_content()
        widget = UserManagementWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("User Management")
        self.update_status_dot()

    def show_settings(self):
        self.clear_content()
        widget = SettingsWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Settings")
        self.update_status_dot()

    def show_dashboard(self):
        self.clear_content()
        widget = ReportingDashboardWidget(self)
        self.content_layout.addWidget(widget)
        self.set_title("Reporting Dashboard")
        self.update_status_dot()

    def toggle_contrast(self):
        self.is_high_contrast = not self.is_high_contrast
        if self.is_high_contrast:
            self.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        else:
            self.setStyleSheet("")
        self.update()

    def set_title(self, title):
        self.setWindowTitle(f"MicroClinic Plus Pharmacy Manager - {title}")


if __name__ == '__main__':
    try:
        subprocess.run(['python', 'scripts/add_user.py'], check=True)
    except Exception as e:
        print(f"[WARN] Failed to run add_user.py: {e}")

    app = QApplication([])
    window = MainWindow()
    window.setStyleSheet("background-color: #000000; color: #FFFFFF;")
    window.show()
    app.exec()

