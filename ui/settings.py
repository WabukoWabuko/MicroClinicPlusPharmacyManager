from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton, QMessageBox
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
        self.sync_toggle.setToolTip("Enable syncing data to the cloud")
        self.sync_toggle.setChecked(self.db.sync_enabled)
        self.sync_toggle.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
            }
        """)
        sync_layout.addWidget(self.sync_toggle)
        main_layout.addLayout(sync_layout)

        # Sync status
        status_label = QLabel(self.get_sync_status())
        status_label.setStyleSheet("font-size: 12px; color: #555555;")
        main_layout.addWidget(status_label)

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

    def save_settings(self):
        """Save settings and update sync status."""
        was_enabled = self.db.sync_enabled
        self.db.toggle_sync(self.sync_toggle.isChecked())
        if self.sync_toggle.isChecked() and not was_enabled:
            QMessageBox.information(self, "Sync", "Cloud sync enabled. Data will sync when online.")
        elif not self.sync_toggle.isChecked() and was_enabled:
            QMessageBox.information(self, "Sync", "Cloud sync disabled.")
        # Update status label
        status_label = self.findChild(QLabel)
        if status_label:
            status_label.setText(self.get_sync_status())
