from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database

class SupplierManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.selected_supplier_id = None  # To track the supplier being edited
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Form for supplier details
        form_layout = QHBoxLayout()
        left_form = QVBoxLayout()
        right_form = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter supplier name")
        self.name_input.setToolTip("Supplier's name (required)")
        self.name_input.setStyleSheet("""
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
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        self.phone_input.setToolTip("Supplier's phone number")
        self.phone_input.setStyleSheet("""
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
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        self.email_input.setToolTip("Supplier's email")
        self.email_input.setStyleSheet("""
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
        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Enter address")
        self.address_input.setToolTip("Supplier's address")
        self.address_input.setStyleSheet("""
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
        self.products_input = QTextEdit()
        self.products_input.setPlaceholderText("Enter products supplied (e.g., Paracetamol, Amoxicillin)")
        self.products_input.setToolTip("List of products supplied by this supplier")
        self.products_input.setStyleSheet("""
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
        self.last_delivery_input = QLineEdit()
        self.last_delivery_input.setPlaceholderText("YYYY-MM-DD (e.g., 2025-05-12)")
        self.last_delivery_input.setToolTip("Last delivery date")
        self.last_delivery_input.setStyleSheet("""
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
        self.responsible_person_input = QLineEdit()
        self.responsible_person_input.setPlaceholderText("Enter responsible person's name")
        self.responsible_person_input.setToolTip("Name of the contact person")
        self.responsible_person_input.setStyleSheet("""
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
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Enter additional notes")
        self.notes_input.setToolTip("Additional information about the supplier")
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

        left_form.addWidget(QLabel("Supplier Name:"))
        left_form.addWidget(self.name_input)
        left_form.addWidget(QLabel("Phone:"))
        left_form.addWidget(self.phone_input)
        left_form.addWidget(QLabel("Email:"))
        left_form.addWidget(self.email_input)
        left_form.addWidget(QLabel("Address:"))
        left_form.addWidget(self.address_input)
        right_form.addWidget(QLabel("Products Supplied:"))
        right_form.addWidget(self.products_input)
        right_form.addWidget(QLabel("Last Delivery Date:"))
        right_form.addWidget(self.last_delivery_input)
        right_form.addWidget(QLabel("Responsible Person:"))
        right_form.addWidget(self.responsible_person_input)
        right_form.addWidget(QLabel("Notes:"))
        right_form.addWidget(self.notes_input)

        form_layout.addLayout(left_form)
        form_layout.addLayout(right_form)
        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Supplier")
        add_button.setToolTip("Add new supplier")
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
        update_button = QPushButton("Update Supplier")
        update_button.setToolTip("Update selected supplier")
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
        add_button.clicked.connect(self.add_supplier)
        update_button.clicked.connect(self.update_supplier)
        clear_button.clicked.connect(self.clear_form)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

        # Suppliers table
        self.supplier_table = QTableWidget()
        self.supplier_table.setColumnCount(7)
        self.supplier_table.setHorizontalHeaderLabels([
            "ID", "Name", "Contact", "Products", "Last Delivery", "Responsible Person", "Notes"
        ])
        self.supplier_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.supplier_table.setToolTip("List of suppliers")
        self.supplier_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.supplier_table.clicked.connect(self.load_supplier_to_form)
        main_layout.addWidget(self.supplier_table)

        main_layout.addStretch()

        self.load_data()

    def load_data(self):
        suppliers = self.db.get_all_suppliers()
        self.supplier_table.setRowCount(len(suppliers))
        for row, supplier in enumerate(suppliers):
            self.supplier_table.setItem(row, 0, QTableWidgetItem(str(supplier['supplier_id'])))
            self.supplier_table.setItem(row, 1, QTableWidgetItem(supplier['name']))
            contact = f"Phone: {supplier['phone']}\nEmail: {supplier['email']}\nAddress: {supplier['address']}"
            self.supplier_table.setItem(row, 2, QTableWidgetItem(contact))
            self.supplier_table.setItem(row, 3, QTableWidgetItem(supplier['products_supplied']))
            self.supplier_table.setItem(row, 4, QTableWidgetItem(supplier['last_delivery_date'] or "N/A"))
            self.supplier_table.setItem(row, 5, QTableWidgetItem(supplier['responsible_person'] or "N/A"))
            self.supplier_table.setItem(row, 6, QTableWidgetItem(supplier['notes'] or "N/A"))

    def load_supplier_to_form(self):
        row = self.supplier_table.currentRow()
        if row < 0:
            return

        self.selected_supplier_id = int(self.supplier_table.item(row, 0).text())
        supplier = self.db.get_supplier(self.selected_supplier_id)
        self.name_input.setText(supplier['name'])
        self.phone_input.setText(supplier['phone'])
        self.email_input.setText(supplier['email'])
        self.address_input.setText(supplier['address'])
        self.products_input.setText(supplier['products_supplied'])
        self.last_delivery_input.setText(supplier['last_delivery_date'])
        self.responsible_person_input.setText(supplier['responsible_person'])
        self.notes_input.setText(supplier['notes'])

    def add_supplier(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.toPlainText().strip()
        products = self.products_input.toPlainText().strip()
        last_delivery = self.last_delivery_input.text().strip()
        responsible_person = self.responsible_person_input.text().strip()
        notes = self.notes_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Error", "Supplier name is required.")
            return

        # Basic date format validation (YYYY-MM-DD)
        import re
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if last_delivery and not re.match(date_pattern, last_delivery):
            QMessageBox.warning(self, "Error", "Last delivery date must be in YYYY-MM-DD format (e.g., 2025-05-12).")
            return

        try:
            self.db.add_supplier(
                name=name,
                phone=phone,
                email=email,
                address=address,
                products_supplied=products,
                last_delivery_date=last_delivery,
                responsible_person=responsible_person,
                notes=notes
            )
            QMessageBox.information(self, "Success", "Supplier added successfully.")
            self.load_data()
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def update_supplier(self):
        if not self.selected_supplier_id:
            QMessageBox.warning(self, "Error", "Please select a supplier to update.")
            return

        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.toPlainText().strip()
        products = self.products_input.toPlainText().strip()
        last_delivery = self.last_delivery_input.text().strip()
        responsible_person = self.responsible_person_input.text().strip()
        notes = self.notes_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Error", "Supplier name is required.")
            return

        # Basic date format validation (YYYY-MM-DD)
        import re
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if last_delivery and not re.match(date_pattern, last_delivery):
            QMessageBox.warning(self, "Error", "Last delivery date must be in YYYY-MM-DD format (e.g., 2025-05-12).")
            return

        try:
            self.db.update_supplier(
                supplier_id=self.selected_supplier_id,
                name=name,
                phone=phone,
                email=email,
                address=address,
                products_supplied=products,
                last_delivery_date=last_delivery,
                responsible_person=responsible_person,
                notes=notes
            )
            QMessageBox.information(self, "Success", "Supplier updated successfully.")
            self.load_data()
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def clear_form(self):
        self.selected_supplier_id = None
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.products_input.clear()
        self.last_delivery_input.clear()
        self.responsible_person_input.clear()
        self.notes_input.clear()
