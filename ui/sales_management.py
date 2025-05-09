from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QComboBox, QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog)
from PyQt6.QtCore import QDate
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from db.database import Database
import os

class SalesManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.sale_items = []
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Patient selection
        patient_layout = QHBoxLayout()
        self.patient_search = QLineEdit()
        self.patient_search.setPlaceholderText("Search by patient name...")
        self.patient_search.textChanged.connect(self.search_patients)
        self.patient_combo = QComboBox()
        patient_layout.addWidget(self.patient_search)
        patient_layout.addWidget(self.patient_combo)

        # Drug selection
        drug_layout = QHBoxLayout()
        self.drug_combo = QComboBox()
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")
        add_drug_button = QPushButton("Add Drug")
        add_drug_button.clicked.connect(self.add_drug_to_sale)
        drug_layout.addWidget(self.drug_combo)
        drug_layout.addWidget(self.quantity_input)
        drug_layout.addWidget(add_drug_button)

        # Form layout
        form_layout = QFormLayout()
        form_layout.addRow("Patient:", patient_layout)
        form_layout.addRow("Drug:", drug_layout)
        self.total_label = QLineEdit()
        self.total_label.setReadOnly(True)
        form_layout.addRow("Total Price (KES):", self.total_label)

        # Table for sale items
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Drug ID", "Name", "Quantity", "Unit Price", "Subtotal"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Sale")
        clear_button = QPushButton("Clear")
        back_button = QPushButton("Back")
        save_button.clicked.connect(self.save_sale)
        clear_button.clicked.connect(self.clear_form)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(back_button)

        # Add to main layout
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)

        # Populate dropdowns
        self.populate_patients()
        self.populate_drugs()

    def populate_patients(self, patients=None):
        """Populate patient dropdown, optionally filtered."""
        self.patient_combo.clear()
        if patients is None:
            patients = self.db.get_all_patients()
        for patient in patients:
            self.patient_combo.addItem(
                f"{patient['first_name']} {patient['last_name']}",
                patient['patient_id']
            )

    def search_patients(self):
        """Filter patients in dropdown based on search term."""
        search_term = self.patient_search.text().strip()
        if search_term:
            patients = self.db.search_patients(search_term)
        else:
            patients = self.db.get_all_patients()
        self.populate_patients(patients)

    def populate_drugs(self):
        """Populate drug dropdown with available inventory."""
        self.drug_combo.clear()
        drugs = self.db.get_all_drugs()
        for drug in drugs:
            if drug['quantity'] > 0:  # Only show drugs with stock
                self.drug_combo.addItem(
                    f"{drug['name']} (Stock: {drug['quantity']})",
                    {'drug_id': drug['drug_id'], 'name': drug['name'], 'price': drug['price']}
                )

    def add_drug_to_sale(self):
        """Add selected drug and quantity to the sale table."""
        drug_data = self.drug_combo.currentData()
        quantity_text = self.quantity_input.text().strip()

        if not drug_data or not quantity_text:
            QMessageBox.warning(self, "Input Error", "Please select a drug and enter a quantity.")
            return

        try:
            quantity = int(quantity_text)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity must be a positive integer.")
            return

        # Check stock
        drug_id = drug_data['drug_id']
        drugs = self.db.get_all_drugs()
        drug = next(d for d in drugs if d['drug_id'] == drug_id)
        if quantity > drug['quantity']:
            QMessageBox.warning(self, "Stock Error", f"Only {drug['quantity']} units available for {drug['name']}.")
            return

        # Add to sale items
        item = {
            'drug_id': drug_id,
            'name': drug_data['name'],
            'quantity': quantity,
            'price': drug_data['price'],
            'subtotal': quantity * drug_data['price']
        }
        self.sale_items.append(item)
        self.update_sale_table()
        self.quantity_input.clear()

    def update_sale_table(self):
        """Update the sale items table and total price."""
        self.table.setRowCount(len(self.sale_items))
        total_price = 0
        for row, item in enumerate(self.sale_items):
            self.table.setItem(row, 0, QTableWidgetItem(str(item['drug_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(item['name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(item['quantity'])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{item['price']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{item['subtotal']:.2f}"))
            total_price += item['subtotal']
        self.total_label.setText(f"{total_price:.2f}")

    def save_sale(self):
        """Save the sale, update inventory, and generate PDF receipt."""
        patient_id = self.patient_combo.currentData()
        if not patient_id or not self.sale_items:
            QMessageBox.warning(self, "Input Error", "Please select a patient and add at least one drug.")
            return

        total_price = sum(item['subtotal'] for item in self.sale_items)
        try:
            # Save sale to database
            sale_id = self.db.add_sale(
                patient_id=patient_id,
                user_id=1,  # Placeholder until login system
                total_price=total_price,
                items=self.sale_items
            )

            # Generate PDF receipt
            self.generate_receipt(sale_id)

            QMessageBox.information(self, "Success", "Sale saved successfully. Receipt generated.")
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Stock Error", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save sale: {str(e)}")

    def generate_receipt(self, sale_id):
        """Generate a PDF receipt for the sale."""
        sale_details = self.db.get_sale_details(sale_id)
        sale = sale_details['sale']
        items = sale_details['items']

        # Open file dialog to choose save location
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Receipt", f"sale_{sale_id}_receipt.pdf", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        c = canvas.Canvas(file_path, pagesize=A4)
        c.setFont("Helvetica", 12)
        y = 800

        # Header
        c.drawString(100, y, "MicroClinicPlus Pharmacy")
        c.drawString(100, y - 20, "Sale Receipt")
        y -= 50

        # Sale details
        c.drawString(100, y, f"Sale ID: {sale['sale_id']}")
        c.drawString(100, y - 20, f"Date: {sale['sale_date']}")
        c.drawString(100, y - 40, f"Patient: {sale['first_name']} {sale['last_name']}")
        y -= 80

        # Items table
        c.drawString(100, y, "Items:")
        c.drawString(100, y - 20, "Drug Name")
        c.drawString(250, y - 20, "Quantity")
        c.drawString(350, y - 20, "Unit Price")
        c.drawString(450, y - 20, "Subtotal")
        y -= 40

        for item in items:
            c.drawString(100, y, item['name'])
            c.drawString(250, y, str(item['quantity_sold']))
            c.drawString(350, y, f"{item['unit_price']:.2f}")
            c.drawString(450, y, f"{item['quantity_sold'] * item['unit_price']:.2f}")
            y -= 20

        # Total
        y -= 20
        c.drawString(100, y, f"Total Price: KES {sale['total_price']:.2f}")

        c.showPage()
        c.save()

    def clear_form(self):
        """Clear all inputs and reset sale items."""
        self.patient_search.clear()
        self.populate_patients()
        self.quantity_input.clear()
        self.sale_items = []
        self.update_sale_table()
        self.total_label.clear()
