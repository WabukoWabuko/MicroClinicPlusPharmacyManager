import sqlite3
import bcrypt
import os
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv
import requests
import json
import pytz
import re

class Database:
    def __init__(self):
        self.db_path = "database/clinic.db"
        self.schema_path = "database/schema.sql"
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
        # Create suppliers table in SQLite if not exists
        conn.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                products_supplied TEXT,
                last_delivery_date TEXT,
                responsible_person TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_synced INTEGER DEFAULT 0,
                sync_status TEXT DEFAULT 'pending'
            )
        """)
        # Insert initial config values for demo period and activation
        current_time = datetime.now(pytz.timezone('Africa/Nairobi')).strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)",
                     ("first_launch_date", current_time))
        conn.execute("INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)",
                     ("activation_code", "ACTIVATE2025"))
        conn.execute("INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)",
                     ("is_activated", "false"))
        conn.commit()
        conn.close()

    def load_config(self):
        """Load settings from config.json and database config table."""
        default_config = {
            "clinic_name": "MicroClinic",
            "logo_path": "",
            "background_path": "",
            "tax_rate": 0,
            "contact_details": "",
            "currency_symbol": "KSh",
            "sync_enabled": False,
            "first_launch_date": None,
            "activation_code": None,
            "is_activated": "false"
        }
        try:
            # Load from config.json
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)

            # Load from config table
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM config")
            db_config = dict(cursor.fetchall())
            conn.close()
            default_config.update(db_config)

            self.sync_enabled = default_config["sync_enabled"]
            if os.path.exists("last_sync.txt"):
                with open("last_sync.txt", "r") as f:
                    last_sync_str = f.read().strip()
                    if last_sync_str:
                        self.last_sync_time = datetime.fromisoformat(last_sync_str)
                        if self.last_sync_time.tzinfo is None:
                            self.last_sync_time = pytz.UTC.localize(self.last_sync_time)
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

    def save_last_sync_time(self):
        """Save the last sync time to a file."""
        try:
            with open("last_sync.txt", "w") as f:
                f.write(self.last_sync_time.isoformat())
        except Exception as e:
            print(f"Error saving last sync time: {e}")

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

    def push_changes(self, tables):
        """Push local changes to Supabase based on sync queue."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sync_queue WHERE status = 'pending' ORDER BY created_at")
        pending_operations = cursor.fetchall()

        table_priority = {
            "users": 1,
            "patients": 2,
            "drugs": 2,
            "suppliers": 2,
            "prescriptions": 3,
            "sales": 3,
            "sale_items": 4
        }
        pending_operations = sorted(pending_operations, key=lambda op: table_priority.get(op['table_name'], 5))

        # Force resync of all users if any dependent table fails due to user_id
        user_ids_to_resync = set()
        for op in pending_operations:
            queue_id = op['queue_id']
            table_name = op['table_name']
            operation = op['operation']
            record_id = op['record_id']
            data = json.loads(op['data']) if op['data'] else {}

            try:
                # Validate data before pushing (e.g., for patients table)
                if table_name == 'patients' and data:
                    if 'age' in data:
                        try:
                            age = int(data['age'])
                            if age <= 0 or age > 150:
                                print(f"Invalid age ({age}) for patient_id {record_id}. Skipping sync operation.")
                                cursor.execute("UPDATE sync_queue SET status = 'failed' WHERE queue_id = ?", (queue_id,))
                                conn.commit()
                                continue
                        except (ValueError, TypeError):
                            print(f"Invalid age value ({data['age']}) for patient_id {record_id}. Skipping sync operation.")
                            cursor.execute("UPDATE sync_queue SET status = 'failed' WHERE queue_id = ?", (queue_id,))
                            conn.commit()
                            continue

                    if 'contact' in data:
                        contact = str(data['contact']).strip()
                        if not re.match(r'^\+[0-9]{3}[0-9]{9}$', contact):
                            print(f"Invalid contact ({contact}) for patient_id {record_id}. Setting to default for sync.")
                            data['contact'] = '+254000000000'

                # Convert SQLite INTEGER (0/1) to BOOLEAN for Supabase
                if 'is_synced' in data:
                    data['is_synced'] = bool(data['is_synced'])

                # Ensure timestamps are in the correct format for Supabase
                for key in ['created_at', 'updated_at', 'registration_date', 'prescription_date', 'sale_date']:
                    if key in data and data[key]:
                        try:
                            dt = datetime.fromisoformat(data[key].replace("Z", "+00:00"))
                            data[key] = dt.isoformat()
                        except ValueError:
                            dt = datetime.strptime(data[key], "%Y-%m-%d %H:%M:%S")
                            dt = pytz.UTC.localize(dt)
                            data[key] = dt.isoformat()

                # Push to Supabase based on operation
                if operation == 'INSERT':
                    response = self.supabase.table(table_name).insert(data).execute()
                    print(f"Pushed INSERT for {table_name} record ID {record_id} to Supabase")
                elif operation == 'UPDATE':
                    response = self.supabase.table(table_name).update(data).eq(f"{table_name[:-1]}_id", record_id).execute()
                    print(f"Pushed UPDATE for {table_name} record ID {record_id} to Supabase")
                elif operation == 'DELETE':
                    response = self.supabase.table(table_name).delete().eq(f"{table_name[:-1]}_id", record_id).execute()
                    print(f"Pushed DELETE for {table_name} record ID {record_id} to Supabase")

                cursor.execute(f"UPDATE {table_name} SET is_synced = 1, sync_status = 'synced' WHERE {table_name[:-1]}_id = ?", (record_id,))
                cursor.execute("UPDATE sync_queue SET status = 'synced' WHERE queue_id = ?", (queue_id,))

            except Exception as e:
                error_msg = str(e)
                print(f"Error syncing {operation} for {table_name} record ID {record_id}: {e}")
                cursor.execute("UPDATE sync_queue SET status = 'failed' WHERE queue_id = ?", (queue_id,))
                # Collect user_ids to resync if foreign key violation
                if '23503' in error_msg and 'user_id' in error_msg:
                    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (data.get('user_id'),))
                    user = cursor.fetchone()
                    if user:
                        user_ids_to_resync.add(user['user_id'])
                elif '23503' in error_msg and 'sale_id' in error_msg:
                    cursor.execute("SELECT sale_id FROM sales WHERE sale_id = ?", (data.get('sale_id'),))
                    sale = cursor.fetchone()
                    if sale:
                        cursor.execute("SELECT user_id FROM sales WHERE sale_id = ?", (sale['sale_id'],))
                        user = cursor.fetchone()
                        if user:
                            user_ids_to_resync.add(user['user_id'])

        # Resync users if any dependencies failed
        if user_ids_to_resync:
            cursor.execute("SELECT * FROM users WHERE user_id IN ({})".format(','.join('?' * len(user_ids_to_resync))), list(user_ids_to_resync))
            users_to_resync = cursor.fetchall()
            for user in users_to_resync:
                user_data = {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'password_hash': user['password_hash'],
                    'role': user['role'],
                    'created_at': user['created_at'],
                    'updated_at': user['updated_at'],
                    'is_synced': bool(user['is_synced']),
                    'sync_status': user['sync_status']
                }
                try:
                    response = self.supabase.table('users').upsert(user_data).execute()
                    print(f"Resynced user with ID {user['user_id']} to Supabase")
                    cursor.execute("UPDATE users SET is_synced = 1, sync_status = 'synced' WHERE user_id = ?", (user['user_id'],))
                except Exception as e:
                    print(f"Error resyncing user ID {user['user_id']}: {e}")

        conn.commit()
        conn.close()

    def sync_data(self):
        """Synchronize local database with Supabase."""
        if not self.supabase or not self.sync_enabled:
            return

        if not self.is_online():
            print("Offline: Changes will sync when online.")
            return

        print("Starting sync...")

        tables = ["users", "patients", "drugs", "suppliers", "prescriptions", "sales", "sale_items"]

        self.push_changes(tables)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for table in tables:
            print(f"Pulling changes for {table}...")

            last_sync = self.last_sync_time or datetime(1970, 1, 1, tzinfo=pytz.UTC)

            try:
                response = self.supabase.table(table).select("*").gt("updated_at", last_sync.isoformat()).execute()
                remote_data = response.data
            except Exception as e:
                print(f"Error fetching {table} from Supabase: {e}")
                continue

            for remote_row in remote_data:
                remote_id = remote_row[f"{table[:-1]}_id"]
                remote_updated_at = datetime.fromisoformat(remote_row["updated_at"].replace("Z", "+00:00"))

                if table == 'patients':
                    if 'age' in remote_row:
                        try:
                            age = int(remote_row['age'])
                            if age <= 0:
                                print(f"Warning: Invalid age ({age}) for patient_id {remote_id}. Clamping to 1.")
                                remote_row['age'] = 1
                            elif age > 150:
                                print(f"Warning: Invalid age ({age}) for patient_id {remote_id}. Clamping to 150.")
                                remote_row['age'] = 150
                        except (ValueError, TypeError):
                            print(f"Warning: Invalid age value ({remote_row['age']}) for patient_id {remote_id}. Skipping record.")
                            continue

                    if 'contact' in remote_row:
                        contact = str(remote_row['contact']).strip()
                        if not re.match(r'^\+[0-9]{3}[0-9]{9}$', contact):
                            print(f"Warning: Invalid contact ({contact}) for patient_id {remote_id}. Setting to default.")
                            remote_row['contact'] = '+254000000000'

                # Convert Supabase BOOLEAN to SQLite INTEGER
                if 'is_synced' in remote_row:
                    remote_row['is_synced'] = 1 if remote_row['is_synced'] else 0

                # Convert Supabase timestamps to SQLite format
                for key in ['created_at', 'updated_at', 'registration_date', 'prescription_date', 'sale_date']:
                    if key in remote_row and remote_row[key]:
                        dt = datetime.fromisoformat(remote_row[key].replace("Z", "+00:00"))
                        remote_row[key] = dt.strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute(f"SELECT updated_at, is_synced FROM {table} WHERE {table[:-1]}_id = ?", (remote_id,))
                local_row = cursor.fetchone()

                if local_row:
                    local_updated_at_str = local_row[0] if local_row[0] else "1970-01-01 00:00:00"
                    try:
                        # Try parsing as ISO format first
                        local_updated_at = datetime.fromisoformat(local_updated_at_str.replace("Z", "+00:00"))
                    except ValueError:
                        # Fall back to expected format
                        local_updated_at = datetime.strptime(local_updated_at_str, "%Y-%m-%d %H:%M:%S")
                    local_updated_at = pytz.UTC.localize(local_updated_at) if local_updated_at.tzinfo is None else local_updated_at
                    is_synced = bool(local_row[1])

                    if remote_updated_at > local_updated_at:
                        updates = ", ".join([f"{key} = ?" for key in remote_row.keys() if key != f"{table[:-1]}_id"])
                        values = [remote_row[key] for key in remote_row.keys() if key != f"{table[:-1]}_id"] + [remote_id]
                        cursor.execute(f"UPDATE {table} SET {updates} WHERE {table[:-1]}_id = ?", values)
                        print(f"Updated {table[:-1]} with ID {remote_id}")
                else:
                    columns = ", ".join(remote_row.keys())
                    placeholders = ", ".join(["?" for _ in remote_row])
                    values = [remote_row[key] for key in remote_row.keys()]
                    cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
                    print(f"Inserted new {table[:-1]} with ID {remote_id}")

        conn.commit()
        conn.close()

        self.last_sync_time = datetime.now(pytz.UTC)
        self.save_last_sync_time()
        print(f"Sync completed at {self.last_sync_time}")

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
            elif table_name == 'suppliers' and 'name' in data:
                details = f"Supplier: {data['name']}"
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
        cursor.execute("SELECT * FROM patients ORDER BY first_name, last_name")
        patients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return patients

    def get_top_patients(self, limit=5):
        """Retrieve the top patients by prescription count."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, COUNT(pr.prescription_id) as prescription_count
            FROM patients p
            LEFT JOIN prescriptions pr ON p.patient_id = pr.patient_id
            GROUP BY p.patient_id
            ORDER BY prescription_count DESC, p.first_name, p.last_name
            LIMIT ?
        """, (limit,))
        patients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return patients

    def add_patient(self, first_name, last_name, age, gender, contact, medical_history):
        """Add a new patient."""
        conn = self.connect()
        cursor = conn.cursor()
        current_time = datetime.now(pytz.UTC)
        cursor.execute("""
            INSERT INTO patients (first_name, last_name, age, gender, contact, medical_history, registration_date, updated_at, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 'pending')
        """, (first_name, last_name, age, gender, contact, medical_history, current_time.strftime("%Y-%m-%d %H:%M:%S"), current_time.strftime("%Y-%m-%d %H:%M:%S")))
        patient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('patients', 'INSERT', patient_id, {
            'patient_id': patient_id, 'first_name': first_name, 'last_name': last_name, 'age': age,
            'gender': gender, 'contact': contact, 'medical_history': medical_history,
            'registration_date': current_time.isoformat(), 'updated_at': current_time.isoformat(),
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
        
    def update_patient(self, patient_id, first_name, last_name, age, gender, contact, medical_history):
        conn = self.connect()
        cursor = conn.cursor()
        updated_at = datetime.now(pytz.UTC)
        cursor.execute("""
            UPDATE patients SET first_name = ?, last_name = ?, age = ?, gender = ?, contact = ?, medical_history = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE patient_id = ?
        """, (first_name, last_name, age, gender, contact, medical_history, updated_at.strftime("%Y-%m-%d %H:%M:%S"), patient_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('patients', 'UPDATE', patient_id, {
            'patient_id': patient_id, 'first_name': first_name, 'last_name': last_name, 'age': age,
            'gender': gender, 'contact': contact, 'medical_history': medical_history,
            'updated_at': updated_at.isoformat(), 'is_synced': False, 'sync_status': 'pending'
        })
        
    def delete_patient(self, patient_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
        conn.commit()
        conn.close()
        self.queue_sync_operation('patients', 'DELETE', patient_id, {})

    def get_all_drugs(self):
        """Retrieve all drugs."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drugs ORDER BY name")
        drugs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return drugs

    def get_top_drugs(self, limit=5):
        """Retrieve the top drugs by prescription and sale count."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.*,
                   (COALESCE((SELECT SUM(pr.quantity_prescribed) FROM prescriptions pr WHERE pr.drug_id = d.drug_id), 0) +
                    COALESCE((SELECT SUM(si.quantity) FROM sale_items si WHERE si.drug_id = d.drug_id), 0)) as usage_count
            FROM drugs d
            GROUP BY d.drug_id
            ORDER BY usage_count DESC, d.name
            LIMIT ?
        """, (limit,))
        drugs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return drugs

    def add_drug(self, name, quantity, batch_number, expiry_date, price):
        """Add a new drug."""
        conn = self.connect()
        cursor = conn.cursor()
        current_time = datetime.now(pytz.UTC)
        cursor.execute("""
            INSERT INTO drugs (name, quantity, batch_number, expiry_date, price, created_at, updated_at, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0, 'pending')
        """, (name, quantity, batch_number, expiry_date, price, current_time.strftime("%Y-%m-%d %H:%M:%S"), current_time.strftime("%Y-%m-%d %H:%M:%S")))
        drug_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('drugs', 'INSERT', drug_id, {
            'drug_id': drug_id, 'name': name, 'quantity': quantity, 'batch_number': batch_number,
            'expiry_date': expiry_date, 'price': price, 'created_at': current_time.isoformat(),
            'updated_at': current_time.isoformat(), 'is_synced': False, 'sync_status': 'pending'
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

    def update_drug(self, drug_id, name, quantity, batch_number, expiry_date, price):
        """Update a drug's details, including name."""
        conn = self.connect()
        cursor = conn.cursor()
        updated_at = datetime.now(pytz.UTC)
        cursor.execute("""
            UPDATE drugs SET name = ?, quantity = ?, batch_number = ?, expiry_date = ?, price = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE drug_id = ?
        """, (name, quantity, batch_number, expiry_date, price, updated_at.strftime("%Y-%m-%d %H:%M:%S"), drug_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('drugs', 'UPDATE', drug_id, {
            'drug_id': drug_id, 'name': name, 'quantity': quantity, 'batch_number': batch_number,
            'expiry_date': expiry_date, 'price': price, 'updated_at': updated_at.isoformat(),
            'is_synced': False, 'sync_status': 'pending'
        })

    def reduce_drug_stock(self, drug_id, quantity):
        """Reduce the stock of a drug by the specified quantity."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT quantity FROM drugs WHERE drug_id = ?", (drug_id,))
        drug = cursor.fetchone()
        if not drug:
            conn.close()
            raise ValueError("Drug not found.")
        current_quantity = drug['quantity']
        if current_quantity < quantity:
            conn.close()
            raise ValueError("Insufficient stock for this drug.")
        new_quantity = current_quantity - quantity
        updated_at = datetime.now(pytz.UTC)
        cursor.execute("""
            UPDATE drugs SET quantity = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE drug_id = ?
        """, (new_quantity, updated_at.strftime("%Y-%m-%d %H:%M:%S"), drug_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('drugs', 'UPDATE', drug_id, {
            'drug_id': drug_id, 'quantity': new_quantity, 'updated_at': updated_at.isoformat(),
            'is_synced': False, 'sync_status': 'pending'
        })
        if new_quantity < 10:
            return f"Warning: Stock for drug ID {drug_id} is low ({new_quantity} units remaining)."
        return None

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
        
    def get_prescription(self, prescription_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prescriptions WHERE prescription_id = ?", (prescription_id,))
        prescription = cursor.fetchone()
        conn.close()
        return dict(prescription) if prescription else None

    def delete_prescription(self, prescription_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prescriptions WHERE prescription_id = ?", (prescription_id,))
        conn.commit()
        conn.close()
        self.queue_sync_operation('prescriptions', 'DELETE', prescription_id, {})
    
    def update_prescription(self, prescription_id, patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed):
        conn = self.connect()
        cursor = conn.cursor()
        current_time = datetime.now(pytz.UTC)
        cursor.execute("""
            UPDATE prescriptions SET patient_id = ?, user_id = ?, diagnosis = ?, notes = ?, drug_id = ?, dosage = ?, frequency = ?, duration = ?, quantity_prescribed = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE prescription_id = ?
        """, (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed, current_time.strftime("%Y-%m-%d %H:%M:%S"), prescription_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('prescriptions', 'UPDATE', prescription_id, {
            'prescription_id': prescription_id, 'patient_id': patient_id, 'user_id': user_id, 'diagnosis': diagnosis,
            'notes': notes, 'drug_id': drug_id, 'dosage': dosage, 'frequency': frequency, 'duration': duration,
            'quantity_prescribed': quantity_prescribed, 'updated_at': current_time.isoformat(),
            'is_synced': False, 'sync_status': 'pending'
        })
        

    def add_prescription(self, patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed):
        conn = self.connect()
        cursor = conn.cursor()
        current_time = datetime.now(pytz.UTC)
        cursor.execute("""
            INSERT INTO prescriptions (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed, prescription_date, updated_at, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 'pending')
        """, (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed, current_time.strftime("%Y-%m-%d %H:%M:%S"), current_time.strftime("%Y-%m-%d %H:%M:%S")))
        prescription_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('prescriptions', 'INSERT', prescription_id, {
            'prescription_id': prescription_id, 'patient_id': patient_id, 'user_id': user_id, 'diagnosis': diagnosis,
            'notes': notes, 'drug_id': drug_id, 'dosage': dosage, 'frequency': frequency, 'duration': duration,
            'quantity_prescribed': quantity_prescribed, 'prescription_date': current_time.isoformat(),
            'updated_at': current_time.isoformat(), 'is_synced': False, 'sync_status': 'pending'
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

    def add_sale(self, patient_id, user_id, total_price, mode_of_payment):
        """Add a new sale."""
        conn = self.connect()
        cursor = conn.cursor()
        current_time = datetime.now(pytz.UTC)
        cursor.execute("""
            INSERT INTO sales (patient_id, user_id, total_price, mode_of_payment, sale_date, updated_at, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, ?, 0, 'pending')
        """, (patient_id, user_id, total_price, mode_of_payment, current_time.strftime("%Y-%m-%d %H:%M:%S"), current_time.strftime("%Y-%m-%d %H:%M:%S")))
        sale_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('sales', 'INSERT', sale_id, {
            'sale_id': sale_id, 'patient_id': patient_id, 'user_id': user_id,
            'total_price': total_price, 'mode_of_payment': mode_of_payment, 'sale_date': current_time.isoformat(),
            'updated_at': current_time.isoformat(), 'is_synced': False, 'sync_status': 'pending'
        })
        return sale_id

    def add_sale_item(self, sale_id, drug_id, quantity, price):
        """Add a sale item to the database without modifying stock."""
        conn = self.connect()
        cursor = conn.cursor()
        current_time = datetime.now(pytz.UTC)
        cursor.execute("""
            INSERT INTO sale_items (sale_id, drug_id, quantity, price, updated_at, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, 0, 'pending')
        """, (sale_id, drug_id, quantity, price, current_time.strftime("%Y-%m-%d %H:%M:%S")))
        sale_item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('sale_items', 'INSERT', sale_item_id, {
            'sale_item_id': sale_item_id, 'sale_id': sale_id, 'drug_id': drug_id,
            'quantity': quantity, 'price': price, 'updated_at': current_time.isoformat(),
            'is_synced': False, 'sync_status': 'pending'
        })

    def get_sale_items(self, sale_id):
        """Retrieve sale items for a sale with drug names."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT si.*, d.name
            FROM sale_items si
            JOIN drugs d ON si.drug_id = d.drug_id
            WHERE si.sale_id = ?
        """, (sale_id,))
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    def get_sale(self, sale_id):
        """Retrieve a sale and its items by sale ID."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales WHERE sale_id = ?", (sale_id,))
        sale = cursor.fetchone()
        if sale:
            sale = dict(sale)
            sale['items'] = self.get_sale_items(sale_id)
        conn.close()
        return sale

    def get_all_suppliers(self):
        """Retrieve all suppliers."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suppliers ORDER BY name")
        suppliers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return suppliers

    def add_supplier(self, name, phone, email, address, products_supplied, last_delivery_date, responsible_person, notes):
        """Add a new supplier."""
        conn = self.connect()
        cursor = conn.cursor()
        current_time = datetime.now(pytz.UTC)
        cursor.execute("""
            INSERT INTO suppliers (name, phone, email, address, products_supplied, last_delivery_date, responsible_person, notes, created_at, updated_at, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 'pending')
        """, (name, phone, email, address, products_supplied, last_delivery_date, responsible_person, notes, current_time.strftime("%Y-%m-%d %H:%M:%S"), current_time.strftime("%Y-%m-%d %H:%M:%S")))
        supplier_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('suppliers', 'INSERT', supplier_id, {
            'supplier_id': supplier_id, 'name': name, 'phone': phone, 'email': email,
            'address': address, 'products_supplied': products_supplied,
            'last_delivery_date': last_delivery_date, 'responsible_person': responsible_person,
            'notes': notes, 'created_at': current_time.isoformat(),
            'updated_at': current_time.isoformat(), 'is_synced': False, 'sync_status': 'pending'
        })
        return supplier_id

    def get_supplier(self, supplier_id):
        """Retrieve a supplier by ID."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suppliers WHERE supplier_id = ?", (supplier_id,))
        supplier = cursor.fetchone()
        conn.close()
        return dict(supplier) if supplier else None

    def update_supplier(self, supplier_id, name, phone, email, address, products_supplied, last_delivery_date, responsible_person, notes):
        """Update a supplier's details."""
        conn = self.connect()
        cursor = conn.cursor()
        current_time = datetime.now(pytz.UTC)
        cursor.execute("""
            UPDATE suppliers
            SET name = ?, phone = ?, email = ?, address = ?, products_supplied = ?, last_delivery_date = ?,
                responsible_person = ?, notes = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE supplier_id = ?
        """, (name, phone, email, address, products_supplied, last_delivery_date, responsible_person, notes, current_time.strftime("%Y-%m-%d %H:%M:%S"), supplier_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('suppliers', 'UPDATE', supplier_id, {
            'supplier_id': supplier_id, 'name': name, 'phone': phone, 'email': email,
            'address': address, 'products_supplied': products_supplied,
            'last_delivery_date': last_delivery_date, 'responsible_person': responsible_person,
            'notes': notes, 'updated_at': current_time.isoformat(),
            'is_synced': False, 'sync_status': 'pending'
        })

    def get_low_stock_drugs(self):
        """Retrieve drugs with low stock."""
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
        current_time = datetime.now(pytz.UTC)
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, created_at, updated_at, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, 0, 'pending')
        """, (username, password_hash, role, current_time.strftime("%Y-%m-%d %H:%M:%S"), current_time.strftime("%Y-%m-%d %H:%M:%S")))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('users', 'INSERT', user_id, {
            'user_id': user_id, 'username': username, 'password_hash': password_hash, 'role': role,
            'created_at': current_time.isoformat(), 'updated_at': current_time.isoformat(),
            'is_synced': False, 'sync_status': 'pending'
        })
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
        current_time = datetime.now(pytz.UTC)
        cursor.execute("""
            UPDATE users SET username = ?, password_hash = ?, role = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE user_id = ?
        """, (username, password_hash, role, current_time.strftime("%Y-%m-%d %H:%M:%S"), user_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('users', 'UPDATE', user_id, {
            'user_id': user_id, 'username': username, 'password_hash': password_hash, 'role': role,
            'updated_at': current_time.isoformat(), 'is_synced': False, 'sync_status': 'pending'
        })

    def delete_user(self, user_id):
        """Delete a user."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        self.queue_sync_operation('users', 'DELETE', user_id, {})

    def get_current_date(self):
        """Get the current date as a string in EAT (East Africa Time)."""
        eat_time = datetime.now(pytz.timezone('Africa/Nairobi'))
        return eat_time.strftime("%Y-%m-%d %H:%M:%S")

    def is_demo_period_active(self):
        """Check if the demo period (7 days) is still active."""
        config = self.load_config()
        first_launch_str = config.get("first_launch_date")
        if not first_launch_str:
            return True  # If no launch date, assume demo is active
        first_launch = datetime.strptime(first_launch_str, "%Y-%m-%d %H:%M:%S")
        first_launch = pytz.timezone('Africa/Nairobi').localize(first_launch)
        current_time = datetime.now(pytz.timezone('Africa/Nairobi'))
        demo_duration = timedelta(days=7)
        return (current_time - first_launch) <= demo_duration

    def is_system_activated(self):
        """Check if the system has been activated."""
        config = self.load_config()
        return config.get("is_activated", "false") == "true"

    def activate_system(self, code):
        """Validate the activation code and activate the system if correct."""
        config = self.load_config()
        if code == config.get("activation_code"):
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
                           ("is_activated", "true"))
            conn.commit()
            conn.close()
            return True
        return False
