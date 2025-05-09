from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QLineEdit, QTextEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database
from utils.validation import is_valid_quantity, is_valid_name
import qtawesome as qta

class PrescriptionLoggingWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Prescription form
        form_layout = QHBoxLayout()
        left_form = QVBoxLayout()
        right_form = QVBoxLayout()

        self.patient_combo = QComboBox()
        self.patient_combo.setToolTip("Select patient")
        self.diagnosis_input = QLineEdit()
        self.diagnosis_input.setPlaceholderText("Enter diagnosis")
        self.diagnosis_input.setToolTip("Enter diagnosis")
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Enter notes")
        self.notes_input.setToolTip("Additional notes")
        self.drug_combo = QComboBox()
        self.drug_combo.setToolTip("Select drug")
        self.dosage_input = QLineEdit()
        self.dosage_input.setPlaceholderText("Enter dosage")
        self.dosage_input.setToolTip("Dosage instructions")
        self.frequency_input = QLineEdit()
        self.frequency_input.setPlaceholderText("Enter frequency")
        self.frequency_input.setToolTip("e.g., Twice daily")
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Enter duration")
        self.duration_input.setToolTip("e.g., 7 days")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setToolTip("Number of units")

        left_form.addWidget(QLabel("Patient:"))
        left_form.addWidget(self.patient_combo)
        left_form.addWidget(QLabel("Diagnosis:"))
        left_form.addWidget(self.diagnosis_input)
        left_form.addWidget(QLabel("Notes:"))
        left_form.addWidget(self.notes_input)
        right_form.addWidget(QLabel("Drug:"))
        right_form.addWidget(self.drug_combo)
        right_form.addWidget(QLabel("Dosage:"))
        right_form.addWidget(self.dosage_input)
        right_form.addWidget(QLabel("Frequency:"))
        right_form.addWidget(self.frequency_input)
        right_form.addWidget(QLabel("Duration:"))
        right_form.addWidget(self.duration_input)
        right_form.addWidget(QLabel("Quantity:"))
        right_form.addWidget(self.quantity_input)

        form_layout.addLayout(left_form)
        form_layout.addLayout(right_form)
        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Prescription")
        add_button.setIcon(qta.icon('mdi.prescription'))
        add_button.setToolTip("Add new prescription")
        clear_button = QPushButton("Clear")
        clear_button.setIcon(qta.icon('mdi.clear'))
        clear_button.setToolTip("Clear form")
        back_button = QPushButton("Back")
        back_button.setIcon(qta.icon('mdi.arrow-back'))
        back_button.setToolTip("Return to menu")
        add_button.clicked.connect(self.add_prescription)
        clear_button.clicked.connect(self.clear_form)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(add_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

        # Prescription table
        self.prescription_table = QTableWidget()
        self.prescription_table.setColumnCount(5)
        self.prescription_table.setHorizontalHeaderLabels(["ID", "Patient", "Drug", "Date", "Quantity"])
        self.prescription_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.prescription_table.setToolTip("List of prescriptions")
        main_layout.addWidget(self.prescription_table)

        main_layout.addStretch()

        self.load_patients()
        self.load_drugs()
        self.load_prescriptions()

    def load_patients(self):
        patients = self.db.get_all_patients()
        self.patient_combo.addItem("Select Patient", None)
        for patient in patients:
            self.patient_combo.addItem(f"{patient['first_name']} {patient['last_name']}", patient['patient_id'])

    def load_drugs(self):
        drugs = self.db.get_all_drugs()
        self.drug_combo.addItem("Select Drug", None)
        for drug in drugs:
            self.drug_combo.addItem(drug['name'], drug['drug_id'])

    def load_prescriptions(self):
        prescriptions = self.db.get_all_prescriptions()
        self.prescription_table.setRowCount(len(prescriptions))
        for row, prescription in enumerate(prescriptions):
            patient = self.db.get_patient(prescription['patient_id'])
            drug = self.db.get_drug(prescription['drug_id'])
            self.prescription_table.setItem(row, 0, QTableWidgetItem(str(prescription['prescription_id'])))
            self.prescription_table.setItem(row, 1, QTableWidgetItem(f"{patient['first_name']} {patient['last_name']}"))
            self.prescription_table.setItem(row, 2, QTableWidgetItem(drug['name']))
            self.prescription_table.setItem(row, 3, QTableWidgetItem(prescription['prescription_date']))
            self.prescription_table.setItem(row, 4, QTableWidgetItem(str(prescription['quantity_prescribed'])))

    def add_prescription(self):
        patient_id = self.patient_combo.currentData()
        diagnosis = self.diagnosis_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        drug_id = self.drug_combo.currentData()
        dosage = self.dosage_input.text().strip()
        frequency = self.frequency_input.text().strip()
        duration = self.duration_input.text().strip()
        quantity = self.quantity_input.text().strip()

        self.diagnosis_input.setStyleSheet("")
        self.dosage_input.setStyleSheet("")
        self.frequency_input.setStyleSheet("")
        self.duration_input.setStyleSheet("")
        self.quantity_input.setStyleSheet("")

        if not patient_id:
            QMessageBox.warning(self, "Error", "Please select a patient.")
            return

        is_valid, error = is_valid_name(diagnosis)
        if not is_valid:
            self.diagnosis_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        if not drug_id:
            QMessageBox.warning(self, "Error", "Please select a drug.")
            return

        is_valid, error = is_valid_name(dosage)
        if not is_valid:
            self.dosage_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_name(frequency)
        if not is_valid:
            self.frequency_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_name(duration)
        if not is_valid:
            self.duration_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_quantity(quantity)
        if not is_valid:
            self.quantity_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        try:
            quantity_val = int(quantity)
            drug = self.db.get_drug(drug_id)
            if drug['quantity'] < quantity_val:
                self.quantity_input.setStyleSheet("border: 1px solid red;")
                QMessageBox.warning(self, "Error", f"Insufficient stock for {drug['name']}. Available: {drug['quantity']}")
                return
            self.db.add_prescription(
                patient_id, self.main_window.current_user['user_id'],
                diagnosis, notes, drug_id, dosage, frequency, duration, quantity_val
            )
            QMessageBox.information(self, "Success", "Prescription added successfully.")
            self.load_prescriptions()
            self.main_window.check_low_stock_alerts()
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def clear_form(self):
        self.patient_combo.setCurrentIndex(0)
        self.diagnosis_input.clear()
        self.notes_input.clear()
        self.drug_combo.setCurrentIndex(0)
        self.dosage_input.clear()
        self.frequency_input.clear()
        self.duration_input.clear()
        self.quantity_input.clear()
        self.diagnosis_input.setStyleSheet("")
        self.dosage_input.setStyleSheet("")
        self.frequency_input.setStyleSheet("")
        self.duration_input.setStyleSheet("")
        self.quantity_input.setStyleSheet("")
