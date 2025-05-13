import sqlite3
import bcrypt
import os
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv
import requests
import json
import pytz

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
        conn.commit()
        conn.close()

    def load_config(self):
        """Load settings from config.json."""
        default_config = {
            "clinic_name": "MicroClinic",
            "logo_path": "",
            "background_path": "",
            "tax_rate": 0,
            "contact_details": "",
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
        """Synchronize local database with Supabase."""
        if not self.supabase or not self.sync_enabled:
            return

        # Ensure online
        if not self.is_online():
            print("Offline: Changes will sync when online.")
            return

        print("Starting sync...")

        # Tables to sync
        tables = ["users", "patients", "drugs", "suppliers", "prescriptions", "sales", "sale_items"]

        # Push local changes to Supabase
        self.push_changes(tables)

        # Pull changes from Supabase
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for table in tables:
            print(f"Pulling changes for {table}...")

            # Get the last sync time for comparison
            last_sync = self.last_sync_time or datetime(1970, 1, 1)

            # Fetch remote data modified since last sync
            try:
                response = self.supabase.table(table).select("*").gt("updated_at", last_sync.isoformat()).execute()
                remote_data = response.data
            except Exception as e:
                print(f"Error fetching {table} from Supabase: {e}")
                continue

            # Process each remote record
            for remote_row in remote_data:
                remote_id = remote_row[f"{table[:-1]}_id"]
                remote_updated_at = datetime.fromisoformat(remote_row["updated_at"].replace("Z", "+00:00"))

                # Validate and sanitize data for the 'patients' table
                if table == 'patients':
                    # Ensure 'age' is within the valid range (1 to 150)
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

                    # Validate and sanitize 'contact' field
                    if 'contact' in remote_row:
                        contact = str(remote_row['contact']).strip()
                        # Check if contact matches the pattern: + followed by 3-digit country code and 9 digits
                        import re
                        if not re.match(r'^\+[0-9]{3}[0-9]{9}$', contact):
                            print(f"Warning: Invalid contact ({contact}) for patient_id {remote_id}. Setting to default.")
                            remote_row['contact'] = '+254000000000'  # Default valid contact

                # Check if the record exists locally
                cursor.execute(f"SELECT updated_at, is_synced FROM {table} WHERE {table[:-1]}_id = ?", (remote_id,))
                local_row = cursor.fetchone()

                if local_row:
                    # Record exists, compare timestamps
                    local_updated_at = datetime.strptime(local_row[0], "%Y-%m-%d %H:%M:%S") if local_row[0] else datetime(1970, 1, 1)
                    is_synced = bool(local_row[1])

                    if remote_updated_at > local_updated_at:
                        # Update local record
                        updates = ", ".join([f"{key} = ?" for key in remote_row.keys() if key != f"{table[:-1]}_id"])
                        values = [remote_row[key] for key in remote_row.keys() if key != f"{table[:-1]}_id"] + [remote_id]
                        cursor.execute(f"UPDATE {table} SET {updates} WHERE {table[:-1]}_id = ?", values)
                        print(f"Updated {table[:-1]} with ID {remote_id}")
                else:
                    # Insert new record
                    columns = ", ".join(remote_row.keys())
                    placeholders = ", ".join(["?" for _ in remote_row])
                    values = [remote_row[key] for key in remote_row.keys()]
                    cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
                    print(f"Inserted new {table[:-1]} with ID {remote_id}")

        # Commit changes
        conn.commit()
        conn.close()

        # Update last sync time
        self.last_sync_time = datetime.now()
        self.save_last_sync_time()
        print(f"{self.last_sync_time}")

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
        
    def update_patient(self, patient_id, first_name, last_name, age, gender, contact, medical_history):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE patients SET first_name = ?, last_name = ?, age = ?, gender = ?, contact = ?, medical_history = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE patient_id = ?
        """, (first_name, last_name, age, gender, contact, medical_history, datetime.now().isoformat(), patient_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('patients', 'UPDATE', patient_id, {
            'patient_id': patient_id, 'first_name': first_name, 'last_name': last_name, 'age': age,
            'gender': gender, 'contact': contact, 'medical_history': medical_history,
            'updated_at': datetime.now().isoformat(), 'is_synced': False, 'sync_status': 'pending'
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

    def update_drug(self, drug_id, name, quantity, batch_number, expiry_date, price):
        """Update a drug's details, including name."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE drugs SET name = ?, quantity = ?, batch_number = ?, expiry_date = ?, price = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE drug_id = ?
        """, (name, quantity, batch_number, expiry_date, price, datetime.now().isoformat(), drug_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('drugs', 'UPDATE', drug_id, {
            'drug_id': drug_id, 'name': name, 'quantity': quantity, 'batch_number': batch_number,
            'expiry_date': expiry_date, 'price': price, 'updated_at': datetime.now().isoformat(),
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
        cursor.execute("""
            UPDATE drugs SET quantity = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE drug_id = ?
        """, (new_quantity, datetime.now().isoformat(), drug_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('drugs', 'UPDATE', drug_id, {
            'drug_id': drug_id, 'quantity': new_quantity, 'updated_at': datetime.now().isoformat(),
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
        current_time = datetime.now().isoformat()
        cursor.execute("""
            UPDATE prescriptions SET patient_id = ?, user_id = ?, diagnosis = ?, notes = ?, drug_id = ?, dosage = ?, frequency = ?, duration = ?, quantity_prescribed = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE prescription_id = ?
        """, (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed, current_time, prescription_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('prescriptions', 'UPDATE', prescription_id, {
            'prescription_id': prescription_id, 'patient_id': patient_id, 'user_id': user_id, 'diagnosis': diagnosis,
            'notes': notes, 'drug_id': drug_id, 'dosage': dosage, 'frequency': frequency, 'duration': duration,
            'quantity_prescribed': quantity_prescribed, 'updated_at': current_time,
            'is_synced': False, 'sync_status': 'pending'
        })
        

    def add_prescription(self, patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed):
        conn = self.connect()
        cursor = conn.cursor()
        current_time = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO prescriptions (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed, prescription_date, updated_at, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 'pending')
        """, (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed, current_time, current_time))
        prescription_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('prescriptions', 'INSERT', prescription_id, {
            'prescription_id': prescription_id, 'patient_id': patient_id, 'user_id': user_id, 'diagnosis': diagnosis,
            'notes': notes, 'drug_id': drug_id, 'dosage': dosage, 'frequency': frequency, 'duration': duration,
            'quantity_prescribed': quantity_prescribed, 'prescription_date': current_time,
            'updated_at': current_time, 'is_synced': False, 'sync_status': 'pending'
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
        cursor.execute("""
            INSERT INTO sales (patient_id, user_id, total_price, mode_of_payment, is_synced, sync_status)
            VALUES (?, ?, ?, ?, 0, 'pending')
        """, (patient_id, user_id, total_price, mode_of_payment))
        sale_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('sales', 'INSERT', sale_id, {
            'sale_id': sale_id, 'patient_id': patient_id, 'user_id': user_id,
            'total_price': total_price, 'mode_of_payment': mode_of_payment, 'sale_date': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(), 'is_synced': False, 'sync_status': 'pending'
        })
        return sale_id

    def add_sale_item(self, sale_id, drug_id, quantity, price):
        """Add a sale item to the database without modifying stock."""
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
        cursor.execute("""
            INSERT INTO suppliers (name, phone, email, address, products_supplied, last_delivery_date, responsible_person, notes, is_synced, sync_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 'pending')
        """, (name, phone, email, address, products_supplied, last_delivery_date, responsible_person, notes))
        supplier_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.queue_sync_operation('suppliers', 'INSERT', supplier_id, {
            'supplier_id': supplier_id, 'name': name, 'phone': phone, 'email': email,
            'address': address, 'products_supplied': products_supplied,
            'last_delivery_date': last_delivery_date, 'responsible_person': responsible_person,
            'notes': notes, 'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(), 'is_synced': False, 'sync_status': 'pending'
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
        cursor.execute("""
            UPDATE suppliers
            SET name = ?, phone = ?, email = ?, address = ?, products_supplied = ?, last_delivery_date = ?,
                responsible_person = ?, notes = ?, updated_at = ?, is_synced = 0, sync_status = 'pending'
            WHERE supplier_id = ?
        """, (name, phone, email, address, products_supplied, last_delivery_date, responsible_person, notes, datetime.now().isoformat(), supplier_id))
        conn.commit()
        conn.close()
        self.queue_sync_operation('suppliers', 'UPDATE', supplier_id, {
            'supplier_id': supplier_id, 'name': name, 'phone': phone, 'email': email,
            'address': address, 'products_supplied': products_supplied,
            'last_delivery_date': last_delivery_date, 'responsible_person': responsible_person,
            'notes': notes, 'updated_at': datetime.now().isoformat(),
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
        """, (username, password_hash, role, datetime.now().isoformat(), user_id))
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
        """Get the current date as a string in EAT (East Africa Time)."""
        # EAT is UTC+3
        eat_time = datetime.now() + timedelta(hours=3)
        return eat_time.strftime("%Y-%m-%d %H:%M:%S")
