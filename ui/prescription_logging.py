from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
                             QComboBox, QLineEdit, QTextEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from db.database import Database

class PrescriptionLoggingWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Patient search and selection
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by patient name...")
        self.search_input.textChanged.connect(self.search_patients)
        self.patient_combo = QComboBox()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.patient_combo)

        # Form layout for prescription details
        form_layout = QFormLayout()
        form_layout.addRow("Patient:", search_layout)
        self.drug_combo = QComboBox()
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")
        self.dosage_input = QLineEdit()
        self.frequency_input = QLineEdit()
        self.duration_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(50)
        self.diagnosis_input = QLineEdit()

        form_layout.addRow("Drug:", self.drug_combo)
        form_layout.addRow("Quantity:", self.quantity_input)
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
        back_button = QPushButton("Back")
        save_button.clicked.connect(self.save_prescription)
        clear_button.clicked.connect(self.clear_form)
        view_button.clicked.connect(self.view_prescriptions)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(view_button)
        button_layout.addWidget(back_button)

        # Table for viewing prescription history
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Prescription ID", "Date", "Drug", "Quantity", "Diagnosis", "Notes"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Add to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        # Populate dropdowns
        self.populate_patients()
        self.populate_drugs()

    def populate_patients(self, patients=None):
        """Populate patient dropdown with patients, optionally filtered."""
        self.patient_combo.clear()
        if patients is None:
            patients = self.db.get_all_patients()
        for patient in patients:
            self.patient_combo.addItem(
                f"{patient['first_name']} {patient['last_name']}",
                patient['patient_id']
            )

    def search_patients(self):
        """Filter patients in dropdown based on search term."""
        search_term = self.search_input.text().strip()
        if search_term:
            patients = self.db.search_patients(search_term)
        else:
            patients = self.db.get_all_patients()
        self.populate_patients(patients)

    def populate_drugs(self):
        """Populate drug dropdown with available inventory."""
        self.drug_combo.clear()
        drugs = self.db.get_all_drugs()
        for drug in drugs:
            if drug['quantity'] > 0:  # Only show drugs with stock
                self.drug_combo.addItem(
                    f"{drug['name']} (Stock: {drug['quantity']})",
                    drug['drug_id']
                )

    def save_prescription(self):
        """Save prescription to the database."""
        patient_id = self.patient_combo.currentData()
        drug_id = self.drug_combo.currentData()
        quantity_text = self.quantity_input.text().strip()
        dosage = self.dosage_input.text().strip()
        frequency = self.frequency_input.text().strip()
        duration = self.duration_input.text().strip()
        diagnosis = self.diagnosis_input.text().strip()
        notes = self.notes_input.toPlainText().strip()

        # Validate inputs
        if not (patient_id and drug_id and quantity_text and dosage and frequency and duration):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            quantity = int(quantity_text)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity must be a positive integer.")
            return

        try:
            # Save to database (user_id=1 as placeholder)
            self.db.add_prescription(
                patient_id=patient_id,
                user_id=1,  # Placeholder until login system is implemented
                diagnosis=diagnosis,
                notes=notes,
                drug_id=drug_id,
                dosage=dosage,
                frequency=frequency,
                duration=duration,
                quantity_prescribed=quantity
            )
            QMessageBox.information(self, "Success", "Prescription saved successfully.")
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Stock Error", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save prescription: {str(e)}")

    def clear_form(self):
        """Clear all input fields."""
        self.search_input.clear()  # Clear search
        self.populate_patients()  # Reset patient dropdown
        self.quantity_input.clear()
        self.dosage_input.clear()
        self.frequency_input.clear()
        self.duration_input.clear()
        self.diagnosis_input.clear()
        self.notes_input.clear()
        self.table.setRowCount(0)  # Clear table
        self.populate_drugs()  # Reset drug dropdown

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
            self.table.setItem(row, 2, QTableWidgetItem(prescription['drug_name']))
            self.table.setItem(row, 3, QTableWidgetItem(str(prescription['quantity_prescribed'])))
            self.table.setItem(row, 4, QTableWidgetItem(prescription['diagnosis'] or ""))
            self.table.setItem(row, 5, QTableWidgetItem(prescription['notes'] or ""))
