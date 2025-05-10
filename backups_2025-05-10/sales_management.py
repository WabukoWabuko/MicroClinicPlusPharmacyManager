from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

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
                border/gu: 1px solid #4CAF50;
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
                total_price=total_price,
                sale_items=self.sale_items
            )
            QMessageBox.information(self, "Success", f"Sale completed successfully. Sale ID: {sale_id}")
            self.load_data()
            self.clear_sale_items()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def generate_receipt(self):
        row = self.sales_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a sale to generate a receipt.")
            return

        sale_id = int(self.sales_table.item(row, 0).text())
        sale = self.db.get_sale(sale_id)
        patient = self.db.get_patient(sale['patient_id'])
        sale_items = self.db.get_sale_items(sale_id)

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Receipt", f"sale_{sale_id}_receipt.pdf", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        pdf = SimpleDocTemplate(file_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("MicroClinicPlus Pharmacy", styles['Heading1']))
        elements.append(Paragraph(f"Sale Receipt - Sale ID: {sale_id}", styles['Heading2']))
        elements.append(Paragraph(f"Patient: {patient['first_name']} {patient['last_name']}", styles['Normal']))
        elements.append(Paragraph(f"Date: {sale['sale_date']}", styles['Normal']))
        elements.append(Spacer(1, 12))

        data = [["Drug", "Quantity", "Price"]]
        for item in sale_items:
            data.append([item['name'], str(item['quantity']), f"{item['price']:.2f}"])
        data.append(["Total", "", f"{sale['total_price']:.2f}"])

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

        elements.append(Paragraph("Thank you for your purchase!", styles['Normal']))
        pdf.build(elements)
        QMessageBox.information(self, "Success", f"Receipt exported to {file_path}")
