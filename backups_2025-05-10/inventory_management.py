from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database

class InventoryManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Form for managing drugs
        form_layout = QHBoxLayout()
        left_form = QVBoxLayout()
        right_form = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter drug - Drug name")
        self.name_input.setToolTip("Enter drug name")
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
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setToolTip("Enter drug quantity")
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
        self.batch_number_input = QLineEdit()
        self.batch_number_input.setPlaceholderText("Enter batch number")
        self.batch_number_input.setToolTip("Enter batch number")
        self.batch_number_input.setStyleSheet("""
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
        self.expiry_date_input = QLineEdit()
        self.expiry_date_input.setPlaceholderText("YYYY-MM-DD")
        self.expiry_date_input.setToolTip("Enter expiry date")
        self.expiry_date_input.setStyleSheet("""
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
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter price")
        self.price_input.setToolTip("Enter drug price")
        self.price_input.setStyleSheet("""
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

        left_form.addWidget(QLabel("Drug Name:"))
        left_form.addWidget(self.name_input)
        left_form.addWidget(QLabel("Quantity:"))
        left_form.addWidget(self.quantity_input)
        right_form.addWidget(QLabel("Batch Number:"))
        right_form.addWidget(self.batch_number_input)
        right_form.addWidget(QLabel("Expiry Date:"))
        right_form.addWidget(self.expiry_date_input)
        right_form.addWidget(QLabel("Price:"))
        right_form.addWidget(self.price_input)

        form_layout.addLayout(left_form)
        form_layout.addLayout(right_form)
        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Drug")
        add_button.setToolTip("Add new drug to inventory")
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
        update_button = QPushButton("Update Drug")
        update_button.setToolTip("Update selected drug")
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
        delete_button = QPushButton("Delete Drug")
        delete_button.setToolTip("Delete selected drug")
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
        add_button.clicked.connect(self.add_drug)
        update_button.clicked.connect(self.update_drug)
        delete_button.clicked.connect(self.delete_drug)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

        # Drug table
        self.drug_table = QTableWidget()
        self.drug_table.setColumnCount(6)
        self.drug_table.setHorizontalHeaderLabels(["ID", "Name", "Quantity", "Batch Number", "Expiry Date", "Price"])
        self.drug_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.drug_table.setToolTip("List of drugs in inventory")
        self.drug_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.drug_table.clicked.connect(self.load_drug_to_form)
        main_layout.addWidget(self.drug_table)

        main_layout.addStretch()

        self.load_drugs()

    def load_drugs(self):
        drugs = self.db.get_all_drugs()
        self.drug_table.setRowCount(len(drugs))
        for row, drug in enumerate(drugs):
            self.drug_table.setItem(row, 0, QTableWidgetItem(str(drug['drug_id'])))
            self.drug_table.setItem(row, 1, QTableWidgetItem(drug['name']))
            self.drug_table.setItem(row, 2, QTableWidgetItem(str(drug['quantity'])))
            self.drug_table.setItem(row, 3, QTableWidgetItem(drug['batch_number']))
            self.drug_table.setItem(row, 4, QTableWidgetItem(drug['expiry_date']))
            self.drug_table.setItem(row, 5, QTableWidgetItem(f"{drug['price']:.2f}"))

    def load_drug_to_form(self):
        row = self.drug_table.currentRow()
        if row >= 0:
            self.name_input.setText(self.drug_table.item(row, 1).text())
            self.quantity_input.setText(self.drug_table.item(row, 2).text())
            self.batch_number_input.setText(self.drug_table.item(row, 3).text())
            self.expiry_date_input.setText(self.drug_table.item(row, 4).text())
            self.price_input.setText(self.drug_table.item(row, 5).text())

    def add_drug(self):
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        batch_number = self.batch_number_input.text().strip()
        expiry_date = self.expiry_date_input.text().strip()
        price = self.price_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Error", "Drug name is required.")
            return
        if not quantity:
            QMessageBox.warning(self, "Error", "Quantity is required.")
            return
        try:
            quantity_val = int(quantity)
            if quantity_val < 0:
                QMessageBox.warning(self, "Error", "Quantity cannot be negative.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Quantity must be a number.")
            return
        if not batch_number:
            QMessageBox.warning(self, "Error", "Batch number is required.")
            return
        if not expiry_date:
            QMessageBox.warning(self, "Error", "Expiry date is required.")
            return
        if not price:
            QMessageBox.warning(self, "Error", "Price is required.")
            return
        try:
            price_val = float(price)
            if price_val < 0:
                QMessageBox.warning(self, "Error", "Price cannot be negative.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Price must be a number.")
            return

        self.db.add_drug(name, quantity_val, batch_number, expiry_date, price_val)
        QMessageBox.information(self, "Success", "Drug added successfully.")
        self.load_drugs()
        self.clear_form()

    def update_drug(self):
        row = self.drug_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a drug to update.")
            return

        drug_id = int(self.drug_table.item(row, 0).text())
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        batch_number = self.batch_number_input.text().strip()
        expiry_date = self.expiry_date_input.text().strip()
        price = self.price_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Error", "Drug name is required.")
            return
        if not quantity:
            QMessageBox.warning(self, "Error", "Quantity is required.")
            return
        try:
            quantity_val = int(quantity)
            if quantity_val < 0:
                QMessageBox.warning(self, "Error", "Quantity cannot be negative.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Quantity must be a number.")
            return
        if not batch_number:
            QMessageBox.warning(self, "Error", "Batch number is required.")
            return
        if not expiry_date:
            QMessageBox.warning(self, "Error", "Expiry date is required.")
            return
        if not price:
            QMessageBox.warning(self, "Error", "Price is required.")
            return
        try:
            price_val = float(price)
            if price_val < 0:
                QMessageBox.warning(self, "Error", "Price cannot be negative.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Price must be a number.")
            return

        self.db.update_drug(drug_id, name, quantity_val, batch_number, expiry_date, price_val)
        QMessageBox.information(self, "Success", "Drug updated successfully.")
        self.load_drugs()
        self.clear_form()

    def delete_drug(self):
        row = self.drug_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a drug to delete.")
            return

        drug_id = int(self.drug_table.item(row, 0).text())
        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this drug?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_drug(drug_id)
            QMessageBox.information(self, "Success", "Drug deleted successfully.")
            self.load_drugs()
            self.clear_form()

    def clear_form(self):
        self.name_input.clear()
        self.quantity_input.clear()
        self.batch_number_input.clear()
        self.expiry_date_input.clear()
        self.price_input.clear()
