from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
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
        self.sync_table.setColumnWidth(0, 100)  # Table
        self.sync_table.setColumnWidth(1, 80)   # Operation
        self.sync_table.setColumnWidth(2, 80)   # Record ID
        self.sync_table.setColumnWidth(3, 80)   # Status
        self.sync_table.setColumnWidth(4, 150)  # Timestamp
        self.sync_table.setColumnWidth(5, 200)  # Details
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
        was_enabled = self.db.sync_enabled
        self.db.toggle_sync(self.sync_toggle.isChecked())
        if self.sync_toggle.isChecked() and not was_enabled:
            QMessageBox.information(self, "Sync", "Cloud sync enabled. Data will sync automatically when online.")
        elif not self.sync_toggle.isChecked() and was_enabled:
            QMessageBox.information(self, "Sync", "Cloud sync disabled.")
        self.status_label.setText(self.get_sync_status())
        self.update_sync_table()

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
