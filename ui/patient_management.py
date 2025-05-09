from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QLineEdit, QComboBox, QTextEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import QDate
from db.database import Database

class PatientManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Form layout for patient details
        form_layout = QFormLayout()
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.gender_input = QComboBox()
        self.gender_input.addItems(["M", "F", "Other"])
        self.phone_input = QLineEdit()
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(50)

        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Age:", self.age_input)
        form_layout.addRow("Gender:", self.gender_input)
        form_layout.addRow("Contact:", self.phone_input)
        form_layout.addRow("Medical History:", self.address_input)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        clear_button = QPushButton("Clear")
        view_button = QPushButton("View All")
        back_button = QPushButton("Back")
        save_button.clicked.connect(self.save_patient)
        clear_button.clicked.connect(self.clear_form)
        view_button.clicked.connect(self.view_patients)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(view_button)
        button_layout.addWidget(back_button)

        # Table for viewing patients
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "First Name", "Last Name", "DOB", "Gender", "Phone", "Medical History"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Add to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

    def save_patient(self):
        """Save patient data to the database."""
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        age = self.age_input.text().strip()
        gender = self.gender_input.currentText()
        phone = self.phone_input.text().strip()
        medical_history = self.address_input.toPlainText().strip()

        # Validate inputs
        if not (first_name and last_name and age):
            QMessageBox.warning(self, "Input Error", "First Name, Last Name, and Age are required.")
            return

        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Age must be a positive number.")
            return

        # Calculate date of birth (approximate, assuming current year)
        current_year = QDate.currentDate().year()
        date_of_birth = f"{current_year - age}-01-01"

        # Save to database
        self.db.add_patient(first_name, last_name, date_of_birth, gender, phone, medical_history)
        QMessageBox.information(self, "Success", "Patient saved successfully.")
        self.clear_form()

    def clear_form(self):
        """Clear all input fields."""
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.age_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.phone_input.clear()
        self.address_input.clear()

    def view_patients(self):
        """Display all patients in the table."""
        patients = self.db.get_all_patients()
        self.table.setRowCount(len(patients))

        for row, patient in enumerate(patients):
            self.table.setItem(row, 0, QTableWidgetItem(str(patient['patient_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(patient['first_name']))
            self.table.setItem(row, 2, QTableWidgetItem(patient['last_name']))
            self.table.setItem(row, 3, QTableWidgetItem(patient['date_of_birth']))
            self.table.setItem(row, 4, QTableWidgetItem(patient['gender']))
            self.table.setItem(row, 5, QTableWidgetItem(patient['phone'] or ""))
            self.table.setItem(row, 6, QTableWidgetItem(patient['address'] or ""))
