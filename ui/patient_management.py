from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QComboBox, QTextEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt
from db.database import Database
from utils.validation import is_valid_name, is_valid_phone
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Image
import os

class PatientManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Form for managing patients
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
        self.contact_input.setToolTip("Patient's contact number (exactly 13 characters, e.g., +254700123456)")
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
        update_button = QPushButton("Update Patient")
        update_button.setToolTip("Update selected patient")
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
        delete_button = QPushButton("Delete Patient")
        delete_button.setToolTip("Delete selected patient")
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
        print_button = QPushButton("Print Patient Data")
        print_button.setToolTip("Print selected patient's data to PDF")
        print_button.setStyleSheet("""
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
        update_button.clicked.connect(self.update_patient)
        delete_button.clicked.connect(self.delete_patient)
        print_button.clicked.connect(self.print_patient_data)
        clear_button.clicked.connect(self.clear_form)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(print_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

        # Patient table
        self.patient_table = QTableWidget()
        self.patient_table.setColumnCount(7)
        self.patient_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Age", "Gender", "Contact", "Medical History"])
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
        self.patient_table.clicked.connect(self.load_patient_to_form)
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
            self.patient_table.setItem(row, 6, QTableWidgetItem(patient['medical_history'] if patient['medical_history'] else "N/A"))

    def load_patient_to_form(self):
        row = self.patient_table.currentRow()
        if row >= 0:
            self.first_name_input.setText(self.patient_table.item(row, 1).text())
            self.last_name_input.setText(self.patient_table.item(row, 2).text())
            self.age_input.setText(self.patient_table.item(row, 3).text())
            self.gender_combo.setCurrentText(self.patient_table.item(row, 4).text())
            self.contact_input.setText(self.patient_table.item(row, 5).text())
            self.medical_history_input.setText(self.patient_table.item(row, 6).text() if self.patient_table.item(row, 6).text() != "N/A" else "")

    def add_patient(self):
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            QMessageBox.warning(self, "Error", "Demo period expired. Please activate the system.")
            return

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
        QMessageBox.information(self, "Success", "Patient added successfully at 11:57 AM EAT on Wednesday, May 14, 2025.")
        self.load_patients()
        self.clear_form()

    def update_patient(self):
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            QMessageBox.warning(self, "Error", "Demo period expired. Please activate the system.")
            return

        row = self.patient_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a patient to update.")
            return

        patient_id = int(self.patient_table.item(row, 0).text())
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

        self.db.update_patient(patient_id, first_name, last_name, age_val, gender, contact, medical_history)
        QMessageBox.information(self, "Success", "Patient updated successfully at 11:57 AM EAT on Wednesday, May 14, 2025.")
        self.load_patients()
        self.clear_form()

    def delete_patient(self):
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            QMessageBox.warning(self, "Error", "Demo period expired. Please activate the system.")
            return

        row = self.patient_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a patient to delete.")
            return

        patient_id = int(self.patient_table.item(row, 0).text())
        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this patient?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_patient(patient_id)
            QMessageBox.information(self, "Success", "Patient deleted successfully at 11:57 AM EAT on Wednesday, May 14, 2025.")
            self.load_patients()
            self.clear_form()

    def print_patient_data(self):
        row = self.patient_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a patient to print data for.")
            return

        patient_id = int(self.patient_table.item(row, 0).text())
        patient = self.db.get_patient(patient_id)

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Patient Data", f"patient_{patient_id}_data.pdf", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        # Setup document
        doc = SimpleDocTemplate(file_path, pagesize=A4,
                                leftMargin=20*mm, rightMargin=20*mm,
                                topMargin=20*mm, bottomMargin=20*mm)

        # Styles
        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(
            'Header', parent=styles['Heading1'], fontSize=18,
            alignment=1, spaceAfter=6)
        normal_center = ParagraphStyle(
            'NormalCenter', parent=styles['Normal'], alignment=1, fontSize=10)
        normal = ParagraphStyle(
            'Normal', parent=styles['Normal'], fontSize=10, leading=12)

        elements = []

        # Retrieve settings from config
        logo_path = self.main_window.config.get("logo_path", "")
        bg_path = self.main_window.config.get("background_path", "")
        clinic_name = self.main_window.config.get("clinic_name", "MicroClinic")
        contact_details = self.main_window.config.get("contact_details", "")

        # Background Image and Logo (faded hospital theme)
        def on_page(canvas, doc):
            canvas.saveState()
            # Background image
            if bg_path and os.path.exists(bg_path):
                canvas.setFillAlpha(0.2)
                canvas.drawImage(bg_path, 20*mm, 20*mm, width=A4[0]-40*mm, height=A4[1]-40*mm, mask='auto')
            else:
                # Fallback background
                canvas.setFillAlpha(0.2)
                if os.path.exists('assets/hospital_bg.jpg'):
                    canvas.drawImage('assets/hospital_bg.jpg', 20*mm, 20*mm, width=A4[0]-40*mm, height=A4[1]-40*mm, mask='auto')
            canvas.restoreState()
            # Logo (Top Left)
            if logo_path and os.path.exists(logo_path):
                canvas.drawImage(logo_path, 20*mm, A4[1]-30*mm, width=50*mm, height=50*mm, mask='auto')
            else:
                # Fallback logo
                if os.path.exists('assets/logo.png'):
                    canvas.drawImage('assets/logo.png', 20*mm, A4[1]-30*mm, width=50*mm, height=50*mm, mask='auto')
            # Logo (Bottom Right)
            if logo_path and os.path.exists(logo_path):
                canvas.drawImage(logo_path, A4[0]-70*mm, 20*mm, width=50*mm, height=50*mm, mask='auto')
            else:
                # Fallback logo
                if os.path.exists('assets/logo.png'):
                    canvas.drawImage('assets/logo.png', A4[0]-70*mm, 20*mm, width=50*mm, height=50*mm, mask='auto')

        # Header
        elements.append(Paragraph(clinic_name, header_style))
        elements.append(Paragraph("123 Moi Avenue, Nairobi, Kenya", normal_center))
        elements.append(Paragraph(f"Phone: {contact_details}" if contact_details else "Contact Not Provided", normal_center))
        elements.append(Spacer(1, 4))
        elements.append(HRFlowable(width=doc.width, thickness=0.5, color=colors.black))
        elements.append(Spacer(1, 8))

        # Patient Data Title
        elements.append(Paragraph("Patient Data", styles['Heading2']))
        elements.append(Spacer(1, 12))

        # Patient Details
        patient_data = [
            ["Patient ID:", f"PT-{patient['patient_id']:05d}"],
            ["First Name:", patient['first_name']],
            ["Last Name:", patient['last_name']],
            ["Age:", str(patient['age'])],
            ["Gender:", patient['gender']],
            ["Contact:", patient['contact']],
            ["Medical History:", patient['medical_history'] if patient['medical_history'] else "N/A"]
        ]
        pat_table = Table(patient_data, colWidths=[40*mm, doc.width-40*mm])
        pat_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (1,0), (1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(pat_table)
        elements.append(Spacer(1, 12))

        # Footer
        elements.append(Paragraph(f"Thank you for choosing {clinic_name}!", normal_center))
        elements.append(Paragraph(f"Contact: {contact_details}" if contact_details else "Contact Not Provided", normal_center))
        elements.append(Spacer(1, 4))

        doc.build(elements, onFirstPage=on_page, onLaterPages=on_page)
        QMessageBox.information(self, "Success", f"Patient data saved to:\n{file_path} at 11:57 AM EAT on Wednesday, May 14, 2025.")

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
