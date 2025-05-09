from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QLineEdit, QComboBox,
                             QPushButton, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database

class UserManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(["User ID", "Username", "Role"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.users_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.users_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.users_table.selectionModel().selectionChanged.connect(self.load_selected_user)
        main_layout.addWidget(self.users_table)

        # Form for adding/editing users
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "staff"])
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Role:", self.role_input)
        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add User")
        self.update_button = QPushButton("Update User")
        self.delete_button = QPushButton("Delete User")
        self.back_button = QPushButton("Back")
        self.add_button.clicked.connect(self.add_user)
        self.update_button.clicked.connect(self.update_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.back_button)
        main_layout.addLayout(button_layout)

        # Selected user ID
        self.selected_user_id = None

        # Load users
        self.load_users()

    def load_users(self):
        """Load all users into the table."""
        users = self.db.get_all_users()
        self.users_table.setRowCount(len(users))
        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(str(user['user_id'])))
            self.users_table.setItem(row, 1, QTableWidgetItem(user['username']))
            self.users_table.setItem(row, 2, QTableWidgetItem(user['role']))
        self.clear_form()

    def load_selected_user(self):
        """Load selected user's details into the form."""
        selected = self.users_table.selectedItems()
        if selected:
            row = selected[0].row()
            self.selected_user_id = int(self.users_table.item(row, 0).text())
            self.username_input.setText(self.users_table.item(row, 1).text())
            self.role_input.setCurrentText(self.users_table.item(row, 2).text())
            self.password_input.clear()

    def clear_form(self):
        """Clear the form inputs."""
        self.selected_user_id = None
        self.username_input.clear()
        self.password_input.clear()
        self.role_input.setCurrentIndex(0)
        self.users_table.clearSelection()

    def add_user(self):
        """Add a new user."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required.")
            return

        try:
            self.db.add_user(username, password, role)
            QMessageBox.information(self, "Success", "User added successfully.")
            self.load_users()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def update_user(self):
        """Update the selected user."""
        if not self.selected_user_id:
            QMessageBox.warning(self, "Error", "No user selected.")
            return

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.currentText()

        if not username:
            QMessageBox.warning(self, "Error", "Username is required.")
            return

        try:
            self.db.update_user(self.selected_user_id, username, password, role)
            QMessageBox.information(self, "Success", "User updated successfully.")
            self.load_users()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_user(self):
        """Delete the selected user."""
        if not self.selected_user_id:
            QMessageBox.warning(self, "Error", "No user selected.")
            return

        if self.selected_user_id == self.main_window.current_user['user_id']:
            QMessageBox.warning(self, "Error", "Cannot delete the currently logged-in user.")
            return

        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this user?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_user(self.selected_user_id)
            QMessageBox.information(self, "Success", "User deleted successfully.")
            self.load_users()
