from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from utils.validation import is_valid_quantity

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

        # Patient selection
        patient_layout = QHBoxLayout()
        patient_label = QLabel("Select Patient:")
        self.patient_combo = QComboBox()
        self.patient_combo.addItem("Select Patient", None)
        patient_layout.addWidget(patient_label)
        patient_layout.addWidget(self.patient_combo)
        main_layout.addLayout(patient_layout)

        # Drug selection and quantity
        drug_layout = QHBoxLayout()
        drug_label = QLabel("Drug:")
        self.drug_combo = QComboBox()
        quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        price_label = QLabel("Price:")
        self.price_input = QLineEdit()
        self.price_input.setReadOnly(True)
        add_item_button = QPushButton("Add Item")
        add_item_button.clicked.connect(self.add_sale_item)
        drug_layout.addWidget(drug_label)
        drug_layout.addWidget(self.drug_combo)
        drug_layout.addWidget(quantity_label)
        drug_layout.addWidget(self.quantity_input)
        drug_layout.addWidget(price_label)
        drug_layout.addWidget(self.price_input)
        drug_layout.addWidget(add_item_button)
        main_layout.addLayout(drug_layout)

        # Sale items table
        self.sale_items_table = QTableWidget()
        self.sale_items_table.setColumnCount(4)
        self.sale_items_table.setHorizontalHeaderLabels(["Drug Name", "Quantity", "Price", "Subtotal"])
        self.sale_items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.sale_items_table)

        # Buttons
        button_layout = QHBoxLayout()
        submit_sale_button = QPushButton("Submit Sale")
        clear_button = QPushButton("Clear")
        back_button = QPushButton("Back")
        submit_sale_button.clicked.connect(self.add_sale)
        clear_button.clicked.connect(self.clear_sale)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(submit_sale_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

        # Load data
        self.load_patients()
        self.load_drugs()

    def load_patients(self):
        patients = self.db.get_all_patients()
        self.patient_combo.clear()
        self.patient_combo.addItem("Select Patient", None)
        for patient in patients:
            self.patient_combo.addItem(
                f"{patient['first_name']} {patient['last_name']}", patient['patient_id']
            )

    def load_drugs(self):
        drugs = self.db.get_all_drugs()
        self.drug_combo.clear()
        self.drug_combo.addItem("Select Drug", None)
        for drug in drugs:
            self.drug_combo.addItem(drug['name'], {'drug_id': drug['drug_id'], 'price': drug['price']})
        self.drug_combo.currentIndexChanged.connect(self.update_price)

    def update_price(self):
        drug_data = self.drug_combo.currentData()
        if drug_data:
            self.price_input.setText(f"{drug_data['price']:.2f}")
        else:
            self.price_input.clear()

    def add_sale_item(self):
        drug_data = self.drug_combo.currentData()
        quantity = self.quantity_input.text().strip()

        # Reset styles
        self.quantity_input.setStyleSheet("")

        # Validate inputs
        if not drug_data:
            QMessageBox.warning(self, "Error", "Please select a drug.")
            return

        is_valid, error = is_valid_quantity(quantity)
        if not is_valid:
            self.quantity_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        try:
            quantity_val = int(quantity)
            drug = self.db.get_drug(drug_data['drug_id'])
            if drug['quantity'] < quantity_val:
                self.quantity_input.setStyleSheet("border: 1px solid red;")
                QMessageBox.warning(self, "Error", f"Insufficient stock for {drug['name']}. Available: {drug['quantity']}")
                return
            self.sale_items.append({
                'drug_id': drug_data['drug_id'],
                'name': drug['name'],
                'quantity': quantity_val,
                'price': drug_data['price']
            })
            self.load_sale_items()
            self.quantity_input.clear()
        except ValueError as e:
            self.quantity_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", str(e))

    def load_sale_items(self):
        self.sale_items_table.setRowCount(len(self.sale_items))
        for row, item in enumerate(self.sale_items):
            self.sale_items_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.sale_items_table.setItem(row, 1, QTableWidgetItem(str(item['quantity'])))
            self.sale_items_table.setItem(row, 2, QTableWidgetItem(f"{item['price']:.2f}"))
            self.sale_items_table.setItem(row, 3, QTableWidgetItem(f"{item['quantity'] * item['price']:.2f}"))

    def clear_sale(self):
        self.sale_items = []
        self.load_sale_items()
        self.patient_combo.setCurrentIndex(0)
        self.drug_combo.setCurrentIndex(0)
        self.quantity_input.clear()
        self.price_input.clear()
        self.quantity_input.setStyleSheet("")

    def add_sale(self):
        patient_id = self.patient_combo.currentData()
        if not patient_id:
            QMessageBox.warning(self, "Error", "Please select a patient.")
            return

        if not self.sale_items:
            QMessageBox.warning(self, "Error", "No items added to the sale.")
            return

        try:
            total_price = sum(item['quantity'] * item['price'] for item in self.sale_items)
            sale_id = self.db.add_sale(
                patient_id, self.main_window.current_user['user_id'], total_price, self.sale_items
            )
            patient = self.db.get_patient(patient_id)
            patient_name = f"{patient['first_name']} {patient['last_name']}"
            patient_contact = patient['contact']
            sale_date = self.db.get_sale(sale_id)['sale_date']
            self.generate_receipt(sale_id, patient_name, patient_contact, self.sale_items, total_price, sale_date)
            QMessageBox.information(self, "Success", f"Sale added successfully. Sale ID: {sale_id}")
            self.sale_items = []
            self.load_sale_items()
            self.main_window.check_low_stock_alerts()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def generate_receipt(self, sale_id, patient_name, patient_contact, sale_items, total_price, sale_date):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Receipt", f"receipt_{sale_id}.pdf", "PDF Files (*.pdf)")
        if not file_path:
            return

        pdf = SimpleDocTemplate(file_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            try:
                elements.append(Image(logo_path, width=100, height=100))
            except Exception as e:
                elements.append(Paragraph(f"Error loading logo: {str(e)}", styles['Normal']))
        else:
            elements.append(Paragraph("MicroClinicPlus Logo", styles['Normal']))
        elements.append(Paragraph("MicroClinicPlus Pharmacy", styles['Heading1']))
        elements.append(Paragraph("Nairobi, Kenya", styles['Normal']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"Receipt ID: {sale_id}", styles['Normal']))
        elements.append(Paragraph(f"Date: {sale_date}", styles['Normal']))
        elements.append(Paragraph(f"Patient: {patient_name or 'N/A'}", styles['Normal']))
        elements.append(Paragraph(f"Contact: {patient_contact or 'N/A'}", styles['Normal']))
        elements.append(Spacer(1, 12))

        data = [["Drug", "Quantity", "Price (KES)", "Subtotal (KES)"]]
        for item in sale_items:
            data.append([
                item['name'],
                str(item['quantity']),
                f"{item['price']:.2f}",
                f"{item['quantity'] * item['price']:.2f}"
            ])
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

        elements.append(Paragraph(f"Total: KES {total_price:.2f}", styles['Heading2']))
        elements.append(Spacer(1, 24))

        elements.append(Paragraph("Thank you for choosing MicroClinicPlus!", styles['Normal']))
        elements.append(Paragraph("Contact: +254 700 123 456 | Email: info@microclinicplus.co.ke", styles['Normal']))

        pdf.build(elements)
        QMessageBox.information(self, "Success", f"Receipt saved to {file_path}")
