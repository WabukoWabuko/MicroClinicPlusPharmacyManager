import sqlite3  # Added import for sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QFileDialog, QScrollArea
from PyQt6.QtCore import Qt
import os
import shutil
import json

class SettingsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = self.main_window.db
        self.init_ui()

    def init_ui(self):
        # Main layout for the entire widget
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create a scroll area to make content expandable
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        main_layout.addWidget(scroll)

        # Widget to hold all content inside the scroll area
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Title
        self.set_title("Settings")
        title = QLabel("Settings")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF; margin: 20px;")
        scroll_layout.addWidget(title)

        # Check if user is admin
        is_admin = self.main_window.current_user and self.main_window.current_user.get('role') == 'admin'

        # Clinic name (admin only)
        if is_admin:
            clinic_layout = QHBoxLayout()
            clinic_label = QLabel("Clinic Name:")
            clinic_label.setStyleSheet("font-size: 14px; color: #FFFFFF; padding: 5px;")
            self.clinic_input = QLineEdit()
            self.clinic_input.setPlaceholderText("Enter clinic name")
            self.clinic_input.setToolTip("Name of the clinic for receipts")
            self.clinic_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #4CAF50;
                    border-radius: 5px;
                    font-size: 14px;
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                    min-width: 300px;
                }
            """)
            clinic_layout.addWidget(clinic_label)
            clinic_layout.addWidget(self.clinic_input)
            clinic_layout.addStretch()
            scroll_layout.addLayout(clinic_layout)

        # Image selection (admin only) - Logo and Background side by side
        if is_admin:
            image_layout = QHBoxLayout()
            
            # Logo selection
            logo_inner_layout = QHBoxLayout()
            logo_label = QLabel("Receipt Logo:")
            logo_label.setStyleSheet("font-size: 14px; color: #FFFFFF; padding: 5px;")
            self.logo_button = QPushButton("Choose Logo")
            self.logo_button.setToolTip("Select a logo for receipts (PNG, JPG, JPEG)")
            self.logo_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: #FFFFFF;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 5px;
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
            self.logo_label.setStyleSheet("font-size: 12px; color: #FFFFFF; padding: 5px;")
            logo_inner_layout.addWidget(logo_label)
            logo_inner_layout.addWidget(self.logo_button)
            logo_inner_layout.addWidget(self.logo_label)
            
            # Background Image selection
            bg_inner_layout = QHBoxLayout()
            bg_label = QLabel("Background Image:")
            bg_label.setStyleSheet("font-size: 14px; color: #FFFFFF; padding: 5px;")
            self.bg_button = QPushButton("Choose Background")
            self.bg_button.setToolTip("Select a background image for receipts (PNG, JPG, JPEG)")
            self.bg_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: #FFFFFF;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
            self.bg_button.clicked.connect(self.choose_background)
            self.bg_label = QLabel("No background selected")
            self.bg_label.setStyleSheet("font-size: 12px; color: #FFFFFF; padding: 5px;")
            bg_inner_layout.addWidget(bg_label)
            bg_inner_layout.addWidget(self.bg_button)
            bg_inner_layout.addWidget(self.bg_label)
            
            image_layout.addLayout(logo_inner_layout)
            image_layout.addStretch()
            image_layout.addLayout(bg_inner_layout)
            scroll_layout.addLayout(image_layout)

        # Tax Rate and Contact Details (admin only) - side by side
        if is_admin:
            tax_contact_layout = QHBoxLayout()
            
            # Tax Rate
            tax_inner_layout = QHBoxLayout()
            tax_label = QLabel("Tax Rate (%):")
            tax_label.setStyleSheet("font-size: 14px; color: #FFFFFF; padding: 5px;")
            self.tax_input = QLineEdit()
            self.tax_input.setPlaceholderText("Enter tax rate (e.g., 16)")
            self.tax_input.setToolTip("Tax rate for sales")
            self.tax_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #4CAF50;
                    border-radius: 5px;
                    font-size: 14px;
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                    min-width: 100px;
                }
            """)
            tax_inner_layout.addWidget(tax_label)
            tax_inner_layout.addWidget(self.tax_input)
            
            # Contact Details
            contact_inner_layout = QHBoxLayout()
            contact_label = QLabel("Contact Details:")
            contact_label.setStyleSheet("font-size: 14px; color: #FFFFFF; padding: 5px;")
            self.contact_input = QLineEdit()
            self.contact_input.setPlaceholderText("Enter contact (e.g., +254712345678)")
            self.contact_input.setToolTip("Contact for clinic")
            self.contact_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #4CAF50;
                    border-radius: 5px;
                    font-size: 14px;
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                    min-width: 200px;
                }
            """)
            contact_inner_layout.addWidget(contact_label)
            contact_inner_layout.addWidget(self.contact_input)
            
            tax_contact_layout.addLayout(tax_inner_layout)
            tax_contact_layout.addStretch()
            tax_contact_layout.addLayout(contact_inner_layout)
            scroll_layout.addLayout(tax_contact_layout)

        # Sync toggle (staff and admin)
        sync_layout = QHBoxLayout()
        self.sync_toggle = QCheckBox("Enable Cloud Sync")
        self.sync_toggle.setToolTip("Enable automatic syncing to the cloud")
        self.sync_toggle.setChecked(self.db.sync_enabled)
        self.sync_toggle.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #FFFFFF;
                padding: 5px;
            }
        """)
        sync_layout.addWidget(self.sync_toggle)
        sync_layout.addStretch()
        scroll_layout.addLayout(sync_layout)

        # Sync status
        self.status_label = QLabel(self.get_sync_status())
        self.status_label.setStyleSheet("font-size: 12px; color: #FFFFFF; padding: 5px;")
        scroll_layout.addWidget(self.status_label)

        # Sync message
        sync_message = QLabel("Syncing is automatic when enabled, but you can sync manually using the button below.")
        sync_message.setStyleSheet("font-size: 12px; color: #FFFFFF; font-style: italic; padding: 5px;")
        scroll_layout.addWidget(sync_message)

        # Action buttons (Sync Now, Import, Export, Save, Back) - side by side
        action_buttons_layout = QHBoxLayout()
        
        # Sync Now button
        sync_now_button = QPushButton("Sync Now")
        sync_now_button.setToolTip("Manually sync data to the cloud")
        sync_now_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        sync_now_button.clicked.connect(self.manual_sync)
        action_buttons_layout.addWidget(sync_now_button)

        # Import Data (admin only)
        if is_admin:
            import_button = QPushButton("Import Data")
            import_button.setToolTip("Import data from a backup file")
            import_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: #FFFFFF;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
                QPushButton:pressed {
                    background-color: #EF6C00;
                }
            """)
            import_button.clicked.connect(self.import_data)
            action_buttons_layout.addWidget(import_button)

        # Export Data (admin only)
        if is_admin:
            export_button = QPushButton("Export Data")
            export_button.setToolTip("Export data to a backup file")
            export_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: #FFFFFF;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
                QPushButton:pressed {
                    background-color: #EF6C00;
                }
            """)
            export_button.clicked.connect(self.export_data)
            action_buttons_layout.addWidget(export_button)

        # Save button
        save_button = QPushButton("Save")
        save_button.setToolTip("Save settings")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        save_button.clicked.connect(self.save_settings)
        action_buttons_layout.addWidget(save_button)

        # Back button
        back_button = QPushButton("Back")
        back_button.setToolTip("Return to menu")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        back_button.clicked.connect(self.main_window.show_menu)
        action_buttons_layout.addWidget(back_button)

        action_buttons_layout.addStretch()
        scroll_layout.addLayout(action_buttons_layout)

        # Sync history table - stretch to fill available space
        self.sync_table = QTableWidget()
        self.sync_table.setRowCount(0)
        self.sync_table.setColumnCount(6)
        self.sync_table.setHorizontalHeaderLabels(["Table", "Operation", "Record ID", "Status", "Timestamp", "Details"])
        self.sync_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #4CAF50;
                font-size: 12px;
                background-color: #2E2E2E;
                color: #FFFFFF;
                margin: 10px 0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #000000;
                color: #FFFFFF;
                padding: 8px;
                border: 1px solid #4CAF50;
                font-size: 12px;
            }
        """)
        self.sync_table.setAlternatingRowColors(True)
        self.sync_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.sync_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.sync_table.setColumnWidth(0, 120)
        self.sync_table.setColumnWidth(1, 100)
        self.sync_table.setColumnWidth(2, 100)
        self.sync_table.setColumnWidth(3, 100)
        self.sync_table.setColumnWidth(4, 180)
        self.sync_table.setColumnWidth(5, 250)
        self.sync_table.verticalHeader().setDefaultSectionSize(30)
        self.sync_table.setMinimumHeight(300)  # Ensure table has enough space
        self.update_sync_table()
        scroll_layout.addWidget(self.sync_table)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)

        # Load saved settings
        config = self.db.load_config()
        if is_admin:
            self.clinic_input.setText(config["clinic_name"])
            self.logo_label.setText(config.get("logo_path", "") if config.get("logo_path", "") else "No logo selected")
            self.bg_label.setText(config.get("background_path", "") if config.get("background_path", "") else "No background selected")
            self.tax_input.setText(str(config.get("tax_rate", 0)))
            self.contact_input.setText(config.get("contact_details", ""))
        self.sync_toggle.setChecked(config["sync_enabled"])

    def set_title(self, title):
        self.main_window.set_title(title)

    def choose_logo(self):
        """Open file dialog to choose a logo image."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Logo", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp)")
        if file_path:
            self.logo_label.setText(file_path)

    def choose_background(self):
        """Open file dialog to choose a background image."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Background", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp)")
        if file_path:
            self.bg_label.setText(file_path)

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
        try:
            self.db.sync_data()
            self.status_label.setText(self.get_sync_status())
            self.update_sync_table()
            QMessageBox.information(self, "Sync", "Manual sync completed successfully at 12:57 PM EAT on Wednesday, May 14, 2025.")
        except sqlite3.IntegrityError as e:
            self.status_label.setText(f"Sync failed: {str(e)}")
            self.update_sync_table()
            retry = QMessageBox.warning(self, "Sync Error", f"Sync failed due to data integrity issue: {str(e)}\nWould you like to retry?",
                                      QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel)
            if retry == QMessageBox.StandardButton.Retry:
                self.manual_sync()
        except Exception as e:
            self.status_label.setText(f"Sync failed: {str(e)}")
            self.update_sync_table()
            QMessageBox.critical(self, "Sync Error", f"An error occurred during sync: {str(e)}")

    def save_settings(self):
        """Save settings and update sync status."""
        is_admin = self.main_window.current_user and self.main_window.current_user.get('role') == 'admin'
        if not is_admin and not self.sync_toggle.isChecked() == self.db.sync_enabled:
            QMessageBox.warning(self, "Access Denied", "Only admin can modify settings except sync toggle.")
            return

        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            QMessageBox.warning(self, "Error", "Demo period expired. Please activate the system.")
            return

        config = self.db.load_config()
        if is_admin:
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

            # Validate background path
            bg_path = self.bg_label.text()
            if bg_path != "No background selected" and not os.path.exists(bg_path):
                QMessageBox.warning(self, "Input Error", "Selected background file does not exist.")
                return

            # Validate tax rate
            tax_rate = self.tax_input.text().strip()
            if tax_rate and (not tax_rate.isdigit() or int(tax_rate) < 0 or int(tax_rate) > 100):
                QMessageBox.warning(self, "Input Error", "Tax rate must be a number between 0 and 100.")
                return

            # Validate contact
            contact = self.contact_input.text().strip()
            if contact and len(contact) > 20:
                QMessageBox.warning(self, "Input Error", "Contact must be 20 characters or less.")

            # Update config with admin settings
            config.update({
                "clinic_name": clinic_name,
                "logo_path": logo_path if logo_path != "No logo selected" else "",
                "background_path": bg_path if bg_path != "No background selected" else "",
                "tax_rate": int(tax_rate) if tax_rate else 0,
                "contact_details": contact if contact else ""
            })

        # Update sync toggle (staff and admin)
        config["sync_enabled"] = self.sync_toggle.isChecked()
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
        QMessageBox.information(self, "Settings", "Settings saved successfully at 12:57 PM EAT on Wednesday, May 14, 2025.")

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

    def import_data(self):
        """Import data from a backup file."""
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            QMessageBox.warning(self, "Error", "Demo period expired. Please activate the system.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Import Data", "", "Database Files (*.db)")
        if file_path and os.path.exists(file_path):
            try:
                db_path = self.db.db_path
                shutil.copy2(file_path, db_path)
                QMessageBox.information(self, "Import", "Data imported successfully. Restart application to apply changes at 12:57 PM EAT on Wednesday, May 14, 2025.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import data: {str(e)}")
        else:
            QMessageBox.warning(self, "Import", "No valid file selected.")

    def export_data(self):
        """Export data to a backup file."""
        if not self.main_window.db.is_system_activated() and not self.main_window.db.is_demo_period_active():
            QMessageBox.warning(self, "Error", "Demo period expired. Please activate the system.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Export Data", f"backup_{self.db.get_current_date()}.db", "Database Files (*.db)")
        if file_path:
            try:
                db_path = self.db.db_path
                shutil.copy2(db_path, file_path)
                QMessageBox.information(self, "Export", "Data exported successfully at 12:57 PM EAT on Wednesday, May 14, 2025.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export data: {str(e)}")
