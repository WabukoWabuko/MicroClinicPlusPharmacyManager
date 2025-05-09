import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.db_path = Path("database/clinic.db")
        self.init_db()

    def init_db(self):
        """Initialize the database by creating tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Check if tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if not cursor.fetchone():
                # Read and execute schema.sql only if tables don't exist
                schema_path = Path("database/schema.sql")
                with open(schema_path, "r") as f:
                    cursor.executescript(f.read())
                conn.commit()

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

    def add_prescription(self, patient_id, user_id, diagnosis, notes, drug_name, dosage, frequency, duration):
        """Add a prescription and its item to the prescriptions and prescription_items tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Insert into prescriptions table
            cursor.execute("""
                INSERT INTO prescriptions (patient_id, user_id, diagnosis, notes)
                VALUES (?, ?, ?, ?)
            """, (patient_id, user_id, diagnosis, notes))
            prescription_id = cursor.lastrowid
            # Insert into prescription_items table
            cursor.execute("""
                INSERT INTO prescription_items (prescription_id, drug_id, dosage_instructions, quantity_prescribed)
                VALUES (?, ?, ?, ?)
            """, (prescription_id, 1, f"{dosage}, {frequency}, for {duration}", 1))  # drug_id=1 as placeholder
            conn.commit()
            return prescription_id

    def get_patient_prescriptions(self, patient_id):
        """Retrieve all prescriptions for a patient, including prescription items."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.prescription_id, p.prescription_date, p.diagnosis, p.notes,
                       pi.dosage_instructions
                FROM prescriptions p
                JOIN prescription_items pi ON p.prescription_id = pi.prescription_id
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
