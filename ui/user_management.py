from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox)
from db.database import Database
from utils.validation import is_valid_username, is_valid_password

class UserManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.selected_user_id = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # User form
        form_layout = QHBoxLayout()
        left_form = QVBoxLayout()
        right_form = QVBoxLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "staff"])

        left_form.addWidget(QLabel("Username:"))
        left_form.addWidget(self.username_input)
        right_form.addWidget(QLabel("Password:"))
        right_form.addWidget(self.password_input)
        right_form.addWidget(QLabel("Role:"))
        right_form.addWidget(self.role_combo)

        form_layout.addLayout(left_form)
        form_layout.addLayout(right_form)
        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add User")
        update_button = QPushButton("Update User")
        delete_button = QPushButton("Delete User")
        back_button = QPushButton("Back")
        add_button.clicked.connect(self.add_user)
        update_button.clicked.connect(self.update_user)
        delete_button.clicked.connect(self.delete_user)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

        # User table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Role"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.user_table.selectionModel().selectionChanged.connect(self.load_selected_user)
        main_layout.addWidget(self.user_table)

        self.load_users()

    def load_users(self):
        users = self.db.get_all_users()
        self.user_table.setRowCount(len(users))
        for row, user in enumerate(users):
            self.user_table.setItem(row, 0, QTableWidgetItem(str(user['user_id'])))
            self.user_table.setItem(row, 1, QTableWidgetItem(user['username']))
            self.user_table.setItem(row, 2, QTableWidgetItem(user['role']))

    def load_selected_user(self):
        selected = self.user_table.selectedItems()
        if selected:
            row = selected[0].row()
            self.selected_user_id = int(self.user_table.item(row, 0).text())
            self.username_input.setText(self.user_table.item(row, 1).text())
            self.role_combo.setCurrentText(self.user_table.item(row, 2).text())
            self.password_input.clear()

    def add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()

        # Reset styles
        self.username_input.setStyleSheet("")
        self.password_input.setStyleSheet("")

        # Validate inputs
        is_valid, error = is_valid_username(username)
        if not is_valid:
            self.username_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        is_valid, error = is_valid_password(password)
        if not is_valid:
            self.password_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        try:
            self.db.add_user(username, password, role)
            QMessageBox.information(self, "Success", "User added successfully.")
            self.load_users()
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def update_user(self):
        if not self.selected_user_id:
            QMessageBox.warning(self, "Error", "No user selected.")
            return

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()

        # Reset styles
        self.username_input.setStyleSheet("")
        self.password_input.setStyleSheet("")

        # Validate inputs
        is_valid, error = is_valid_username(username)
        if not is_valid:
            self.username_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Error", error)
            return

        if password:  # Password is optional for update
            is_valid, error = is_valid_password(password)
            if not is_valid:
                self.password_input.setStyleSheet("border: 1px solid red;")
                QMessageBox.warning(self, "Error", error)
                return

        try:
            self.db.update_user(self.selected_user_id, username, password, role)
            QMessageBox.information(self, "Success", "User updated successfully.")
            self.load_users()
            self.clear_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_user(self):
        if not self.selected_user_id:
            QMessageBox.warning(self, "Error", "No user selected.")
            return

        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this user?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_user(self.selected_user_id)
            QMessageBox.information(self, "Success", "User deleted successfully.")
            self.load_users()
            self.clear_form()

    def clear_form(self):
        self.selected_user_id = None
        self.username_input.clear()
        self.password_input.clear()
        self.role_combo.setCurrentIndex(0)
        self.user_table.clearSelection()
        self.username_input.setStyleSheet("")
        self.password_input.setStyleSheet("")
