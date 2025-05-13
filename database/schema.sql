-- Drop existing tables to ensure a clean schema
DROP TABLE IF EXISTS sale_items;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS drugs;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS sync_queue;

-- Users table: Stores admin and staff accounts
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'staff')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    CONSTRAINT username_not_empty CHECK (TRIM(username) != '')
);

-- Patients table: Stores patient information
CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0 AND age <= 150),
    gender TEXT CHECK (gender IN ('Male', 'Female', 'Other')),
    contact TEXT NOT NULL,
    medical_history TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_synced INTEGER DEFAULT 0,
    sync_status TEXT DEFAULT 'pending' CHECK (sync_status IN ('pending', 'synced', 'failed')),
    CONSTRAINT first_name_not_empty CHECK (TRIM(first_name) != ''),
    CONSTRAINT last_name_not_empty CHECK (TRIM(last_name) != ''),
    CONSTRAINT contact_not_empty CHECK (TRIM(contact) != ''),
    CONSTRAINT contact_format CHECK (contact GLOB '+[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
);

-- Drugs table: Stores inventory details
CREATE TABLE drugs (
    drug_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    batch_number TEXT NOT NULL,
    expiry_date TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_synced INTEGER DEFAULT 0,
    sync_status TEXT DEFAULT 'pending' CHECK (sync_status IN ('pending', 'synced', 'failed')),
    CONSTRAINT name_not_empty CHECK (TRIM(name) != ''),
    CONSTRAINT batch_number_not_empty CHECK (TRIM(batch_number) != ''),
    CONSTRAINT expiry_date_not_empty CHECK (TRIM(expiry_date) != '')
);

-- Suppliers table: Stores supplier information
CREATE TABLE suppliers (
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
    sync_status TEXT DEFAULT 'pending' CHECK (sync_status IN ('pending', 'synced', 'failed')),
    CONSTRAINT name_not_empty CHECK (TRIM(name) != '')
);

-- Prescriptions table: Stores prescription records
CREATE TABLE prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    diagnosis TEXT NOT NULL,
    notes TEXT,
    drug_id INTEGER NOT NULL,
    dosage TEXT NOT NULL,
    frequency TEXT NOT NULL,
    duration TEXT NOT NULL,
    quantity_prescribed INTEGER NOT NULL CHECK (quantity_prescribed > 0),
    prescription_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_synced INTEGER DEFAULT 0,
    sync_status TEXT DEFAULT 'pending' CHECK (sync_status IN ('pending', 'synced', 'failed')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (drug_id) REFERENCES drugs(drug_id) ON DELETE CASCADE,
    CONSTRAINT diagnosis_not_empty CHECK (TRIM(diagnosis) != ''),
    CONSTRAINT dosage_not_empty CHECK (TRIM(dosage) != ''),
    CONSTRAINT frequency_not_empty CHECK (TRIM(frequency) != ''),
    CONSTRAINT duration_not_empty CHECK (TRIM(duration) != '')
);

-- Sales table: Stores sale transactions
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    total_price REAL NOT NULL CHECK (total_price >= 0),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mode_of_payment TEXT NOT NULL CHECK (mode_of_payment IN ('Cash', 'Card', 'Mobile')),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_synced INTEGER DEFAULT 0,
    sync_status TEXT DEFAULT 'pending' CHECK (sync_status IN ('pending', 'synced', 'failed')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    CONSTRAINT mode_of_payment_not_empty CHECK (TRIM(mode_of_payment) != '')
);

-- Sale Items table: Stores individual items in a sale
CREATE TABLE sale_items (
    sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    drug_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price REAL NOT NULL CHECK (price >= 0),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_synced INTEGER DEFAULT 0,
    sync_status TEXT DEFAULT 'pending' CHECK (sync_status IN ('pending', 'synced', 'failed')),
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id) ON DELETE CASCADE,
    FOREIGN KEY (drug_id) REFERENCES drugs(drug_id) ON DELETE CASCADE
);

-- Sync queue table
CREATE TABLE sync_queue (
    queue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'synced', 'failed')),
    CONSTRAINT table_name_not_empty CHECK (TRIM(table_name) != '')
);

-- Indexes for performance
CREATE INDEX idx_patients_contact ON patients(contact);
CREATE INDEX idx_patients_name ON patients(first_name, last_name);
CREATE INDEX idx_patients_updated_at ON patients(updated_at);
CREATE INDEX idx_drugs_name ON drugs(name);
CREATE INDEX idx_drugs_updated_at ON drugs(updated_at);
CREATE INDEX idx_suppliers_name ON suppliers(name);
CREATE INDEX idx_suppliers_updated_at ON suppliers(updated_at);
CREATE INDEX idx_prescriptions_patient_id ON prescriptions(patient_id);
CREATE INDEX idx_prescriptions_drug_id ON prescriptions(drug_id);
CREATE INDEX idx_prescriptions_updated_at ON prescriptions(updated_at);
CREATE INDEX idx_sales_patient_id ON sales(patient_id);
CREATE INDEX idx_sales_sale_date ON sales(sale_date);
CREATE INDEX idx_sales_updated_at ON sales(updated_at);
CREATE INDEX idx_sale_items_sale_id ON sale_items(sale_id);
CREATE INDEX idx_sale_items_updated_at ON sale_items(updated_at);
CREATE INDEX idx_sync_queue_status ON sync_queue(status);
CREATE INDEX idx_sync_queue_created_at ON sync_queue(created_at);
