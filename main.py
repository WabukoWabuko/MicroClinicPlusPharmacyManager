import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from ui.patient_management import PatientManagementWindow
from ui.prescription_logging import PrescriptionLoggingWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MicroClinicPlusPharmacyManager")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        patient_button = QPushButton("Patient Management")
        prescription_button = QPushButton("Prescription Logging")
        patient_button.clicked.connect(self.open_patient_management)
        prescription_button.clicked.connect(self.open_prescription_logging)
        layout.addWidget(patient_button)
        layout.addWidget(prescription_button)

    def open_patient_management(self):
        self.patient_window = PatientManagementWindow()
        self.patient_window.show()

    def open_prescription_logging(self):
        self.prescription_window = PrescriptionLoggingWindow()
        self.prescription_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
