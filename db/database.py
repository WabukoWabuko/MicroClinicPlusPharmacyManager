import sqlite3
import bcrypt
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_path = "database/clinic.db"
        self.schema_path = "db/schema.sql"
        self.init_database()

    def init_database(self):
        """Initialize the database with schema.sql if it doesn't exist."""
        if not os.path.exists(self.db_path) or not self.table_exists("users"):
            with open(self.schema_path, 'r') as f:
                schema = f.read()
            conn = sqlite3.connect(self.db_path)
            conn.executescript(schema)
            conn.commit()
            conn.close()

    def table_exists(self, table_name):
        """Check if a table exists in the database."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def connect(self):
        """Connect to the database with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def authenticate_user(self, username, password):
        """Authenticate a user by verifying username and password."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return dict(user)
        return None

    def get_all_patients(self):
        """Retrieve all patients."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        patients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return patients

    def add_patient(self, first_name, last_name, age, gender, contact, medical_history):
        """Add a new patient."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patients (first_name, last_name, age, gender, contact, medical_history)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, age, gender, contact, medical_history))
        conn.commit()
        patient_id = cursor.lastrowid
        conn.close()
        return patient_id

    def get_patient(self, patient_id):
        """Retrieve a patient by ID."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
        patient = cursor.fetchone()
        conn.close()
        return dict(patient) if patient else None

    def get_all_drugs(self):
        """Retrieve all drugs."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drugs")
        drugs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return drugs

    def add_drug(self, name, quantity, batch_number, expiry_date, price):
        """Add a new drug."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO drugs (name, quantity, batch_number, expiry_date, price)
            VALUES (?, ?, ?, ?, ?)
        """, (name, quantity, batch_number, expiry_date, price))
        conn.commit()
        drug_id = cursor.lastrowid
        conn.close()
        return drug_id

    def get_drug(self, drug_id):
        """Retrieve a drug by ID."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drugs WHERE drug_id = ?", (drug_id,))
        drug = cursor.fetchone()
        conn.close()
        return dict(drug) if drug else None

    def update_drug(self, drug_id, quantity, batch_number, expiry_date, price):
        """Update a drug's details."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE drugs SET quantity = ?, batch_number = ?, expiry_date = ?, price = ?, updated_at = ?
            WHERE drug_id = ?
        """, (quantity, batch_number, expiry_date, price, datetime.now(), drug_id))
        conn.commit()
        conn.close()

    def delete_drug(self, drug_id):
        """Delete a drug."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM drugs WHERE drug_id = ?", (drug_id,))
        conn.commit()
        conn.close()

    def get_all_prescriptions(self):
        """Retrieve all prescriptions."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prescriptions")
        prescriptions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return prescriptions

    def add_prescription(self, patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed):
        """Add a new prescription."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO prescriptions (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed))
        conn.commit()
        prescription_id = cursor.lastrowid
        conn.close()
        return prescription_id

    def get_all_sales(self):
        """Retrieve all sales."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales")
        sales = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return sales

    def add_sale(self, patient_id, user_id, total_price):
        """Add a new sale."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sales (patient_id, user_id, total_price)
            VALUES (?, ?, ?)
        """, (patient_id, user_id, total_price))
        conn.commit()
        sale_id = cursor.lastrowid
        conn.close()
        return sale_id

    def add_sale_item(self, sale_id, drug_id, quantity, price):
        """Add a sale item."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sale_items (sale_id, drug_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (sale_id, drug_id, quantity, price))
        conn.commit()
        conn.close()

    def get_sale_items(self, sale_id):
        """Retrieve sale items for a sale."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sale_items WHERE sale_id = ?", (sale_id,))
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    def get_low_stock_drugs(self):
        """Retrieve drugs with low stock (quantity < 10)."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drugs WHERE quantity < 10")
        drugs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return drugs

    def add_user(self, username, password_hash, role):
        """Add a new user."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, password_hash, role))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    def get_all_users(self):
        """Retrieve all users."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users

    def update_user(self, user_id, username, password_hash, role):
        """Update a user's details."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET username = ?, password_hash = ?, role = ?, updated_at = ?
            WHERE user_id = ?
        """, (username, password_hash, role, datetime.now(), user_id))
        conn.commit()
        conn.close()

    def delete_user(self, user_id):
        """Delete a user."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

    def get_current_date(self):
        """Get the current date as a string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
