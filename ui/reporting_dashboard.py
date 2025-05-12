from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Image

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

        # Setup document with consistent margins
        pdf = SimpleDocTemplate(file_path, pagesize=A4,
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
        small = ParagraphStyle(
            'Small', parent=styles['Normal'], fontSize=8, leading=10)

        elements = []

        # Header
        elements.append(Paragraph("Wabuko Health Clinic", header_style))
        elements.append(Paragraph("123 Moi Avenue, Nairobi, Kenya", normal_center))
        elements.append(Paragraph("Phone: +234 700 123 4567 | info@wabukohealth.ng", normal_center))
        elements.append(Spacer(1, 4))
        elements.append(HRFlowable(width=pdf.width, thickness=0.5, color=colors.black))
        elements.append(Spacer(1, 8))

        # Report Title
        elements.append(Paragraph(f"{report_type} Report", styles['Heading2']))
        elements.append(Paragraph(f"Generated on: {self.db.get_current_date()}", normal))
        elements.append(Spacer(1, 12))

        # Table Data
        headers = [self.report_table.horizontalHeaderItem(i).text() for i in range(self.report_table.columnCount())]
        data = [headers]
        for row in range(self.report_table.rowCount()):
            row_data = [self.report_table.item(row, col).text() for col in range(self.report_table.columnCount())]
            data.append(row_data)

        # Calculate column widths dynamically based on content
        col_widths = [pdf.width / len(headers)] * len(headers)  # Evenly distribute initially
        # Adjust for specific reports
        if report_type == "Patient Summary":
            col_widths = [15*mm, 40*mm, 40*mm, 20*mm, 25*mm, 40*mm]
        elif report_type == "Prescription History":
            col_widths = [15*mm, 40*mm, 40*mm, 30*mm, 30*mm, 25*mm]
        elif report_type == "Inventory Status":
            col_widths = [15*mm, 40*mm, 25*mm, 35*mm, 30*mm, 25*mm]
        elif report_type == "Sales Report":
            col_widths = [25*mm, 50*mm, 35*mm, 30*mm]
        elif report_type == "Low Stock Alert":
            col_widths = [25*mm, 60*mm, 30*mm]

        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        # Footer
        elements.append(Paragraph("Thank you for choosing Wabuko Health Clinic!", normal_center))
        elements.append(Paragraph("Contact: +234 700 123 4567 | info@wabukohealth.ng", normal_center))
        elements.append(Spacer(1, 4))

        # Build with canvas setup for background and logos
        def on_page(canvas, doc):
            # Background Image (faded hospital theme)
            canvas.saveState()
            canvas.setFillAlpha(0.2)  # Faded effect
            canvas.drawImage('database/hospital_bg2.jpg', 20*mm, 20*mm, width=A4[0]-40*mm, height=A4[1]-40*mm, mask='auto')
            canvas.restoreState()

            # Logo (Top Left)
            canvas.drawImage('database/logo2.jpg', 20*mm, A4[1]-30*mm, width=50*mm, height=50*mm, mask='auto')

            # Logo (Bottom Right)
            canvas.drawImage('database/logo2.jpg', A4[0]-70*mm, 20*mm, width=50*mm, height=50*mm, mask='auto')

        pdf.build(elements, onFirstPage=on_page, onLaterPages=on_page)
        QMessageBox.information(self, "Success", f"Report exported to {file_path}")
