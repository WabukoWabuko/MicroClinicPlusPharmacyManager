from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class ReportingDashboardWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Report selection
        report_layout = QHBoxLayout()
        report_label = QLabel("Select Report:")
        self.report_combo = QComboBox()
        self.report_combo.addItems([
            "Select Report",
            "Patient Summary",
            "Prescription History",
            "Inventory Status",
            "Sales Report",
            "Low Stock Alert"
        ])
        self.report_combo.setToolTip("Select a report to generate")
        self.report_combo.setStyleSheet("""
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
        generate_button = QPushButton("Generate Report")
        generate_button.setToolTip("Generate the selected report")
        generate_button.setStyleSheet("""
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
        generate_button.clicked.connect(self.generate_report)
        report_layout.addWidget(report_label)
        report_layout.addWidget(self.report_combo)
        report_layout.addWidget(generate_button)
        main_layout.addLayout(report_layout)

        # Report table
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(0)
        self.report_table.setHorizontalHeaderLabels([])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.report_table.setToolTip("Generated report data")
        self.report_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        main_layout.addWidget(self.report_table)

        # Buttons
        button_layout = QHBoxLayout()
        export_button = QPushButton("Export to PDF")
        export_button.setToolTip("Export the report to a PDF file")
        export_button.setStyleSheet("""
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
        export_button.clicked.connect(self.export_to_pdf)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(export_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

        main_layout.addStretch()

    def generate_report(self):
        report_type = self.report_combo.currentText()
        if report_type == "Select Report":
            QMessageBox.warning(self, "Error", "Please select a report type.")
            return

        if report_type == "Patient Summary":
            self.generate_patient_summary()
        elif report_type == "Prescription History":
            self.generate_prescription_history()
        elif report_type == "Inventory Status":
            self.generate_inventory_status()
        elif report_type == "Sales Report":
            self.generate_sales_report()
        elif report_type == "Low Stock Alert":
            self.generate_low_stock_alert()

    def generate_patient_summary(self):
        patients = self.db.get_all_patients()
        self.report_table.setColumnCount(6)
        self.report_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Age", "Gender", "Contact"])
        self.report_table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            self.report_table.setItem(row, 0, QTableWidgetItem(str(patient['patient_id'])))
            self.report_table.setItem(row, 1, QTableWidgetItem(patient['first_name']))
            self.report_table.setItem(row, 2, QTableWidgetItem(patient['last_name']))
            self.report_table.setItem(row, 3, QTableWidgetItem(str(patient['age'])))
            self.report_table.setItem(row, 4, QTableWidgetItem(patient['gender']))
            self.report_table.setItem(row, 5, QTableWidgetItem(patient['contact']))

    def generate_prescription_history(self):
        prescriptions = self.db.get_all_prescriptions()
        self.report_table.setColumnCount(6)
        self.report_table.setHorizontalHeaderLabels(["ID", "Patient", "Drug", "Dosage", "Date", "Quantity"])
        self.report_table.setRowCount(len(prescriptions))
        for row, prescription in enumerate(prescriptions):
            patient = self.db.get_patient(prescription['patient_id'])
            drug = self.db.get_drug(prescription['drug_id'])
            self.report_table.setItem(row, 0, QTableWidgetItem(str(prescription['prescription_id'])))
            self.report_table.setItem(row, 1, QTableWidgetItem(f"{patient['first_name']} {patient['last_name']}"))
            self.report_table.setItem(row, 2, QTableWidgetItem(drug['name']))
            self.report_table.setItem(row, 3, QTableWidgetItem(prescription['dosage']))
            self.report_table.setItem(row, 4, QTableWidgetItem(prescription['prescription_date']))
            self.report_table.setItem(row, 5, QTableWidgetItem(str(prescription['quantity_prescribed'])))

    def generate_inventory_status(self):
        drugs = self.db.get_all_drugs()
        self.report_table.setColumnCount(6)
        self.report_table.setHorizontalHeaderLabels(["ID", "Name", "Quantity", "Batch Number", "Expiry Date", "Price"])
        self.report_table.setRowCount(len(drugs))
        for row, drug in enumerate(drugs):
            self.report_table.setItem(row, 0, QTableWidgetItem(str(drug['drug_id'])))
            self.report_table.setItem(row, 1, QTableWidgetItem(drug['name']))
            self.report_table.setItem(row, 2, QTableWidgetItem(str(drug['quantity'])))
            self.report_table.setItem(row, 3, QTableWidgetItem(drug['batch_number']))
            self.report_table.setItem(row, 4, QTableWidgetItem(drug['expiry_date']))
            self.report_table.setItem(row, 5, QTableWidgetItem(f"{drug['price']:.2f}"))

    def generate_sales_report(self):
        sales = self.db.get_all_sales()
        self.report_table.setColumnCount(4)
        self.report_table.setHorizontalHeaderLabels(["Sale ID", "Patient", "Total Price", "Date"])
        self.report_table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            patient = self.db.get_patient(sale['patient_id'])
            self.report_table.setItem(row, 0, QTableWidgetItem(str(sale['sale_id'])))
            self.report_table.setItem(row, 1, QTableWidgetItem(f"{patient['first_name']} {patient['last_name']}"))
            self.report_table.setItem(row, 2, QTableWidgetItem(f"{sale['total_price']:.2f}"))
            self.report_table.setItem(row, 3, QTableWidgetItem(sale['sale_date']))

    def generate_low_stock_alert(self):
        drugs = self.db.get_low_stock_drugs()
        self.report_table.setColumnCount(3)
        self.report_table.setHorizontalHeaderLabels(["ID", "Name", "Quantity"])
        self.report_table.setRowCount(len(drugs))
        for row, drug in enumerate(drugs):
            self.report_table.setItem(row, 0, QTableWidgetItem(str(drug['drug_id'])))
            self.report_table.setItem(row, 1, QTableWidgetItem(drug['name']))
            self.report_table.setItem(row, 2, QTableWidgetItem(str(drug['quantity'])))

    def export_to_pdf(self):
        if self.report_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "No report data to export.")
            return

        report_type = self.report_combo.currentText()
        if report_type == "Select Report":
            QMessageBox.warning(self, "Error", "Please generate a report first.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", f"{report_type.replace(' ', '_').lower()}_report.pdf", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        pdf = SimpleDocTemplate(file_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("MicroClinicPlus Pharmacy", styles['Heading1']))
        elements.append(Paragraph(f"{report_type} Report", styles['Heading2']))
        elements.append(Spacer(1, 12))

        headers = [self.report_table.horizontalHeaderItem(i).text() for i in range(self.report_table.columnCount())]
        data = [headers]
        for row in range(self.report_table.rowCount()):
            row_data = [self.report_table.item(row, col).text() for col in range(self.report_table.columnCount())]
            data.append(row_data)

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"Generated on: {self.db.get_current_date()}", styles['Normal']))
        pdf.build(elements)
        QMessageBox.information(self, "Success", f"Report exported to {file_path}")
