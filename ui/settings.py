from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QFileDialog
from PyQt6.QtCore import Qt

class SettingsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = self.main_window.db
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Clinic name
        clinic_layout = QHBoxLayout()
        clinic_label = QLabel("Clinic Name:")
        clinic_label.setStyleSheet("font-size: 14px;")
        self.clinic_input = QLineEdit()
        self.clinic_input.setPlaceholderText("Enter clinic name")
        self.clinic_input.setToolTip("Name of the clinic for receipts")
        self.clinic_input.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        clinic_layout.addWidget(clinic_label)
        clinic_layout.addWidget(self.clinic_input)
        main_layout.addLayout(clinic_layout)

        # Logo
        logo_layout = QHBoxLayout()
        logo_label = QLabel("Receipt Logo:")
        logo_label.setStyleSheet("font-size: 14px;")
        self.logo_button = QPushButton("Choose Logo")
        self.logo_button.setToolTip("Select a PNG or JPG logo for receipts")
        self.logo_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 6px 12px;
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
        self.logo_button.clicked.connect(self.choose_logo)
        self.logo_label = QLabel("No logo selected")
        self.logo_label.setStyleSheet("font-size: 12px; color: #555555;")
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(self.logo_button)
        logo_layout.addWidget(self.logo_label)
        main_layout.addLayout(logo_layout)

        # Currency symbol
        currency_layout = QHBoxLayout()
        currency_label = QLabel("Currency Symbol:")
        currency_label.setStyleSheet("font-size: 14px;")
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["KSh", "$", "£", "€", "₹", "¥", "A$"])
        self.currency_combo.setToolTip("Select currency symbol for receipts")
        self.currency_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        currency_layout.addWidget(currency_label)
        currency_layout.addWidget(self.currency_combo)
        main_layout.addLayout(currency_layout)

        # Load saved settings
        config = self.db.load_config()
        self.clinic_input.setText(config["clinic_name"])
        self.logo_label.setText(config["logo_path"] if config["logo_path"] else "No logo selected")
        self.currency_combo.setCurrentText(config["currency_symbol"])

        # Sync toggle
        sync_layout = QHBoxLayout()
        self.sync_toggle = QCheckBox("Enable Cloud Sync")
        self.sync_toggle.setToolTip("Enable automatic syncing to the cloud")
        self.sync_toggle.setChecked(self.db.sync_enabled)
        self.sync_toggle.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
            }
        """)
        sync_layout.addWidget(self.sync_toggle)
        main_layout.addLayout(sync_layout)

        # Sync status
        self.status_label = QLabel(self.get_sync_status())
        self.status_label.setStyleSheet("font-size: 12px; color: #555555;")
        main_layout.addWidget(self.status_label)

        # Sync message
        sync_message = QLabel("Syncing is automatic when enabled, but you can sync manually using the button below.")
        sync_message.setStyleSheet("font-size: 12px; color: #555555; font-style: italic;")
        main_layout.addWidget(sync_message)

        # Sync now button
        sync_now_button = QPushButton("Sync Now")
        sync_now_button.setToolTip("Manually sync data to the cloud")
        sync_now_button.setStyleSheet("""
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
        sync_now_button.clicked.connect(self.manual_sync)
        main_layout.addWidget(sync_now_button)

        # Sync history table
        self.sync_table = QTableWidget()
        self.sync_table.setRowCount(0)
        self.sync_table.setColumnCount(6)
        self.sync_table.setHorizontalHeaderLabels(["Table", "Operation", "Record ID", "Status", "Timestamp", "Details"])
        self.sync_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #cccccc;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #cccccc;
                font-size: 12px;
            }
        """)
        self.sync_table.setAlternatingRowColors(True)
        self.sync_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.sync_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.sync_table.setColumnWidth(0, 100)
        self.sync_table.setColumnWidth(1, 80)
        self.sync_table.setColumnWidth(2, 80)
        self.sync_table.setColumnWidth(3, 80)
        self.sync_table.setColumnWidth(4, 150)
        self.sync_table.setColumnWidth(5, 200)
        self.update_sync_table()
        main_layout.addWidget(self.sync_table)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.setToolTip("Save settings")
        save_button.setStyleSheet("""
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
        save_button.clicked.connect(self.save_settings)
        back_button.clicked.connect(self.main_window.show_menu)
        button_layout.addWidget(save_button)
        button_layout.addWidget(back_button)
        main_layout.addLayout(button_layout)

        main_layout.addStretch()

    def choose_logo(self):
        """Open file dialog to choose a logo image."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Logo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.logo_label.setText(file_path)

    def get_sync_status(self):
        """Get the current sync status."""
        if not self.db.supabase:
            return "Cloud sync unavailable: Supabase not configured."
        if not self.db.sync_enabled:
            return "Cloud sync disabled."
        if not self.db.is_online():
            return "Offline: Changes will sync when online."
        if self.db.last_sync_time:
            return f"Last synced: {self.db.last_sync_time.strftime('%Y-%m-%d %H:%M:%S')}"
        return "Sync enabled, no sync performed yet."

    def manual_sync(self):
        """Manually trigger a sync."""
        if not self.db.is_online():
            QMessageBox.warning(self, "Sync", "No internet connection. Changes will sync when online.")
            return
        if not self.db.supabase:
            QMessageBox.warning(self, "Sync", "Supabase not configured. Check credentials.")
            return
        self.db.sync_data()
        self.status_label.setText(self.get_sync_status())
        self.update_sync_table()
        QMessageBox.information(self, "Sync", "Manual sync completed.")

    def save_settings(self):
        """Save settings and update sync status."""
        # Validate clinic name
        clinic_name = self.clinic_input.text().strip()
        if not clinic_name:
            QMessageBox.warning(self, "Input Error", "Clinic name cannot be empty.")
            return
        if len(clinic_name) > 100:
            QMessageBox.warning(self, "Input Error", "Clinic name must be 100 characters or less.")
            return

        # Validate logo path
        logo_path = self.logo_label.text()
        if logo_path != "No logo selected" and not os.path.exists(logo_path):
            QMessageBox.warning(self, "Input Error", "Selected logo file does not exist.")
            return

        # Save config
        config = {
            "clinic_name": clinic_name,
            "logo_path": logo_path if logo_path != "No logo selected" else "",
            "currency_symbol": self.currency_combo.currentText(),
            "sync_enabled": self.sync_toggle.isChecked()
        }
        self.db.save_config(config)
        self.main_window.config = config

        # Handle sync toggle
        was_enabled = self.db.sync_enabled
        self.db.toggle_sync(self.sync_toggle.isChecked())
        if self.sync_toggle.isChecked() and not was_enabled:
            QMessageBox.information(self, "Sync", "Cloud sync enabled. Data will sync automatically when online.")
        elif not self.sync_toggle.isChecked() and was_enabled:
            QMessageBox.information(self, "Sync", "Cloud sync disabled.")
        
        self.status_label.setText(self.get_sync_status())
        self.update_sync_table()
        QMessageBox.information(self, "Settings", "Settings saved successfully.")

    def update_sync_table(self):
        """Update the sync history table."""
        history = self.db.get_sync_history()
        self.sync_table.setRowCount(len(history))
        for row, item in enumerate(history):
            self.sync_table.setItem(row, 0, QTableWidgetItem(item['table_name']))
            self.sync_table.setItem(row, 1, QTableWidgetItem(item['operation']))
            self.sync_table.setItem(row, 2, QTableWidgetItem(str(item['record_id'])))
            self.sync_table.setItem(row, 3, QTableWidgetItem(item['status']))
            self.sync_table.setItem(row, 4, QTableWidgetItem(str(item['timestamp'])))
            self.sync_table.setItem(row, 5, QTableWidgetItem(item['details']))
            for col in range(6):
                self.sync_table.item(row, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
