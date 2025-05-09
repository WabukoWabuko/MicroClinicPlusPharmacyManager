-- Creating users table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
);

-- Creating patients table
CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL,
    phone TEXT,
    address TEXT
);

-- Creating inventory table
CREATE TABLE inventory (
    drug_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    batch_number TEXT NOT NULL,
    expiry_date TEXT NOT NULL,
    price REAL NOT NULL
);

-- Creating prescriptions table
CREATE TABLE prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    prescription_date TEXT NOT NULL DEFAULT (date('now')),
    diagnosis TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Creating prescription_items table
CREATE TABLE prescription_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prescription_id INTEGER NOT NULL,
    drug_id INTEGER NOT NULL,
    dosage_instructions TEXT NOT NULL,
    quantity_prescribed INTEGER NOT NULL,
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id),
    FOREIGN KEY (drug_id) REFERENCES inventory(drug_id)
);

-- Creating sales table
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    sale_date TEXT NOT NULL DEFAULT (date('now')),
    total_price REAL NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Creating sale_items table
CREATE TABLE sale_items (
    sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    drug_id INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
    FOREIGN KEY (drug_id) REFERENCES inventory(drug_id)
);
