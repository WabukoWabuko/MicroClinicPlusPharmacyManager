import sqlite3
from pathlib import Path

class Database:
    def __init__(self):
        self.db_path = Path("database/clinic.db")
        self.init_db()

    def init_db(self):
        """Initialize the database by creating tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Read and execute schema.sql
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
