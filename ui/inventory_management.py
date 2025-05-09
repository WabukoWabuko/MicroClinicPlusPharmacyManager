from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
                             QLineEdit, QDateEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QDate
from db.database import Database

class InventoryManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.selected_drug_id = None
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Form layout for drug details
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.batch_number_input = QLineEdit()
        self.expiry_date_input = QDateEdit()
        self.expiry_date_input.setCalendarPopup(True)
        self.expiry_date_input.setDate(QDate.currentDate())
        self.price_input = QLineEdit()

        form_layout.addRow("Drug Name:", self.name_input)
        form_layout.addRow("Quantity:", self.quantity_input)
        form_layout.addRow("Batch Number:", self.batch_number_input)
        form_layout.addRow("Expiry Date:", self.expiry_date_input)
        form_layout.addRow("Price (KES):", self.price_input)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        update_button = QPushButton("Update")
        clear_button = QPushButton("Clear")
        back_button = QPushButton("Back")
        add_button.clicked.connect(self.add_drug)
        update_button.clicked.connect(self.update_drug)
        clear_button.clicked.connect(self.clear_form)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(back_button)

        # Table for viewing inventory
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Quantity", "Batch Number", "Expiry Date", "Price", "Delete"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.cellClicked.connect(self.select_drug)

        # Add to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        # Populate table
        self.populate_table()

    def populate_table(self):
        """Populate the inventory table with drugs."""
        drugs = self.db.get_all_drugs()
        expiring_drugs = set(drug['drug_id'] for drug in self.db.get_expiring_drugs())
        self.table.setRowCount(len(drugs))

        for row, drug in enumerate(drugs):
            self.table.setItem(row, 0, QTableWidgetItem(str(drug['drug_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(drug['name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(drug['quantity'])))
            self.table.setItem(row, 3, QTableWidgetItem(drug['batch_number']))
            self.table.setItem(row, 4, QTableWidgetItem(drug['expiry_date']))
            self.table.setItem(row, 5, QTableWidgetItem(f"{drug['price']:.2f}"))
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, d=drug['drug_id']: self.delete_drug(d))
            self.table.setCellWidget(row, 6, delete_button)

            # Highlight expiring drugs in red
            if drug['drug_id'] in expiring_drugs:
                for col in range(6):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QColor(255, 0, 0))

    def add_drug(self):
        """Add a new drug to the inventory."""
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        batch_number = self.batch_number_input.text().strip()
        expiry_date = self.expiry_date_input.date().toString("yyyy-MM-dd")
        price = self.price_input.text().strip()

        # Validate inputs
        if not (name and quantity and batch_number and expiry_date and price):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity must be a positive integer, and Price must be a non-negative number.")
            return

        # Save to database
        self.db.add_drug(name, quantity, batch_number, expiry_date, price)
        QMessageBox.information(self, "Success", "Drug added successfully.")
        self.clear_form()
        self.populate_table()

    def select_drug(self, row, column):
        """Populate form with selected drug's details for editing."""
        if column == 6:  # Ignore delete button clicks
            return
        self.selected_drug_id = int(self.table.item(row, 0).text())
        drug = next(d for d in self.db.get_all_drugs() if d['drug_id'] == self.selected_drug_id)
        self.name_input.setText(drug['name'])
        self.quantity_input.setText(str(drug['quantity']))
        self.batch_number_input.setText(drug['batch_number'])
        expiry_date = QDate.fromString(drug['expiry_date'], "yyyy-MM-dd")
        self.expiry_date_input.setDate(expiry_date)
        self.price_input.setText(str(drug['price']))

    def update_drug(self):
        """Update the selected drug in the inventory."""
        if not self.selected_drug_id:
            QMessageBox.warning(self, "Selection Error", "Please select a drug to update.")
            return

        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        batch_number = self.batch_number_input.text().strip()
        expiry_date = self.expiry_date_input.date().toString("yyyy-MM-dd")
        price = self.price_input.text().strip()

        # Validate inputs
        if not (name and quantity and batch_number and expiry_date and price):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity must be a positive integer, and Price must be a non-negative number.")
            return

        # Update in database
        self.db.update_drug(self.selected_drug_id, name, quantity, batch_number, expiry_date, price)
        QMessageBox.information(self, "Success", "Drug updated successfully.")
        self.clear_form()
        self.populate_table()

    def delete_drug(self, drug_id):
        """Delete the selected drug from the inventory."""
        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this drug?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_drug(drug_id)
            QMessageBox.information(self, "Success", "Drug deleted successfully.")
            self.clear_form()
            self.populate_table()

    def clear_form(self):
        """Clear all input fields and reset selected drug."""
        self.name_input.clear()
        self.quantity_input.clear()
        self.batch_number_input.clear()
        self.expiry_date_input.setDate(QDate.currentDate())
        self.price_input.clear()
        self.selected_drug_id = None
