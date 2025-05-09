import sys
from PyQt6.QtWidgets import QApplication
from ui.patient_management import PatientManagementWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PatientManagementWindow()
    window.show()
    sys.exit(app.exec())
