from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from db.database import Database
import bcrypt
import sqlite3

class UserManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Form for managing users
        form_layout = QHBoxLayout()
        left_form = QVBoxLayout()
        right_form = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setToolTip("Enter user username")
        self.username_input.setStyleSheet("""
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
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setToolTip("Enter user password")
        self.password_input.setStyleSheet("""
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
        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "staff"])
        self.role_combo.setToolTip("Select user role")
        self.role_combo.setStyleSheet("""
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
        add_button.setToolTip("Add new user")
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
        update_button = QPushButton("Update User")
        update_button.setToolTip("Update selected user")
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
        delete_button = QPushButton("Delete User")
        delete_button.setToolTip("Delete selected user")
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
        self.user_table.setToolTip("List of users")
        self.user_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.user_table.clicked.connect(self.load_user_to_form)
        main_layout.addWidget(self.user_table)

        main_layout.addStretch()

        self.load_users()

    def load_users(self):
        users = self.db.get_all_users()
        self.user_table.setRowCount(len(users))
        for row, user in enumerate(users):
            self.user_table.setItem(row, 0, QTableWidgetItem(str(user['user_id'])))
            self.user_table.setItem(row, 1, QTableWidgetItem(user['username']))
            self.user_table.setItem(row, 2, QTableWidgetItem(user['role']))

    def load_user_to_form(self):
        row = self.user_table.currentRow()
        if row >= 0:
            self.username_input.setText(self.user_table.item(row, 1).text())
            self.password_input.clear()
            self.role_combo.setCurrentText(self.user_table.item(row, 2).text())

    def add_user(self):
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            QMessageBox.warning(self, "Error", "Demo period expired. Please activate the system.")
            return

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()

        if not username:
            QMessageBox.warning(self, "Error", "Username is required.")
            return
        if not password:
            QMessageBox.warning(self, "Error", "Password is required.")
            return

        try:
            # Hash the password using bcrypt
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            self.db.add_user(username, password_hash.decode('utf-8'), role)
            QMessageBox.information(self, "Success", "User added successfully at 12:52 PM EAT on Wednesday, May 14, 2025.")
            self.load_users()
            self.clear_form()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists.")

    def update_user(self):
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            QMessageBox.warning(self, "Error", "Demo period expired. Please activate the system.")
            return

        row = self.user_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a user to update.")
            return

        user_id = int(self.user_table.item(row, 0).text())
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()

        if not username:
            QMessageBox.warning(self, "Error", "Username is required.")
            return

        try:
            # Hash the password if provided, otherwise keep the existing hash
            if password:
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            else:
                existing_user = self.db.get_user_by_id(user_id)
                password_hash = existing_user['password_hash']
            self.db.update_user(user_id, username, password_hash, role)
            QMessageBox.information(self, "Success", "User updated successfully at 12:52 PM EAT on Wednesday, May 14, 2025.")
            self.load_users()
            self.clear_form()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists.")

    def delete_user(self):
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            QMessageBox.warning(self, "Error", "Demo period expired. Please activate the system.")
            return

        row = self.user_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a user to delete.")
            return

        user_id = int(self.user_table.item(row, 0).text())
        if user_id == self.main_window.current_user['user_id']:
            QMessageBox.warning(self, "Error", "Cannot delete the current user.")
            return

        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this user?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_user(user_id)
            QMessageBox.information(self, "Success", "User deleted successfully at 12:52 PM EAT on Wednesday, May 14, 2025.")
            self.load_users()
            self.clear_form()

    def clear_form(self):
        self.username_input.clear()
        self.password_input.clear()
        self.role_combo.setCurrentIndex(0)
