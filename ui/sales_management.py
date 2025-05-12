from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm


class SalesManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.sale_items = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Form for adding sale items
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
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setToolTip("Enter quantity sold")
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
        right_form.addWidget(QLabel("Drug:"))
        right_form.addWidget(self.drug_combo)
        right_form.addWidget(QLabel("Quantity:"))
        right_form.addWidget(self.quantity_input)

        form_layout.addLayout(left_form)
        form_layout.addLayout(right_form)
        main_layout.addLayout(form_layout)

        # Buttons for sale items
        item_button_layout = QHBoxLayout()
        add_item_button = QPushButton("Add Item")
        add_item_button.setToolTip("Add drug to sale")
        add_item_button.setStyleSheet("""
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
        clear_items_button = QPushButton("Clear Items")
        clear_items_button.setToolTip("Clear sale items")
        clear_items_button.setStyleSheet("""
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
        add_item_button.clicked.connect(self.add_sale_item)
        clear_items_button.clicked.connect(self.clear_sale_items)
        item_button_layout.addWidget(add_item_button)
        item_button_layout.addWidget(clear_items_button)
        main_layout.addLayout(item_button_layout)

        # Sale items table
        self.sale_items_table = QTableWidget()
        self.sale_items_table.setColumnCount(3)
        self.sale_items_table.setHorizontalHeaderLabels(["Drug", "Quantity", "Price"])
        self.sale_items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sale_items_table.setToolTip("Current sale items")
        self.sale_items_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        main_layout.addWidget(self.sale_items_table)

        # Sale buttons
        sale_button_layout = QHBoxLayout()
        complete_sale_button = QPushButton("Complete Sale")
        complete_sale_button.setToolTip("Finalize the sale")
        complete_sale_button.setStyleSheet("""
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
        generate_receipt_button = QPushButton("Generate Receipt")
        generate_receipt_button.setToolTip("Export sale receipt to PDF")
        generate_receipt_button.setStyleSheet("""
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
        complete_sale_button.clicked.connect(self.complete_sale)
        generate_receipt_button.clicked.connect(self.generate_receipt)
        back_button.clicked.connect(self.main_window.show_menu)
        sale_button_layout.addWidget(complete_sale_button)
        sale_button_layout.addWidget(generate_receipt_button)
        sale_button_layout.addWidget(back_button)
        main_layout.addLayout(sale_button_layout)

        # Sales table
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(4)
        self.sales_table.setHorizontalHeaderLabels(["Sale ID", "Patient", "Total Price", "Date"])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sales_table.setToolTip("List of completed sales")
        self.sales_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        main_layout.addWidget(self.sales_table)

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

        sales = self.db.get_all_sales()
        self.sales_table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            patient = self.db.get_patient(sale['patient_id'])
            self.sales_table.setItem(row, 0, QTableWidgetItem(str(sale['sale_id'])))
            self.sales_table.setItem(row, 1, QTableWidgetItem(f"{patient['first_name']} {patient['last_name']}"))
            self.sales_table.setItem(row, 2, QTableWidgetItem(f"{sale['total_price']:.2f}"))
            self.sales_table.setItem(row, 3, QTableWidgetItem(sale['sale_date']))

    def add_sale_item(self):
        drug_id = self.drug_combo.currentData()
        quantity = self.quantity_input.text().strip()

        if not drug_id or self.drug_combo.currentText() == "Select Drug":
            QMessageBox.warning(self, "Error", "Please select a drug.")
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

        drug = self.db.get_drug(drug_id)
        self.sale_items.append({
            'drug_id': drug_id,
            'name': drug['name'],
            'quantity': quantity_val,
            'price': drug['price'] * quantity_val
        })

        self.sale_items_table.setRowCount(len(self.sale_items))
        for row, item in enumerate(self.sale_items):
            self.sale_items_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.sale_items_table.setItem(row, 1, QTableWidgetItem(str(item['quantity'])))
            self.sale_items_table.setItem(row, 2, QTableWidgetItem(f"{item['price']:.2f}"))

        self.quantity_input.clear()

    def clear_sale_items(self):
        self.sale_items = []
        self.sale_items_table.setRowCount(0)
        self.quantity_input.clear()

    def complete_sale(self):
        patient_id = self.patient_combo.currentData()
        if not patient_id or self.patient_combo.currentText() == "Select Patient":
            QMessageBox.warning(self, "Error", "Please select a patient.")
            return
        if not self.sale_items:
            QMessageBox.warning(self, "Error", "No items added to sale.")
            return

        total_price = sum(item['price'] for item in self.sale_items)
        try:
            sale_id = self.db.add_sale(
                patient_id=patient_id,
                user_id=self.main_window.current_user['user_id'],
                total_price=total_price
            )
            for item in self.sale_items:
                self.db.add_sale_item(
                    sale_id=sale_id,
                    drug_id=item['drug_id'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            QMessageBox.information(self, "Success", f"Sale completed successfully. Sale ID: {sale_id}")
            self.load_data()
            self.clear_sale_items()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def generate_receipt(self):
        """Generate a slick PDF receipt with clean styling."""
        row = self.sales_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select a sale to generate receipt.")
            return

        sale_id = int(self.sales_table.item(row, 0).text())
        sale = self.db.get_sale(sale_id)
        patient = self.db.get_patient(sale['patient_id'])
        sale_items = sale['items']

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Receipt", f"receipt_{sale_id}.pdf", "PDF Files (*.pdf)"
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
        small = ParagraphStyle(
            'Small', parent=styles['Normal'], fontSize=8, leading=10)

        elements = []

        # Header Block
        elements.append(Paragraph("Wabuko Health Clinic", header_style))
        elements.append(Paragraph("123 Moi Avenue, Nairobi, Kenya", normal_center))
        elements.append(Paragraph("Phone: +234 700 123 4567 | info@wabukohealth.ng", normal_center))
        elements.append(Spacer(1, 4))
        elements.append(HRFlowable(width=doc.width, thickness=0.5, color=colors.black))
        elements.append(Spacer(1, 8))

        # Receipt Metadata
        receipt_id = f"RCPT-{sale['sale_date'][:10].replace('-', '')}-{sale_id:04d}"
        meta_data = [
            ["Receipt ID:", receipt_id],
            ["Date:", sale['sale_date'][:10]],
            ["Time:", sale['sale_date'][11:16]],
            ["Issued By:", self.main_window.current_user['username']]
        ]
        meta_table = Table(meta_data, colWidths=[40*mm, doc.width-40*mm])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 12))

        # Patient Info
        patient_data = [
            ["Patient Name:", f"{patient['first_name']} {patient['last_name']}"],
            ["Patient ID:", f"PT-{patient['patient_id']:05d}"],
            ["Date of Birth:", patient.get('dob', 'N/A')]
        ]
        pat_table = Table(patient_data, colWidths=[40*mm, doc.width-40*mm])
        pat_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(pat_table)
        elements.append(Spacer(1, 12))

        # Items Table
        data = [["#", "Item / Service", "Qty", "Unit Price", "Total"]]
        for i, item in enumerate(sale_items, 1):
            unit_price = item['price'] / item['quantity'] if item['quantity'] else 0
            data.append([
                str(i),
                item['name'],
                str(item['quantity']),
                f"KSh. {unit_price:,.2f}",
                f"KSh. {item['price']:,.2f}"
            ])

        items_table = Table(data, colWidths=[
            10*mm, 70*mm, 15*mm, 30*mm, 30*mm
        ])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (2,1), (-1,-1), 'RIGHT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 11),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('TOPPADDING', (0,0), (-1,0), 6),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 12))

        # Summary Calculations
        subtotal = sum(it['price'] for it in sale_items)
        tax_rate = 0.075
        tax = subtotal * tax_rate
        total = subtotal + tax

        summary = [
            ["Subtotal:", f"KSh. {subtotal:,.2f}"],
            ["Tax (7.5%):", f"KSh. {tax:,.2f}"],
            ["Total Payable:", f"KSh. {total:,.2f}"]
        ]
        summary_table = Table(summary, colWidths=[doc.width-40*mm, 40*mm])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('LINEABOVE', (0,-1), (-1,-1), 1, colors.black),
            ('TOPPADDING', (0,-1), (-1,-1), 6),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 18))

        # Footer
        elements.append(Paragraph("Thank you for choosing Wabuko Health Clinic!", normal_center))
        elements.append(Paragraph("<i>Powered by Wabuko Software</i>", small))

        # Build!
        doc.build(elements)
        QMessageBox.information(self, "Success", f"Receipt saved to:\n{file_path}")
