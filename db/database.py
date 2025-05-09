import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import bcrypt

class Database:
    def __init__(self):
        self.db_path = Path("database/clinic.db")
        self.init_db()

    def init_db(self):
        """Initialize the database by creating tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if not cursor.fetchone():
                schema_path = Path("database/schema.sql")
                with open(schema_path, "r") as f:
                    cursor.executescript(f.read())
                conn.commit()

    def add_user(self, username, password, role):
        """Add a user with a hashed password to the users table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            try:
                cursor.execute("""
                    INSERT INTO users (username, password_hash, role)
                    VALUES (?, ?, ?)
                """, (username, password_hash.decode('utf-8'), role))
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError(f"Username {username} already exists")

    def update_user(self, user_id, username, password, role):
        """Update a user's details in the users table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                if password:
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    cursor.execute("""
                        UPDATE users
                        SET username = ?, password_hash = ?, role = ?
                        WHERE user_id = ?
                    """, (username, password_hash, role, user_id))
                else:
                    cursor.execute("""
                        UPDATE users
                        SET username = ?, role = ?
                        WHERE user_id = ?
                    """, (username, role, user_id))
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError(f"Username {username} already exists")

    def delete_user(self, user_id):
        """Delete a user from the users table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()

    def get_all_users(self):
        """Retrieve all users from the users table."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, role FROM users")
            return cursor.fetchall()

    def authenticate_user(self, username, password):
        """Authenticate a user by checking username and password."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                return user
            return None

    def add_patient(self, first_name, last_name, date_of_birth, gender, phone, address):
        """Add a patient to the patients table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone, address)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, date_of_birth, gender, phone, address))
            conn.commit()

    def get_all_patients(self):
        """Retrieve all patients from the patients table."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients")
            return cursor.fetchall()

    def search_patients(self, search_term):
        """Search patients by first name or last name."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM patients
                WHERE first_name LIKE ? OR last_name LIKE ?
            """, (f"%{search_term}%", f"%{search_term}%"))
            return cursor.fetchall()

    def add_prescription(self, patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed):
        """Add a prescription and its item to the prescriptions and prescription_items tables, updating inventory."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT quantity FROM inventory WHERE drug_id = ?", (drug_id,))
                current_quantity = cursor.fetchone()
                if not current_quantity or current_quantity[0] < quantity_prescribed:
                    raise ValueError(f"Insufficient stock for drug ID {drug_id}")

                cursor.execute("""
                    INSERT INTO prescriptions (patient_id, user_id, diagnosis, notes)
                    VALUES (?, ?, ?, ?)
                """, (patient_id, user_id, diagnosis, notes))
                prescription_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO prescription_items (prescription_id, drug_id, dosage_instructions, quantity_prescribed)
                    VALUES (?, ?, ?, ?)
                """, (prescription_id, drug_id, f"{dosage}, {frequency}, for {duration}", quantity_prescribed))

                cursor.execute("""
                    UPDATE inventory
                    SET quantity = quantity - ?
                    WHERE drug_id = ?
                """, (quantity_prescribed, drug_id))

                conn.commit()
                return prescription_id
            except Exception as e:
                conn.rollback()
                raise e

    def get_patient_prescriptions(self, patient_id):
        """Retrieve all prescriptions for a patient, including prescription items."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.prescription_id, p.prescription_date, p.diagnosis, p.notes,
                       pi.dosage_instructions, pi.quantity_prescribed, i.name as drug_name
                FROM prescriptions p
                JOIN prescription_items pi ON p.prescription_id = pi.prescription_id
                JOIN inventory i ON pi.drug_id = i.drug_id
                WHERE p.patient_id = ?
            """, (patient_id,))
            return cursor.fetchall()

    def add_drug(self, name, quantity, batch_number, expiry_date, price):
        """Add a drug to the inventory table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inventory (name, quantity, batch_number, expiry_date, price)
                VALUES (?, ?, ?, ?, ?)
            """, (name, quantity, batch_number, expiry_date, price))
            conn.commit()

    def get_all_drugs(self):
        """Retrieve all drugs from the inventory table."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory")
            return cursor.fetchall()

    def update_drug(self, drug_id, name, quantity, batch_number, expiry_date, price):
        """Update a drug in the inventory table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE inventory
                SET name = ?, quantity = ?, batch_number = ?, expiry_date = ?, price = ?
                WHERE drug_id = ?
            """, (name, quantity, batch_number, expiry_date, price, drug_id))
            conn.commit()

    def delete_drug(self, drug_id):
        """Delete a drug from the inventory table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventory WHERE drug_id = ?", (drug_id,))
            conn.commit()

    def get_expiring_drugs(self):
        """Retrieve drugs expiring within 30 days."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            expiry_threshold = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            cursor.execute("SELECT * FROM inventory WHERE expiry_date <= ?", (expiry_threshold,))
            return cursor.fetchall()

    def add_sale(self, patient_id, user_id, total_price, items):
        """Add a sale and its items, updating inventory quantities."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO sales (patient_id, user_id, total_price)
                    VALUES (?, ?, ?)
                """, (patient_id, user_id, total_price))
                sale_id = cursor.lastrowid

                for item in items:
                    drug_id = item['drug_id']
                    quantity_sold = item['quantity']
                    unit_price = item['price']

                    cursor.execute("SELECT quantity FROM inventory WHERE drug_id = ?", (drug_id,))
                    current_quantity = cursor.fetchone()[0]
                    if current_quantity < quantity_sold:
                        raise ValueError(f"Insufficient stock for drug ID {drug_id}")

                    cursor.execute("""
                        INSERT INTO sale_items (sale_id, drug_id, quantity_sold, unit_price)
                        VALUES (?, ?, ?, ?)
                    """, (sale_id, drug_id, quantity_sold, unit_price))

                    cursor.execute("""
                        UPDATE inventory
                        SET quantity = quantity - ?
                        WHERE drug_id = ?
                    """, (quantity_sold, drug_id))

                conn.commit()
                return sale_id
            except Exception as e:
                conn.rollback()
                raise e

    def get_sale_details(self, sale_id):
        """Retrieve details of a sale, including items."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.sale_id, s.sale_date, s.total_price, s.patient_id,
                       p.first_name, p.last_name
                FROM sales s
                JOIN patients p ON s.patient_id = p.patient_id
                WHERE s.sale_id = ?
            """, (sale_id,))
            sale = cursor.fetchone()

            cursor.execute("""
                SELECT si.sale_item_id, si.quantity_sold, si.unit_price,
                       i.drug_id, i.name
                FROM sale_items si
                JOIN inventory i ON si.drug_id = i.drug_id
                WHERE si.sale_id = ?
            """, (sale_id,))
            items = cursor.fetchall()

            return {'sale': sale, 'items': items}

    def get_sales_summary(self):
        """Get total sales value and count."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) as sale_count, SUM(total_price) as total_value
                FROM sales
            """)
            return cursor.fetchone()

    def get_prescriptions_by_user(self):
        """Get prescription count by user."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.username, COUNT(p.prescription_id) as prescription_count
                FROM prescriptions p
                JOIN users u ON p.user_id = u.user_id
                GROUP BY u.user_id, u.username
            """)
            return cursor.fetchall()

    def get_low_stock_drugs(self):
        """Get drugs with quantity <= 10."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT drug_id, name, quantity, batch_number, expiry_date, price
                FROM inventory
                WHERE quantity <= 10
            """)
            return cursor.fetchall()

    def get_sales_for_chart(self):
        """Get daily sales totals for the last 30 days."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sale_date, SUM(total_price) as daily_total
                FROM sales
                WHERE sale_date >= date('now', '-30 days')
                GROUP BY sale_date
                ORDER BY sale_date
            """)
            return cursor.fetchall()
