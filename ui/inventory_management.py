from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QLineEdit, QPushButton,
                             QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database
from utils.validation import is_valid_name, is_valid_quantity, is_valid_date, is_valid_price

class InventoryManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.selected_drug_id = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Inventory table
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels(["Drug ID", "Name", "Quantity", "Batch Number", "Expiry Date", "Price"])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.inventory_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.inventory_table.selectionModel().selectionChanged.connect(self.load_selected_drug)
        main_layout.addWidget(self.inventory_table)

        # Form for adding/editing drugs
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.batch_number_input = QLineEdit()
        self.expiry_date_input = QLineEdit()
        self.expiry_date_input.setPlaceholderText("YYYY-MM-DD")
        self.price_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Quantity:", self.quantity_input)
        form_layout.addRow("Batch Number:", self.batch_number_input)
        form_layout.addRow("Expiry Date:", self.expiry_date_input)
        form_layout.addRow("Price:", self.price_input)
        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Drug")
        self.update_button = QPushButton("Update Drug")
        self.delete_button = QPushButton("Delete Drug")
        self.back_button = QPushButton("Back")
        self.add_button.clicked.connect(self.add_drug)
        self.update_button.clicked.connect(self.update_drug)
        self.delete_button.clicked.connect(self.delete_drug)
        self.back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.back_button)
        main_layout.addLayout(button_layout)

        # Load inventory
        self.load_inventory()

    def load_inventory(self):
        drugs = self.db.get_all_drugs()
        self.inventory_table.setRowCount(len(drugs))
        for row, drug in enumerate(drugs):
            self.inventory_table.setItem(row, 0, QTableWidgetItem(str(drug['drug_id'])))
            self.inventory_table.setItem(row, 1, QTableWidgetItem(drug['name']))
            self.inventory_table.setItem(row, 2, QTableWidgetItem(str(drug['quantity'])))
            self.inventory_table.setItem(row, 3, QTableWidgetItem(drug['batch_number']))
            self.inventory_table.setItem(row, 4, QTableWidgetItem(drug['expiry_date']))
            self.inventory_table.setItem(row, 5, QTableWidgetItem(f"{drug['price']:.2f}"))
        self.clear_form()

    def load_selected_drug(self):
        selected = self.inventory_table.selectedItems()
        if selected:
            row = selected[0].row()
            self.selected_drug_id = int(self.inventory_table.item(row, 0).text())
            self.name_input.setText(self.inventory_table.item(row, 1).text())
            self.quantity_input.setText(self.inventory_table.item(row, 2).text())
            self.batch_number_input.setText(self.inventory_table.item(row, 3).text())
            self.expiry_date_input.setText(self.inventory_table.item(row, 4).text())
            self.price_input.setText(self.inventory_table.item(row, 5).text())

    def clear_form(self):
        self.selected_drug_id = None
        self.name_input.clear()
        self.quantity_input.clear()
        self.batch_number_input.clear()
        self.expiry_date_input.clear()
        self.price_input.clear()
        self.inventory_table.clearSelection()
        self.name_input.setStyleSheet("")
        self.quantity_input.setStyleSheet("")
        self.batch_number_input.setStyleSheet("")
        self.expiry_date_input.setStyleSheet("")
        self.price_input.setStyleSheet("")

    def add_drug(self):
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        batch_number = self.batch_number_input.text().strip()
        expiry_date = self.expiry_date_input.text().strip()
        price = self.price_input.text().strip()

        # Reset styles
        self.name_input.setStyleSheet("")
        self.quantity_input.setStyleSheet("")
        self.batch_number_input.setStyleSheet("")
        self.expiry_date_input.setStyleSheet("")
        self.price_input.setStyleSheet("")

        # Validate inputs
        is_valid, error = is_valid_name(name)
        if not is_valid:
            self.name_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_quantity(quantity)
        if not is_valid:
            self.quantity_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_name(batch_number)
        if not is_valid:
            self.batch_number_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_date(expiry_date)
        if not is_valid:
            self.expiry_date_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_price(price)
        if not is_valid:
            self.price_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        try:
            quantity_val = int(quantity)
            price_val = float(price)
            self.db.add_drug(name, quantity_val, batch_number, expiry_date, price_val)
            QMessageBox.information(self, "Success", "Drug added successfully.")
            self.load_inventory()
            self.main_window.check_low_stock_alerts()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def update_drug(self):
        if not self.selected_drug_id:
            QMessageBox.warning(self, "Error", "No drug selected.")
            return

        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        batch_number = self.batch_number_input.text().strip()
        expiry_date = self.expiry_date_input.text().strip()
        price = self.price_input.text().strip()

        # Reset styles
        self.name_input.setStyleSheet("")
        self.quantity_input.setStyleSheet("")
        self.batch_number_input.setStyleSheet("")
        self.expiry_date_input.setStyleSheet("")
        self.price_input.setStyleSheet("")

        # Validate inputs
        is_valid, error = is_valid_name(name)
        if not is_valid:
            self.name_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_quantity(quantity)
        if not is_valid:
            self.quantity_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_name(batch_number)
        if not is_valid:
            self.batch_number_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_date(expiry_date)
        if not is_valid:
            self.expiry_date_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_price(price)
        if not is_valid:
            self.price_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        try:
            quantity_val = int(quantity)
            price_val = float(price)
            self.db.update_drug(self.selected_drug_id, name, quantity_val, batch_number, expiry_date, price_val)
            QMessageBox.information(self, "Success", "Drug updated successfully.")
            self.load_inventory()
            self.main_window.check_low_stock_alerts()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_drug(self):
        if not self.selected_drug_id:
            QMessageBox.warning(self, "Error", "No drug selected.")
            return

        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this drug?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_drug(self.selected_drug_id)
            QMessageBox.information(self, "Success", "Drug deleted successfully.")
            self.load_inventory()
