-- Creating Users table for optional login functionality
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'staff', 'pharmacist')),
    full_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creating Patients table
CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    gender TEXT CHECK(gender IN ('M', 'F', 'Other')),
    phone TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creating Inventory (Drugs) table
CREATE TABLE inventory (
    drug_id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_name TEXT NOT NULL,
    generic_name TEXT,
    batch_number TEXT NOT NULL,
    expiry_date DATE NOT NULL,
    quantity_in_stock INTEGER NOT NULL CHECK(quantity_in_stock >= 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    supplier TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creating Prescriptions table
CREATE TABLE prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    prescription_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    diagnosis TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- Creating Prescription Items table (links prescriptions to drugs)
CREATE TABLE prescription_items (
    prescription_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prescription_id INTEGER NOT NULL,
    drug_id INTEGER NOT NULL,
    dosage_instructions TEXT NOT NULL,
    quantity_prescribed INTEGER NOT NULL CHECK(quantity_prescribed > 0),
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id) ON DELETE CASCADE,
    FOREIGN KEY (drug_id) REFERENCES inventory(drug_id) ON DELETE RESTRICT
);

-- Creating Sales table
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    user_id INTEGER NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL CHECK(total_amount >= 0),
    payment_method TEXT CHECK(payment_method IN ('Cash', 'Card', 'Mobile', 'Insurance')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- Creating Sale Items table (links sales to drugs)
CREATE TABLE sale_items (
    sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    drug_id INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL CHECK(quantity_sold > 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    subtotal REAL NOT NULL CHECK(subtotal >= 0),
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id) ON DELETE CASCADE,
    FOREIGN KEY (drug_id) REFERENCES inventory(drug_id) ON DELETE RESTRICT
);

-- Creating Config/Settings table
CREATE TABLE config (
    config_id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_name TEXT NOT NULL UNIQUE,
    setting_value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creating index for faster queries
CREATE INDEX idx_patient_name ON patients(first_name, last_name);
CREATE INDEX idx_drug_name ON inventory(drug_name);
CREATE INDEX idx_sale_date ON sales(sale_date);
CREATE INDEX idx_prescription_date ON prescriptions(prescription_date);
