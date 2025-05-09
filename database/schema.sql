CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
);

CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL,
    phone TEXT,
    address TEXT
);

CREATE TABLE prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    prescription_date TEXT DEFAULT (date('now')),
    diagnosis TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE inventory (
    drug_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    batch_number TEXT NOT NULL,
    expiry_date TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE prescription_items (
    prescription_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prescription_id INTEGER NOT NULL,
    drug_id INTEGER NOT NULL,
    dosage_instructions TEXT NOT NULL,
    quantity_prescribed INTEGER NOT NULL,
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id),
    FOREIGN KEY (drug_id) REFERENCES inventory(drug_id)
);

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    sale_date TEXT DEFAULT (date('now')),
    total_price REAL NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE sale_items (
    sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    drug_id INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
    FOREIGN KEY (drug_id) REFERENCES inventory(drug_id)
);

-- Insert a default admin user
INSERT INTO users (username, password_hash, role)
VALUES ('admin', '$2b$12$3X8G8k3z3Q9z2g5r7q8w9u8z7y6x5w4v3u2t1r0q9p8o7n6m5k4j3', 'admin');
