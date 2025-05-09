from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
                             QComboBox, QLineEdit, QTextEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import QDate
from db.database import Database

class PrescriptionLoggingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prescription Logging - MicroClinicPlusPharmacyManager")
        self.setGeometry(100, 100, 800, 600)
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Form layout for prescription details
        form_layout = QFormLayout()
        self.patient_combo = QComboBox()
        self.populate_patients()
        self.drug_name_input = QLineEdit()
        self.dosage_input = QLineEdit()
        self.frequency_input = QLineEdit()
        self.duration_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(50)
        self.diagnosis_input = QLineEdit()

        form_layout.addRow("Patient:", self.patient_combo)
        form_layout.addRow("Drug Name:", self.drug_name_input)
        form_layout.addRow("Dosage:", self.dosage_input)
        form_layout.addRow("Frequency:", self.frequency_input)
        form_layout.addRow("Duration:", self.duration_input)
        form_layout.addRow("Diagnosis:", self.diagnosis_input)
        form_layout.addRow("Notes:", self.notes_input)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        clear_button = QPushButton("Clear")
        view_button = QPushButton("View History")
        save_button.clicked.connect(self.save_prescription)
        clear_button.clicked.connect(self.clear_form)
        view_button.clicked.connect(self.view_prescriptions)
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(view_button)

        # Table for viewing prescription history
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Prescription ID", "Date", "Diagnosis", "Notes", "Dosage Instructions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Add to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

    def populate_patients(self):
        """Populate patient dropdown with all patients."""
        self.patient_combo.clear()
        patients = self.db.get_all_patients()
        for patient in patients:
            self.patient_combo.addItem(
                f"{patient['first_name']} {patient['last_name']}",
                patient['patient_id']
            )

    def save_prescription(self):
        """Save prescription to the database."""
        patient_id = self.patient_combo.currentData()
        drug_name = self.drug_name_input.text().strip()
        dosage = self.dosage_input.text().strip()
        frequency = self.frequency_input.text().strip()
        duration = self.duration_input.text().strip()
        diagnosis = self.diagnosis_input.text().strip()
        notes = self.notes_input.toPlainText().strip()

        # Validate inputs
        if not (patient_id and drug_name and dosage and frequency and duration):
            QMessageBox.warning(self, "Input Error", "Patient, Drug Name, Dosage, Frequency, and Duration are required.")
            return

        # Save to database (user_id=1 as placeholder)
        self.db.add_prescription(
            patient_id=patient_id,
            user_id=1,  # Placeholder until login system is implemented
            diagnosis=diagnosis,
            notes=notes,
            drug_name=drug_name,
            dosage=dosage,
            frequency=frequency,
            duration=duration
        )
        QMessageBox.information(self, "Success", "Prescription saved successfully.")
        self.clear_form()

    def clear_form(self):
        """Clear all input fields."""
        self.drug_name_input.clear()
        self.dosage_input.clear()
        self.frequency_input.clear()
        self.duration_input.clear()
        self.diagnosis_input.clear()
        self.notes_input.clear()
        self.table.setRowCount(0)  # Clear table as well

    def view_prescriptions(self):
        """Display prescription history for the selected patient."""
        patient_id = self.patient_combo.currentData()
        if not patient_id:
            QMessageBox.warning(self, "Selection Error", "Please select a patient.")
            return

        prescriptions = self.db.get_patient_prescriptions(patient_id)
        self.table.setRowCount(len(prescriptions))

        for row, prescription in enumerate(prescriptions):
            self.table.setItem(row, 0, QTableWidgetItem(str(prescription['prescription_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(prescription['prescription_date']))
            self.table.setItem(row, 2, QTableWidgetItem(prescription['diagnosis'] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(prescription['notes'] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(prescription['dosage_instructions']))
