from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QComboBox, QTextEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database
from utils.validation import is_valid_name, is_valid_phone

class PatientManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Form for adding patients
        form_layout = QHBoxLayout()
        left_form = QVBoxLayout()
        right_form = QVBoxLayout()

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter first name")
        self.first_name_input.setToolTip("Patient's first name")
        self.first_name_input.setStyleSheet("""
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
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter last name")
        self.last_name_input.setToolTip("Patient's last name")
        self.last_name_input.setStyleSheet("""
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
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter age")
        self.age_input.setToolTip("Patient's age (1-150)")
        self.age_input.setStyleSheet("""
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
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        self.gender_combo.setToolTip("Select gender")
        self.gender_combo.setStyleSheet("""
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
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("e.g., +254700123456")
        self.contact_input.setToolTip("Patient's contact number (e.g., +254700123456)")
        self.contact_input.setStyleSheet("""
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
        self.medical_history_input = QTextEdit()
        self.medical_history_input.setPlaceholderText("Enter medical history")
        self.medical_history_input.setToolTip("Patient's medical history")
        self.medical_history_input.setStyleSheet("""
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

        left_form.addWidget(QLabel("First Name:"))
        left_form.addWidget(self.first_name_input)
        left_form.addWidget(QLabel("Last Name:"))
        left_form.addWidget(self.last_name_input)
        left_form.addWidget(QLabel("Age:"))
        left_form.addWidget(self.age_input)
        right_form.addWidget(QLabel("Gender:"))
        right_form.addWidget(self.gender_combo)
        right_form.addWidget(QLabel("Contact:"))
        right_form.addWidget(self.contact_input)
        right_form.addWidget(QLabel("Medical History:"))
        right_form.addWidget(self.medical_history_input)

        form_layout.addLayout(left_form)
        form_layout.addLayout(right_form)
        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Patient")
        add_button.setToolTip("Add new patient")
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
        add_button.clicked.connect(self.add_patient)
        clear_button.clicked.connect(self.clear_form)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(add_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

        # Patient table
        self.patient_table = QTableWidget()
        self.patient_table.setColumnCount(6)
        self.patient_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Age", "Gender", "Contact"])
        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.patient_table.setToolTip("List of registered patients")
        self.patient_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        main_layout.addWidget(self.patient_table)

        main_layout.addStretch()

        self.load_patients()

    def load_patients(self):
        patients = self.db.get_all_patients()
        self.patient_table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            self.patient_table.setItem(row, 0, QTableWidgetItem(str(patient['patient_id'])))
            self.patient_table.setItem(row, 1, QTableWidgetItem(patient['first_name']))
            self.patient_table.setItem(row, 2, QTableWidgetItem(patient['last_name']))
            self.patient_table.setItem(row, 3, QTableWidgetItem(str(patient['age'])))
            self.patient_table.setItem(row, 4, QTableWidgetItem(patient['gender']))
            self.patient_table.setItem(row, 5, QTableWidgetItem(patient['contact']))

    def add_patient(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        age = self.age_input.text().strip()
        gender = self.gender_combo.currentText()
        contact = self.contact_input.text().strip()
        medical_history = self.medical_history_input.toPlainText().strip()

        self.first_name_input.setStyleSheet("""
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
        self.last_name_input.setStyleSheet("""
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
        self.age_input.setStyleSheet("""
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
        self.contact_input.setStyleSheet("""
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

        is_valid, error = is_valid_name(first_name)
        if not is_valid:
            self.first_name_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid red;
                    border-radius: 4px;
                    font-size: 14px;
                }
            """)
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_name(last_name)
        if not is_valid:
            self.last_name_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid red;
                    border-radius: 4px;
                    font-size: 14px;
                }
            """)
            QMessageBox.warning(self, "Error", error)
            return

        if not age:
            self.age_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid red;
                    border-radius: 4px;
                    font-size: 14px;
                }
            """)
            QMessageBox.warning(self, "Error", "Age is required.")
            return
        try:
            age_val = int(age)
            if age_val <= 0 or age_val > 150:
                self.age_input.setStyleSheet("""
                    QLineEdit {
                        padding: 8px;
                        border: 1px solid red;
                        border-radius: 4px;
                        font-size: 14px;
                    }
                """)
                QMessageBox.warning(self, "Error", "Age must be between 1 and 150.")
                return
        except ValueError:
            self.age_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid red;
                    border-radius: 4px;
                    font-size: 14px;
                }
            """)
            QMessageBox.warning(self, "Error", "Age must be a number.")
            return

        is_valid, error = is_valid_phone(contact)
        if not is_valid:
            self.contact_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid red;
                    border-radius: 4px;
                    font-size: 14px;
                }
            """)
            QMessageBox.warning(self, "Error", error)
            return

        self.db.add_patient(first_name, last_name, age_val, gender, contact, medical_history)
        QMessageBox.information(self, "Success", "Patient added successfully.")
        self.load_patients()
        self.clear_form()

    def clear_form(self):
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.age_input.clear()
        self.gender_combo.setCurrentIndex(0)
        self.contact_input.clear()
        self.medical_history_input.clear()
        self.first_name_input.setStyleSheet("""
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
        self.last_name_input.setStyleSheet("""
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
        self.age_input.setStyleSheet("""
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
        self.contact_input.setStyleSheet("""
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
