import sqlite3
import bcrypt
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import requests
import json

class Database:
    def __init__(self):
        self.db_path = "database/clinic.db"
        self.schema_path = "db/schema.sql"
        self.config_path = "database/config.json"
        load_dotenv()
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = None
        self.sync_enabled = False
        self.last_sync_time = None
        if self.supabase_url and self.supabase_key:
            self.supabase = create_client(self.supabase_url, self.supabase_key)
        self.init_database()
        self.load_config()

    def init_database(self):
        """Initialize the local SQLite database with schema.sql."""
        if not os.path.exists(self.db_path) or not self.table_exists("users"):
            with open(self.schema_path, 'r') as f:
                schema = f.read()
            conn = sqlite3.connect(self.db_path)
            conn.executescript(schema)
            conn.commit()
            conn.close()
        # Create sync_queue table in SQLite if not exists
        conn = self.connect()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sync_queue (
                queue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                operation TEXT NOT NULL,
                record_id INTEGER NOT NULL,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        """)
        conn.commit()
        conn.close()

    def load_config(self):
        """Load settings from config.json."""
        default_config = {
            "clinic_name": "MicroClinic",
            "logo_path": "",
            "currency_symbol": "KSh",
            "sync_enabled": False
        }
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
            self.sync_enabled = default_config["sync_enabled"]
            return default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_config

    def save_config(self, config):
        """Save settings to config.json."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def table_exists(self, table_name):
        """Check if a table exists in the local SQLite database."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def supabase_table_exists(self, table_name):
        """Check if a table exists in Supabase."""
        if not self.supabase:
            return False
        try:
            self.supabase.table(table_name).select("*").limit(1).execute()
            return True
        except Exception as e:
            if '42P01' in str(e):
                return False
            raise e

    def connect(self):
        """Connect to the local SQLite database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def is_online(self):
        """Check if internet connection is available."""
        try:
            requests.get("https://www.google.com", timeout=2)
            return True
        except requests.ConnectionError:
            return False

    def toggle_sync(self, enabled):
        """Enable or disable cloud sync and save to config."""
        self.sync_enabled = enabled
        config = self.load_config()
        config["sync_enabled"] = enabled
        self.save_config(config)
        if enabled and self.is_online():
            self.sync_data()

    def queue_sync_operation(self, table_name, operation, record_id, data):
        """Add an operation to the sync queue."""
        if not self.sync_enabled:
            return
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sync_queue (table_name, operation, record_id, data, status)
            VALUES (?, ?, ?, ?, 'pending')
        """, (table_name, operation, record_id, json.dumps(data)))
        conn.commit()
        conn.close()

    def sync_data(self):
        """Sync local SQLite with Supabase."""
        if not self.sync_enabled or not self.is_online() or not self.supabase:
            return
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sync_queue WHERE status = 'pending'")
        queue_items = [dict(row) for row in cursor.fetchall()]
        
        for item in queue_items:
            table_name = item['table_name']
            operation = item['operation']
            record_id = item['record_id']
            data = json.loads(item['data']) if item['data'] else {}
            if not self.supabase_table_exists(table_name):
                print(f"Error: Supabase table '{table_name}' does not exist. Skipping sync for queue_id {item['queue_id']}.")
                continue
            try:
                if operation == 'INSERT':
                    response = self.supabase.table(table_name).insert(data).execute()
                    if response.data:
                        conn.execute(f"UPDATE {table_name} SET is_synced = 1, sync_status = 'synced' WHERE {table_name}_id = ?", (record_id,))
                elif operation == 'UPDATE':
                    response = self.supabase.table(table_name).update(data).eq(f"{table_name}_id", record_id).execute()
                    if response.data:
                        conn.execute(f"UPDATE {table_name} SET is_synced = 1, sync_status = 'synced' WHERE {table_name}_id = ?", (record_id,))
                elif operation == 'DELETE':
                    response = self.supabase.table(table_name).delete().eq(f"{table_name}_id", record_id).execute()
                    if response.data:
                        conn.execute(f"UPDATE sync_queue SET status = 'synced' WHERE queue_id = ?", (item['queue_id'],))
                conn.execute("UPDATE sync_queue SET status = 'synced' WHERE queue_id = ?", (item['queue_id'],))
            except Exception as e:
                conn.execute("UPDATE sync_queue SET status = 'failed' WHERE queue_id = ?", (item['queue_id'],))
                print(f"Sync error for {table_name} {operation}: {e}")
        
        for table in ['patients', 'drugs', 'prescriptions', 'sales', 'sale_items']:
            if not self.supabase_table_exists(table):
                print(f"Error: Supabase table '{table}' does not exist. Skipping pull.")
                continue
            local_data = {row[f"{table[:-1]}_id"]: dict(row) for row in conn.execute(f"SELECT * FROM {table}").fetchall()}
            try:
                remote_data = self.supabase.table(table).select("*").execute().data
            except Exception as e:
                print(f"Error fetching Supabase table '{table}': {e}")
                continue
            for remote_row in remote_data:
                remote_id = remote_row[f"{table[:-1]}_id"]
                remote_updated_at = datetime.fromisoformat(remote_row['updated_at'].replace('Z', '+00:00'))
                local_row = local_data.get(remote_id)
                if not local_row:
                    cols = ', '.join(remote_row.keys())
                    placeholders = ', '.join('?' for _ in remote_row)
                    conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", list(remote_row.values()))
                elif datetime.fromisoformat(local_row['updated_at'].replace('Z', '+00:00')) < remote_updated_at:
                    updates = ', '.join(f"{k} = ?" for k in remote_row.keys() if k != f"{table[:-1]}_id")
                    conn.execute(f"UPDATE {table} SET {updates} WHERE {table[:-1]}_id = ?", 
                                 list(remote_row.values())[:-1] + [remote_id])
        
        conn.commit()
        conn.close()
        self.last_sync_time = datetime.now()

    def get_sync_history(self, limit=100):
        """Retrieve sync history from sync_queue with enriched details."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sync_queue ORDER BY created_at DESC LIMIT ?", (limit,))
        queue_items = [dict(row) for row in cursor.fetchall()]
        history = []
        
        for item in queue_items:
            details = ""
            table_name = item['table_name']
            data = json.loads(item['data']) if item['data'] else {}
            if table_name == 'patients' and 'first_name' in data and 'last_name' in data:
                details = f"Patient: {data['first_name']} {data['last_name']}"
            elif table_name == 'drugs' and 'name' in data:
                details = f"Drug: {data['name']}"
            elif table_name == 'prescriptions' and 'diagnosis' in data:
                details = f"Diagnosis: {data['diagnosis']}"
            elif table_name == 'sales' and 'total_price' in data:
                details = f"Total: ${data['total_price']}"
            elif table_name == 'sale_items' and 'quantity' in data:
                details = f"Quantity: {data['quantity']}"
            history.append({
                'table_name': table_name,
                'operation': item['operation'],
                'record_id': item['record_id'],
                'status': item['status'],
                'timestamp': item['created_at'],
                'details': details
            })
        
        conn.close()
        return history

    def authenticate_user(self, username, password):
        """Authenticate a user."""
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
            INSERT INTO patients (first_name, last_name, age, gender, contact, medical_history, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, ?, 0, 'pending')
        """, (first_name, last_name, age, gender, contact, medical_history))
        patient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('patients', 'INSERT', patient_id, {
            'patient_id': patient_id, 'first_name': first_name, 'last_name': last_name, 'age': age,
            'gender': gender, 'contact': contact, 'medical_history': medical_history,
            'registration_date': datetime.now().isoformat(), 'updated_at': datetime.now().isoformat(),
            'is_synced': False, 'sync_status': 'pending'
        })
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
            INSERT INTO drugs (name, quantity, batch_number, expiry_date, price, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, 0, 'pending')
        """, (name, quantity, batch_number, expiry_date, price))
        drug_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('drugs', 'INSERT', drug_id, {
            'drug_id': drug_id, 'name': name, 'quantity': quantity, 'batch_number': batch_number,
            'expiry_date': expiry_date, 'price': price, 'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(), 'is_synced': False, 'sync_status': 'pending'
        })
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
            UPDATE drugs SET quantity = ?, batch_number = ?, expiry_date = ?, price = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE drug_id = ?
        """, (quantity, batch_number, expiry_date, price, datetime.now(), drug_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('drugs', 'UPDATE', drug_id, {
            'drug_id': drug_id, 'quantity': quantity, 'batch_number': batch_number,
            'expiry_date': expiry_date, 'price': price, 'updated_at': datetime.now().isoformat(),
            'is_synced': False, 'sync_status': 'pending'
        })

    def delete_drug(self, drug_id):
        """Delete a drug."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM drugs WHERE drug_id = ?", (drug_id,))
        conn.commit()
        conn.close()
        self.queue_sync_operation('drugs', 'DELETE', drug_id, {})

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
            INSERT INTO prescriptions (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 'pending')
        """, (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed))
        prescription_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('prescriptions', 'INSERT', prescription_id, {
            'prescription_id': prescription_id, 'patient_id': patient_id, 'user_id': user_id,
            'diagnosis': diagnosis, 'notes': notes, 'drug_id': drug_id, 'dosage': dosage,
            'frequency': frequency, 'duration': duration, 'quantity_prescribed': quantity_prescribed,
            'prescription_date': datetime.now().isoformat(), 'updated_at': datetime.now().isoformat(),
            'is_synced': False, 'sync_status': 'pending'
        })
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
            INSERT INTO sales (patient_id, user_id, total_price, is_synced, sync_status)
            VALUES (?, ?, ?, 0, 'pending')
        """, (patient_id, user_id, total_price))
        sale_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('sales', 'INSERT', sale_id, {
            'sale_id': sale_id, 'patient_id': patient_id, 'user_id': user_id,
            'total_price': total_price, 'sale_date': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(), 'is_synced': False, 'sync_status': 'pending'
        })
        return sale_id

    def add_sale_item(self, sale_id, drug_id, quantity, price):
        """Add a sale item."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sale_items (sale_id, drug_id, quantity, price, is_synced, sync_status)
            VALUES (?, ?, ?, ?, 0, 'pending')
        """, (sale_id, drug_id, quantity, price))
        sale_item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('sale_items', 'INSERT', sale_item_id, {
            'sale_item_id': sale_item_id, 'sale_id': sale_id, 'drug_id': drug_id,
            'quantity': quantity, 'price': price, 'updated_at': datetime.now().isoformat(),
            'is_synced': False, 'sync_status': 'pending'
        })

    def get_sale_items(self, sale_id):
        """Retrieve sale items for a sale."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sale_items WHERE sale_id = ?", (sale_id,))
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    def get_low_stock_drugs(self):
        """Retrieve drugs with low stock."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drugs WHERE quantity < 10")
        drugs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return drugs

    def add_user(self, username, password_hash, role):
        """Add a new user (local only)."""
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
