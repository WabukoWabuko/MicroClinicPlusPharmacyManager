import sqlite3
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QLineEdit, QPushButton,
                             QTabWidget)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from db.database import Database

class ReportingDashboardWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Summary metrics
        summary_layout = QHBoxLayout()
        self.sales_summary_label = QLabel("Sales: 0 sales, KES 0.00")
        self.prescription_summary_label = QLabel("Prescriptions: 0")
        summary_layout.addWidget(self.sales_summary_label)
        summary_layout.addWidget(self.prescription_summary_label)
        main_layout.addLayout(summary_layout)

        # Tabs for different reports
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Sales table tab
        self.sales_tab = QWidget()
        sales_layout = QVBoxLayout()
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(4)
        self.sales_table.setHorizontalHeaderLabels(["Sale ID", "Date", "Patient", "Total Price"])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sales_table.setSortingEnabled(True)
        sales_filter_layout = QHBoxLayout()
        self.sales_filter = QLineEdit()
        self.sales_filter.setPlaceholderText("Filter by patient name...")
        self.sales_filter.textChanged.connect(self.filter_sales)
        sales_filter_layout.addWidget(self.sales_filter)
        sales_layout.addLayout(sales_filter_layout)
        sales_layout.addWidget(self.sales_table)
        self.sales_tab.setLayout(sales_layout)
        self.tabs.addTab(self.sales_tab, "Sales")

        # Prescriptions table tab
        self.prescriptions_tab = QWidget()
        prescriptions_layout = QVBoxLayout()
        self.prescriptions_table = QTableWidget()
        self.prescriptions_table.setColumnCount(4)
        self.prescriptions_table.setHorizontalHeaderLabels(["Username", "Prescription Count", "Last Prescription", "Total Quantity"])
        self.prescriptions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.prescriptions_table.setSortingEnabled(True)
        prescriptions_layout.addWidget(self.prescriptions_table)
        self.prescriptions_tab.setLayout(prescriptions_layout)
        self.tabs.addTab(self.prescriptions_tab, "Prescriptions by User")

        # Low stock table tab
        self.low_stock_tab = QWidget()
        low_stock_layout = QVBoxLayout()
        self.low_stock_table = QTableWidget()
        self.low_stock_table.setColumnCount(5)
        self.low_stock_table.setHorizontalHeaderLabels(["Drug ID", "Name", "Quantity", "Batch Number", "Expiry Date"])
        self.low_stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.low_stock_table.setSortingEnabled(True)
        low_stock_layout.addWidget(self.low_stock_table)
        self.low_stock_tab.setLayout(low_stock_layout)
        self.tabs.addTab(self.low_stock_tab, "Low Stock Drugs")

        # Sales chart
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.main_window.show_menu)
        main_layout.addWidget(back_button)

        # Load data
        self.load_summary()
        self.load_sales()
        self.load_prescriptions()
        self.load_low_stock()
        self.load_sales_chart()

    def load_summary(self):
        """Load summary metrics."""
        sales_summary = self.db.get_sales_summary()
        self.sales_summary_label.setText(
            f"Sales: {sales_summary['sale_count']} sales, KES {sales_summary['total_value'] or 0:.2f}"
        )
        prescriptions = self.db.get_prescriptions_by_user()
        total_prescriptions = sum(p['prescription_count'] for p in prescriptions)
        self.prescription_summary_label.setText(f"Prescriptions: {total_prescriptions}")

    def load_sales(self):
        """Load all sales into the sales table."""
        with sqlite3.connect(self.db.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.sale_id, s.sale_date, p.first_name, p.last_name, s.total_price
                FROM sales s
                JOIN patients p ON s.patient_id = p.patient_id
            """)
            sales = cursor.fetchall()

        self.sales_table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            self.sales_table.setItem(row, 0, QTableWidgetItem(str(sale['sale_id'])))
            self.sales_table.setItem(row, 1, QTableWidgetItem(sale['sale_date']))
            self.sales_table.setItem(row, 2, QTableWidgetItem(f"{sale['first_name']} {sale['last_name']}"))
            self.sales_table.setItem(row, 3, QTableWidgetItem(f"{sale['total_price']:.2f}"))

    def filter_sales(self):
        """Filter sales table by patient name."""
        filter_text = self.sales_filter.text().strip().lower()
        with sqlite3.connect(self.db.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.sale_id, s.sale_date, p.first_name, p.last_name, s.total_price
                FROM sales s
                JOIN patients p ON s.patient_id = p.patient_id
                WHERE p.first_name LIKE ? OR p.last_name LIKE ?
            """, (f"%{filter_text}%", f"%{filter_text}%"))
            sales = cursor.fetchall()

        self.sales_table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            self.sales_table.setItem(row, 0, QTableWidgetItem(str(sale['sale_id'])))
            self.sales_table.setItem(row, 1, QTableWidgetItem(sale['sale_date']))
            self.sales_table.setItem(row, 2, QTableWidgetItem(f"{sale['first_name']} {sale['last_name']}"))
            self.sales_table.setItem(row, 3, QTableWidgetItem(f"{sale['total_price']:.2f}"))

    def load_prescriptions(self):
        """Load prescriptions by user into the prescriptions table."""
        prescriptions = self.db.get_prescriptions_by_user()
        with sqlite3.connect(self.db.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.username, MAX(p.prescription_date) as last_prescription,
                       SUM(pi.quantity_prescribed) as total_quantity
                FROM prescriptions p
                JOIN users u ON p.user_id = u.user_id
                JOIN prescription_items pi ON p.prescription_id = pi.prescription_id
                GROUP BY u.username
            """)
            additional_data = {row['username']: row for row in cursor.fetchall()}

        self.prescriptions_table.setRowCount(len(prescriptions))
        for row, prescription in enumerate(prescriptions):
            username = prescription['username']
            self.prescriptions_table.setItem(row, 0, QTableWidgetItem(username))
            self.prescriptions_table.setItem(row, 1, QTableWidgetItem(str(prescription['prescription_count'])))
            last_prescription = additional_data.get(username, {}).get('last_prescription', '')
            total_quantity = additional_data.get(username, {}).get('total_quantity', 0)
            self.prescriptions_table.setItem(row, 2, QTableWidgetItem(last_prescription))
            self.prescriptions_table.setItem(row, 3, QTableWidgetItem(str(total_quantity)))

    def load_low_stock(self):
        """Load low stock drugs into the low stock table."""
        drugs = self.db.get_low_stock_drugs()
        self.low_stock_table.setRowCount(len(drugs))
        for row, drug in enumerate(drugs):
            self.low_stock_table.setItem(row, 0, QTableWidgetItem(str(drug['drug_id'])))
            self.low_stock_table.setItem(row, 1, QTableWidgetItem(drug['name']))
            self.low_stock_table.setItem(row, 2, QTableWidgetItem(str(drug['quantity'])))
            self.low_stock_table.setItem(row, 3, QTableWidgetItem(drug['batch_number']))
            self.low_stock_table.setItem(row, 4, QTableWidgetItem(drug['expiry_date']))

    def load_sales_chart(self):
        """Load sales chart for the last 30 days."""
        sales_data = self.db.get_sales_for_chart()
        dates = [row['sale_date'] for row in sales_data]
        totals = [row['daily_total'] for row in sales_data]

        self.ax.clear()
        self.ax.plot(dates, totals, marker='o')
        self.ax.set_title("Daily Sales (Last 30 Days)")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Total Sales (KES)")
        self.ax.grid(True)
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha="right")
        self.canvas.draw()
