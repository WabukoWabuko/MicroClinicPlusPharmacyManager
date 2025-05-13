from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QLineEdit, QTextEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox, QCompleter)
from PyQt6.QtCore import Qt
from db.database import Database

class SearchableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer().setFilterMode(Qt.MatchFlag.MatchContains)
        self.setStyleSheet("""
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

        # Searchable patient combo
        self.patient_search_combo = SearchableComboBox()
        self.patient_search_combo.setToolTip("Search or select patient")
        # Searchable drug combo
        self.drug_search_combo = SearchableComboBox()
        self.drug_search_combo.setToolTip("Search or select drug")
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

        left_form.addWidget(QLabel("Patient (Search):"))
        left_form.addWidget(self.patient_search_combo)
        left_form.addWidget(QLabel("Drug (Search):"))
        left_form.addWidget(self.drug_search_combo)
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
        update_button = QPushButton("Update Prescription")
        update_button.setToolTip("Update selected prescription")
        update_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        delete_button = QPushButton("Delete Prescription")
        delete_button.setToolTip("Delete selected prescription")
        delete_button.setStyleSheet("""
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
        update_button.clicked.connect(self.update_prescription)
        delete_button.clicked.connect(self.delete_prescription)
        clear_button.clicked.connect(self.clear_form)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
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
        self.prescription_table.clicked.connect(self.load_prescription_to_form)
        main_layout.addWidget(self.prescription_table)

        main_layout.addStretch()

        self.load_data()

    def load_data(self):
        # Load patients
        patients = self.db.get_all_patients()
        self.patient_search_combo.clear()
        self.patient_search_combo.addItem("Select Patient")
        for patient in patients:
            self.patient_search_combo.addItem(f"{patient['first_name']} {patient['last_name']}", patient['patient_id'])

        # Load drugs
        drugs = self.db.get_all_drugs()
        self.drug_search_combo.clear()
        self.drug_search_combo.addItem("Select Drug")
        for drug in drugs:
            self.drug_search_combo.addItem(drug['name'], drug['drug_id'])

        # Load prescriptions
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

    def load_prescription_to_form(self):
        row = self.prescription_table.currentRow()
        if row >= 0:
            prescription_id = int(self.prescription_table.item(row, 0).text())
            prescription = self.db.get_prescription(prescription_id)  # Assuming this method exists
            patient = self.db.get_patient(prescription['patient_id'])
            drug = self.db.get_drug(prescription['drug_id'])
            self.patient_search_combo.setCurrentText(f"{patient['first_name']} {patient['last_name']}")
            self.drug_search_combo.setCurrentText(drug['name'])
            self.diagnosis_input.setText(prescription['diagnosis'])
            self.notes_input.setText(prescription['notes'] or "")
            self.dosage_input.setText(prescription['dosage'])
            self.frequency_input.setText(prescription['frequency'])
            self.duration_input.setText(prescription['duration'])
            self.quantity_input.setText(str(prescription['quantity_prescribed']))

    def add_prescription(self):
        patient_id = self.patient_search_combo.currentData()
        drug_id = self.drug_search_combo.currentData()
        diagnosis = self.diagnosis_input.toPlainText().strip()
        notes = self.notes_input.toPlainText().strip()
        dosage = self.dosage_input.text().strip()
        frequency = self.frequency_input.text().strip()
        duration = self.duration_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not patient_id or self.patient_search_combo.currentText() == "Select Patient":
            QMessageBox.warning(self, "Error", "Please select a patient.")
            return
        if not drug_id or self.drug_search_combo.currentText() == "Select Drug":
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

    def update_prescription(self):
        row = self.prescription_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a prescription to update.")
            return

        prescription_id = int(self.prescription_table.item(row, 0).text())
        patient_id = self.patient_search_combo.currentData()
        drug_id = self.drug_search_combo.currentData()
        diagnosis = self.diagnosis_input.toPlainText().strip()
        notes = self.notes_input.toPlainText().strip()
        dosage = self.dosage_input.text().strip()
        frequency = self.frequency_input.text().strip()
        duration = self.duration_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not patient_id or self.patient_search_combo.currentText() == "Select Patient":
            QMessageBox.warning(self, "Error", "Please select a patient.")
            return
        if not drug_id or self.drug_search_combo.currentText() == "Select Drug":
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
            self.db.update_prescription(
                prescription_id=prescription_id,
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
            QMessageBox.information(self, "Success", "Prescription updated successfully.")
            self.load_data()
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_prescription(self):
        row = self.prescription_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a prescription to delete.")
            return

        prescription_id = int(self.prescription_table.item(row, 0).text())
        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this prescription?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_prescription(prescription_id)
            QMessageBox.information(self, "Success", "Prescription deleted successfully.")
            self.load_data()
            self.clear_form()

    def clear_form(self):
        self.patient_search_combo.setCurrentIndex(0)
        self.drug_search_combo.setCurrentIndex(0)
        self.diagnosis_input.clear()
        self.notes_input.clear()
        self.dosage_input.clear()
        self.frequency_input.clear()
        self.duration_input.clear()
        self.quantity_input.clear()
