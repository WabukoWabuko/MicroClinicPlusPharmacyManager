import sqlite3
import bcrypt
import os

class Database:
    def __init__(self):
        self.db_path = "database/clinic.db"
        self.init_db()

    def init_db(self):
        """Initialize the database with the schema."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            with open("database/schema.sql", "r") as f:
                cursor.executescript(f.read())
            # Insert default admin user
            cursor.execute(
                "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ("admin", bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(), "admin")
            )
            conn.commit()

    def authenticate_user(self, username, password):
        """Authenticate a user and update last_login."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
                cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?", (user["user_id"],))
                conn.commit()
                return user
            return None

    def add_user(self, username, password, role):
        """Add a new user."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            conn.commit()

    def update_user(self, user_id, username, password, role):
        """Update an existing user."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if password:
                password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                cursor.execute(
                    "UPDATE users SET username = ?, password_hash = ?, role = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                    (username, password_hash, role, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE users SET username = ?, role = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                    (username, role, user_id)
                )
            conn.commit()

    def delete_user(self, user_id):
        """Delete a user."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()

    def get_all_users(self):
        """Retrieve all users."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()

    def add_patient(self, first_name, last_name, age, gender, contact, medical_history):
        """Add a new patient."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO patients (first_name, last_name, age, gender, contact, medical_history) VALUES (?, ?, ?, ?, ?, ?)",
                (first_name, last_name, age, gender, contact, medical_history)
            )
            conn.commit()

    def get_patient(self, patient_id):
        """Retrieve a patient by their ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
            return cursor.fetchone()

    def get_all_patients(self):
        """Retrieve all patients."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients")
            return cursor.fetchall()

    def add_drug(self, name, quantity, batch_number, expiry_date, price):
        """Add a new drug."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO drugs (name, quantity, batch_number, expiry_date, price) VALUES (?, ?, ?, ?, ?)",
                (name, quantity, batch_number, expiry_date, price)
            )
            conn.commit()

    def update_drug(self, drug_id, name, quantity, batch_number, expiry_date, price):
        """Update an existing drug."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE drugs SET name = ?, quantity = ?, batch_number = ?, expiry_date = ?, price = ?, updated_at = CURRENT_TIMESTAMP WHERE drug_id = ?",
                (name, quantity, batch_number, expiry_date, price, drug_id)
            )
            conn.commit()

    def delete_drug(self, drug_id):
        """Delete a drug."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM drugs WHERE drug_id = ?", (drug_id,))
            conn.commit()

    def get_drug(self, drug_id):
        """Retrieve a drug by its ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM drugs WHERE drug_id = ?", (drug_id,))
            return cursor.fetchone()

    def get_all_drugs(self):
        """Retrieve all drugs."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM drugs")
            return cursor.fetchall()

    def get_low_stock_drugs(self, threshold=10):
        """Retrieve drugs with low stock."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM drugs WHERE quantity <= ?", (threshold,))
            return cursor.fetchall()

    def add_prescription(self, patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity):
        """Add a new prescription and update drug quantity."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT quantity FROM drugs WHERE drug_id = ?", (drug_id,))
            drug = cursor.fetchone()
            if not drug or drug[0] < quantity:
                raise ValueError("Insufficient drug quantity")
            cursor.execute(
                "INSERT INTO prescriptions (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity)
            )
            cursor.execute("UPDATE drugs SET quantity = quantity - ? WHERE drug_id = ?", (quantity, drug_id))
            conn.commit()

    def get_all_prescriptions(self):
        """Retrieve all prescriptions."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prescriptions")
            return cursor.fetchall()

    def add_sale(self, patient_id, user_id, total_price, sale_items):
        """Add a new sale and update drug quantities."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sales (patient_id, user_id, total_price) VALUES (?, ?, ?)",
                (patient_id, user_id, total_price)
            )
            sale_id = cursor.lastrowid
            for item in sale_items:
                cursor.execute("SELECT quantity FROM drugs WHERE drug_id = ?", (item['drug_id'],))
                drug = cursor.fetchone()
                if not drug or drug[0] < item['quantity']:
                    raise ValueError(f"Insufficient stock for {item['name']}")
                cursor.execute(
                    "INSERT INTO sale_items (sale_id, drug_id, quantity, price) VALUES (?, ?, ?, ?)",
                    (sale_id, item['drug_id'], item['quantity'], item['price'])
                )
                cursor.execute("UPDATE drugs SET quantity = quantity - ? WHERE drug_id = ?", (item['quantity'], item['drug_id']))
            conn.commit()
            return sale_id

    def get_sale(self, sale_id):
        """Retrieve a sale by its ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sales WHERE sale_id = ?", (sale_id,))
            return cursor.fetchone()

    def get_all_sales(self):
        """Retrieve all sales."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sales")
            return cursor.fetchall()

    def get_sale_items(self, sale_id):
        """Retrieve items for a specific sale."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT si.*, d.name FROM sale_items si JOIN drugs d ON si.drug_id = d.drug_id WHERE si.sale_id = ?", (sale_id,))
            return cursor.fetchall()
