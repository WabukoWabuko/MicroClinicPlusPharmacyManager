from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QLineEdit, QTextEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database

class PrescriptionLoggingWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Form for logging prescriptions
        form_layout = QHBoxLayout()
        left_form = QVBoxLayout()
        right_form = QVBoxLayout()

        self.patient_combo = QComboBox()
        self.patient_combo.setToolTip("Select patient")
        self.patient_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.drug_combo = QComboBox()
        self.drug_combo.setToolTip("Select drug")
        self.drug_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.diagnosis_input = QTextEdit()
        self.diagnosis_input.setPlaceholderText("Enter diagnosis")
        self.diagnosis_input.setToolTip("Enter patient diagnosis")
        self.diagnosis_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Enter notes")
        self.notes_input.setToolTip("Additional prescription notes")
        self.notes_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.dosage_input = QLineEdit()
        self.dosage_input.setPlaceholderText("e.g., 500mg")
        self.dosage_input.setToolTip("Enter dosage")
        self.dosage_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.frequency_input = QLineEdit()
        self.frequency_input.setPlaceholderText("e.g., Twice daily")
        self.frequency_input.setToolTip("Enter frequency")
        self.frequency_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("e.g., 7 days")
        self.duration_input.setToolTip("Enter duration")
        self.duration_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setToolTip("Enter quantity prescribed")
        self.quantity_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)

        left_form.addWidget(QLabel("Patient:"))
        left_form.addWidget(self.patient_combo)
        left_form.addWidget(QLabel("Drug:"))
        left_form.addWidget(self.drug_combo)
        left_form.addWidget(QLabel("Diagnosis:"))
        left_form.addWidget(self.diagnosis_input)
        right_form.addWidget(QLabel("Dosage:"))
        right_form.addWidget(self.dosage_input)
        right_form.addWidget(QLabel("Frequency:"))
        right_form.addWidget(self.frequency_input)
        right_form.addWidget(QLabel("Duration:"))
        right_form.addWidget(self.duration_input)
        right_form.addWidget(QLabel("Quantity:"))
        right_form.addWidget(self.quantity_input)
        right_form.addWidget(QLabel("Notes:"))
        right_form.addWidget(self.notes_input)

        form_layout.addLayout(left_form)
        form_layout.addLayout(right_form)
        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Prescription")
        add_button.setToolTip("Log new prescription")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        clear_button = QPushButton("Clear")
        clear_button.setToolTip("Clear form")
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        back_button = QPushButton("Back")
        back_button.setToolTip("Return to menu")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        add_button.clicked.connect(self.add_prescription)
        clear_button.clicked.connect(self.clear_form)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(add_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

        # Prescription table
        self.prescription_table = QTableWidget()
        self.prescription_table.setColumnCount(6)
        self.prescription_table.setHorizontalHeaderLabels(["ID", "Patient", "Drug", "Dosage", "Date", "Quantity"])
        self.prescription_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.prescription_table.setToolTip("List of prescriptions")
        self.prescription_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        main_layout.addWidget(self.prescription_table)

        main_layout.addStretch()

        self.load_data()

    def load_data(self):
        patients = self.db.get_all_patients()
        self.patient_combo.clear()
        self.patient_combo.addItem("Select Patient")
        for patient in patients:
            self.patient_combo.addItem(f"{patient['first_name']} {patient['last_name']}", patient['patient_id'])

        drugs = self.db.get_all_drugs()
        self.drug_combo.clear()
        self.drug_combo.addItem("Select Drug")
        for drug in drugs:
            self.drug_combo.addItem(drug['name'], drug['drug_id'])

        prescriptions = self.db.get_all_prescriptions()
        self.prescription_table.setRowCount(len(prescriptions))
        for row, prescription in enumerate(prescriptions):
            patient = self.db.get_patient(prescription['patient_id'])
            drug = self.db.get_drug(prescription['drug_id'])
            self.prescription_table.setItem(row, 0, QTableWidgetItem(str(prescription['prescription_id'])))
            self.prescription_table.setItem(row, 1, QTableWidgetItem(f"{patient['first_name']} {patient['last_name']}"))
            self.prescription_table.setItem(row, 2, QTableWidgetItem(drug['name']))
            self.prescription_table.setItem(row, 3, QTableWidgetItem(prescription['dosage']))
            self.prescription_table.setItem(row, 4, QTableWidgetItem(prescription['prescription_date']))
            self.prescription_table.setItem(row, 5, QTableWidgetItem(str(prescription['quantity_prescribed'])))

    def add_prescription(self):
        patient_id = self.patient_combo.currentData()
        drug_id = self.drug_combo.currentData()
        diagnosis = self.diagnosis_input.toPlainText().strip()
        notes = self.notes_input.toPlainText().strip()
        dosage = self.dosage_input.text().strip()
        frequency = self.frequency_input.text().strip()
        duration = self.duration_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not patient_id or self.patient_combo.currentText() == "Select Patient":
            QMessageBox.warning(self, "Error", "Please select a patient.")
            return
        if not drug_id or self.drug_combo.currentText() == "Select Drug":
            QMessageBox.warning(self, "Error", "Please select a drug.")
            return
        if not diagnosis:
            QMessageBox.warning(self, "Error", "Diagnosis is required.")
            return
        if not dosage:
            QMessageBox.warning(self, "Error", "Dosage is required.")
            return
        if not frequency:
            QMessageBox.warning(self, "Error", "Frequency is required.")
            return
        if not duration:
            QMessageBox.warning(self, "Error", "Duration is required.")
            return
        if not quantity:
            QMessageBox.warning(self, "Error", "Quantity is required.")
            return
        try:
            quantity_val = int(quantity)
            if quantity_val <= 0:
                QMessageBox.warning(self, "Error", "Quantity must be greater than 0.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Quantity must be a number.")
            return

        try:
            self.db.add_prescription(
                patient_id=patient_id,
                user_id=self.main_window.current_user['user_id'],
                diagnosis=diagnosis,
                notes=notes,
                drug_id=drug_id,
                dosage=dosage,
                frequency=frequency,
                duration=duration,
                quantity_prescribed=quantity_val
            )
            QMessageBox.information(self, "Success", "Prescription added successfully.")
            self.load_data()
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def clear_form(self):
        self.patient_combo.setCurrentIndex(0)
        self.drug_combo.setCurrentIndex(0)
        self.diagnosis_input.clear()
        self.notes_input.clear()
        self.dosage_input.clear()
        self.frequency_input.clear()
        self.duration_input.clear()
        self.quantity_input.clear()
