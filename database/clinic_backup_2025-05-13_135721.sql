PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'staff')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
INSERT INTO users VALUES(1,'admin1','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','admin','2025-01-01 08:00:00','2025-01-01 08:00:00',NULL);
INSERT INTO users VALUES(2,'staff1','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','staff','2025-01-01 08:05:00','2025-01-01 08:05:00',NULL);
INSERT INTO users VALUES(3,'admin2','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','admin','2025-01-01 08:10:00','2025-01-01 08:10:00',NULL);
INSERT INTO users VALUES(4,'staff2','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','staff','2025-01-01 08:15:00','2025-01-01 08:15:00',NULL);
INSERT INTO users VALUES(5,'admin3','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','admin','2025-01-01 08:20:00','2025-01-01 08:20:00',NULL);
INSERT INTO users VALUES(6,'staff3','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','staff','2025-01-01 08:25:00','2025-01-01 08:25:00',NULL);
INSERT INTO users VALUES(7,'staff4','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','staff','2025-01-01 08:30:00','2025-01-01 08:30:00',NULL);
INSERT INTO users VALUES(8,'staff5','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','staff','2025-01-01 08:35:00','2025-01-01 08:35:00',NULL);
INSERT INTO users VALUES(9,'staff6','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','staff','2025-01-01 08:40:00','2025-01-01 08:40:00',NULL);
INSERT INTO users VALUES(10,'staff7','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','staff','2025-01-01 08:45:00','2025-01-01 08:45:00',NULL);
INSERT INTO users VALUES(11,'staff8','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','staff','2025-01-01 08:50:00','2025-01-01 08:50:00',NULL);
INSERT INTO users VALUES(12,'staff9','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','staff','2025-01-01 08:55:00','2025-01-01 08:55:00',NULL);
INSERT INTO users VALUES(13,'staff10','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','staff','2025-01-01 09:00:00','2025-01-01 09:00:00',NULL);
INSERT INTO users VALUES(14,'admin4','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','admin','2025-01-01 09:05:00','2025-01-01 09:05:00',NULL);
INSERT INTO users VALUES(15,'admin5','$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l','admin','2025-01-01 09:10:00','2025-01-01 09:10:00',NULL);
INSERT INTO users VALUES(16,'admin','$2b$12$.Q4n/nmnPG0J3HIfUCUEIOA/hysqHU8RvxGkVrn1e2HkvNur4dkQ.','admin','2025-05-12 20:53:21','2025-05-12 20:53:21',NULL);
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
    sync_status TEXT DEFAULT 'pending'
);
INSERT INTO patients VALUES(1,'John','Doe',45,'Male','0712345678','Hypertension','2025-01-02 09:00:00','2025-01-02 09:00:00',0,'pending');
INSERT INTO patients VALUES(2,'Mary','Jane',30,'Female','0723456789','Asthma','2025-01-02 09:05:00','2025-01-02 09:05:00',0,'pending');
INSERT INTO patients VALUES(3,'Peter','Smith',60,'Male','0734567890','Diabetes','2025-01-02 09:10:00','2025-01-02 09:10:00',0,'pending');
INSERT INTO patients VALUES(4,'Sarah','Wambui',25,'Female','0745678901','None','2025-01-02 09:15:00','2025-01-02 09:15:00',0,'pending');
INSERT INTO patients VALUES(5,'James','Otieno',50,'Male','0756789012','Allergies','2025-01-02 09:20:00','2025-01-02 09:20:00',0,'pending');
INSERT INTO patients VALUES(6,'Grace','Njeri',35,'Female','0767890123','Migraines','2025-01-02 09:25:00','2025-01-02 09:25:00',0,'pending');
INSERT INTO patients VALUES(7,'Michael','Kamau',70,'Male','0778901234','Arthritis','2025-01-02 09:30:00','2025-01-02 09:30:00',0,'pending');
INSERT INTO patients VALUES(8,'Lucy','Muthoni',40,'Female','0789012345','Hypothyroidism','2025-01-02 09:35:00','2025-01-02 09:35:00',0,'pending');
INSERT INTO patients VALUES(9,'David','Kiptoo',28,'Male','0790123456','None','2025-01-02 09:40:00','2025-01-02 09:40:00',0,'pending');
INSERT INTO patients VALUES(10,'Esther','Achieng',55,'Female','0711234567','High Cholesterol','2025-01-02 09:45:00','2025-01-02 09:45:00',0,'pending');
INSERT INTO patients VALUES(11,'Joseph','Mwangi',65,'Male','0722345678','Heart Disease','2025-01-02 09:50:00','2025-01-02 09:50:00',0,'pending');
INSERT INTO patients VALUES(12,'Faith','Kariuki',22,'Female','0733456789','None','2025-01-02 09:55:00','2025-01-02 09:55:00',0,'pending');
INSERT INTO patients VALUES(13,'Brian','Odhiambo',33,'Male','0744567890','Asthma','2025-01-02 10:00:00','2025-01-02 10:00:00',0,'pending');
INSERT INTO patients VALUES(14,'Ruth','Nyambura',48,'Female','0755678901','Diabetes','2025-01-02 10:05:00','2025-01-02 10:05:00',0,'pending');
INSERT INTO patients VALUES(15,'Samuel','Njoroge',52,'Male','0766789012','Hypertension','2025-01-02 10:10:00','2025-01-02 10:10:00',0,'pending');
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
    sync_status TEXT DEFAULT 'pending'
);
INSERT INTO drugs VALUES(1,'Paracetamol',100,'PARA2025','2026-12-31',50.0,'2025-01-03 10:00:00','2025-01-03 10:00:00',0,'pending');
INSERT INTO drugs VALUES(2,'Amoxicillin',80,'AMOX2025','2026-11-30',150.0,'2025-01-03 10:05:00','2025-01-03 10:05:00',0,'pending');
INSERT INTO drugs VALUES(3,'Ibuprofen',0,'IBU2025','2026-10-31',80.0,'2025-01-03 10:10:00','2025-05-13 10:00:06.698309',0,'pending');
INSERT INTO drugs VALUES(4,'Metformin',0,'MET2025','2026-09-30',120.0,'2025-01-03 10:15:00','2025-05-13 10:32:55.501209',0,'pending');
INSERT INTO drugs VALUES(5,'Lisinopril',0,'LIS2025','2026-08-31',200.0,'2025-01-03 10:20:00','2025-05-13 09:49:19.905376',0,'pending');
INSERT INTO drugs VALUES(6,'Cetirizine',81,'CET2025','2026-07-31',60.0,'2025-01-03 10:25:00','2025-05-13T12:40:43.258136',0,'pending');
INSERT INTO drugs VALUES(7,'Salbutamol',0,'SAL2025','2026-06-30',300.0,'2025-01-03 10:30:00','2025-05-13 10:22:26.058526',0,'pending');
INSERT INTO drugs VALUES(8,'Amlodipine',7,'AML2025','2026-05-31',180.0,'2025-01-03 10:35:00','2025-05-13T11:13:06.360510',0,'pending');
INSERT INTO drugs VALUES(9,'Omeprazole',0,'OME2025','2026-04-30',90.0,'2025-01-03 10:40:00','2025-05-13 10:57:41.931072',0,'pending');
INSERT INTO drugs VALUES(10,'Levothyroxine',0,'LEV2025','2026-03-31',110.0,'2025-01-03 10:45:00','2025-05-13 10:09:38.367136',0,'pending');
INSERT INTO drugs VALUES(11,'Atorvastatin',0,'ATO2025','2026-02-28',250.0,'2025-01-03 10:50:00','2025-05-13 09:29:14.357307',0,'pending');
INSERT INTO drugs VALUES(12,'Ciprofloxacin',0,'CIP2025','2026-01-31',140.0,'2025-01-03 10:55:00','2025-05-13 10:52:13.832810',0,'pending');
INSERT INTO drugs VALUES(13,'Diazepam',0,'DIA2025','2025-12-31',100.0,'2025-01-03 11:00:00','2025-05-13 10:18:51.819744',0,'pending');
INSERT INTO drugs VALUES(14,'Hydrochlorothiazide',0,'HCT2025','2025-11-30',130.0,'2025-01-03 11:05:00','2025-05-13 08:58:25.962132',0,'pending');
INSERT INTO drugs VALUES(15,'Prednisolone',0,'PRE2025','2025-10-31',70.0,'2025-01-03 11:10:00','2025-05-13T11:07:45.239692',0,'pending');
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
    sync_status TEXT DEFAULT 'pending'
);
INSERT INTO suppliers VALUES(1,'MediCorp','0711111111','contact@medicorp.com','123 Nairobi Rd','Paracetamol, Amoxicillin','2025-04-01','Alice Kim','Reliable supplier','2025-01-04 11:00:00','2025-01-04 11:00:00',0,'pending');
INSERT INTO suppliers VALUES(2,'PharmaPlus','0722222222','sales@pharmaplus.com','456 Mombasa St','Ibuprofen, Metformin','2025-03-15','Bob Otieno','Fast delivery','2025-01-04 11:05:00','2025-01-04 11:05:00',0,'pending');
INSERT INTO suppliers VALUES(3,'HealthDist','0733333333','info@healthdist.com','789 Kisumu Ave','Lisinopril, Cetirizine','2025-02-28','Clara Wanjiku','Good pricing','2025-01-04 11:10:00','2025-01-04 11:10:00',0,'pending');
INSERT INTO suppliers VALUES(4,'BioMed','0744444444','support@biomed.com','101 Eldoret Ln','Salbutamol, Amlodipine','2025-03-01','David Kiptoo','Bulk orders','2025-01-04 11:15:00','2025-01-04 11:15:00',0,'pending');
INSERT INTO suppliers VALUES(5,'CureLabs','0755555555','orders@curelabs.com','202 Nakuru Rd','Omeprazole, Levothyroxine','2025-04-10','Emma Njoroge','Quality products','2025-01-04 11:20:00','2025-01-04 11:20:00',0,'pending');
INSERT INTO suppliers VALUES(6,'VitalSupply','0766666666','vital@vitalsupply.com','303 Thika St','Atorvastatin, Ciprofloxacin','2025-03-20','Frank Mwangi','Flexible terms','2025-01-04 11:25:00','2025-01-04 11:25:00',0,'pending');
INSERT INTO suppliers VALUES(7,'MediSource','0777777777','source@medisource.com','404 Nyeri Ave','Diazepam, Hydrochlorothiazide','2025-04-05','Grace Achieng','Good support','2025-01-04 11:30:00','2025-01-04 11:30:00',0,'pending');
INSERT INTO suppliers VALUES(8,'PharmaCore','0788888888','core@pharmacore.com','505 Meru Rd','Prednisolone','2025-03-25','Henry Kamau','On-time delivery','2025-01-04 11:35:00','2025-01-04 11:35:00',0,'pending');
INSERT INTO suppliers VALUES(9,'GlobalMed','0799999999','global@globalmed.com','606 Machakos Ln','Paracetamol, Ibuprofen','2025-04-15','Irene Muthoni','Wide range','2025-01-04 11:40:00','2025-01-04 11:40:00',0,'pending');
INSERT INTO suppliers VALUES(10,'CarePharm','0710101010','care@carepharm.com','707 Kitale St','Metformin, Lisinopril','2025-03-30','James Odhiambo','Competitive prices','2025-01-04 11:45:00','2025-01-04 11:45:00',0,'pending');
INSERT INTO suppliers VALUES(11,'PureMed','0721212121','pure@puremed.com','808 Kakamega Rd','Cetirizine, Salbutamol','2025-04-20','Kelly Nyambura','Reliable stock','2025-01-04 11:50:00','2025-01-04 11:50:00',0,'pending');
INSERT INTO suppliers VALUES(12,'LifeDist','0732323232','life@lifedist.com','909 Kericho Ave','Amlodipine, Omeprazole','2025-04-01','Liam Kariuki','Good communication','2025-01-04 11:55:00','2025-01-04 11:55:00',0,'pending');
INSERT INTO suppliers VALUES(13,'HealthCore','0743434343','health@healthcore.com','1010 Bungoma St','Levothyroxine, Atorvastatin','2025-03-10','Mary Wambui','Prompt service','2025-01-04 12:00:00','2025-01-04 12:00:00',0,'pending');
INSERT INTO suppliers VALUES(14,'PharmaLife','0754545454','pharma@pharmalife.com','1111 Nanyuki Rd','Ciprofloxacin, Diazepam','2025-04-25','Nick Kiptoo','High quality','2025-01-04 12:05:00','2025-01-04 12:05:00',0,'pending');
INSERT INTO suppliers VALUES(15,'MediCare','0765656565','medi@medicare.com','1212 Embu Ln','Hydrochlorothiazide, Prednisolone','2025-03-05','Olivia Njeri','Excellent service','2025-01-04 12:10:00','2025-01-04 12:10:00',0,'pending');
INSERT INTO suppliers VALUES(16,'ade','+254867921385','jesnbjew@gmail.com','Kisumu','Nothing','2025-05-13','ehqbvhw qecbiue','ecbrje vazswberh azisvlcnkjrd','2025-05-13 07:12:34','2025-05-13 07:12:34',0,'pending');
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
    is_synced INTEGER DEFAULT 0,
    sync_status TEXT DEFAULT 'pending',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (drug_id) REFERENCES drugs(drug_id) ON DELETE CASCADE
);
INSERT INTO prescriptions VALUES(1,8,16,'I don''t know','Take after meal',14,'500mg','1 x 3','5 days',7,'2025-05-13 05:58:27',0,'pending');
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    total_price REAL NOT NULL CHECK (total_price >= 0),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mode_of_payment TEXT NOT NULL CHECK (mode_of_payment IN ('Cash', 'Card', 'Mobile')),
    is_synced INTEGER DEFAULT 0,
    sync_status TEXT DEFAULT 'pending',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);
INSERT INTO sales VALUES(1,8,16,1260.0,'2025-05-13 06:19:37','Cash',0,'pending');
INSERT INTO sales VALUES(2,13,16,180.0,'2025-05-13 06:27:41','Cash',0,'pending');
INSERT INTO sales VALUES(3,6,16,500.0,'2025-05-13 06:29:13','Mobile',0,'pending');
INSERT INTO sales VALUES(4,1,16,1550.0,'2025-05-13 06:47:20','Cash',0,'pending');
INSERT INTO sales VALUES(5,9,16,600.0,'2025-05-13 06:49:12','Mobile',0,'pending');
INSERT INTO sales VALUES(6,12,16,400.0,'2025-05-13 07:00:00','Card',0,'pending');
INSERT INTO sales VALUES(7,11,16,660.0,'2025-05-13 07:09:52','Cash',0,'pending');
INSERT INTO sales VALUES(8,15,16,2000.0,'2025-05-13 07:19:00','Cash',0,'pending');
INSERT INTO sales VALUES(9,4,16,6000.0,'2025-05-13 07:22:42','Cash',0,'pending');
INSERT INTO sales VALUES(10,10,16,6000.0,'2025-05-13 07:33:19','Card',0,'pending');
INSERT INTO sales VALUES(11,2,16,7840.0,'2025-05-13 07:52:30','Cash',0,'pending');
INSERT INTO sales VALUES(12,12,16,6300.0,'2025-05-13 07:57:54','Cash',0,'pending');
INSERT INTO sales VALUES(13,3,16,5950.0,'2025-05-13 08:07:56','Cash',0,'pending');
CREATE TABLE sale_items (
    sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    drug_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price REAL NOT NULL CHECK (price >= 0),
    is_synced INTEGER DEFAULT 0,
    sync_status TEXT DEFAULT 'pending',
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id) ON DELETE CASCADE,
    FOREIGN KEY (drug_id) REFERENCES drugs(drug_id) ON DELETE CASCADE
);
INSERT INTO sale_items VALUES(1,1,8,7,1260.0,0,'pending');
INSERT INTO sale_items VALUES(2,2,8,1,180.0,0,'pending');
INSERT INTO sale_items VALUES(3,3,11,2,500.0,0,'pending');
INSERT INTO sale_items VALUES(4,4,13,5,500.0,0,'pending');
INSERT INTO sale_items VALUES(5,4,10,7,770.0,0,'pending');
INSERT INTO sale_items VALUES(6,4,12,2,280.0,0,'pending');
INSERT INTO sale_items VALUES(7,5,5,3,600.0,0,'pending');
INSERT INTO sale_items VALUES(8,6,3,5,400.0,0,'pending');
INSERT INTO sale_items VALUES(9,13,15,85,5950.0,0,'pending');
CREATE TABLE sync_queue (
    queue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending'
);
INSERT INTO sync_queue VALUES(1,'drugs','UPDATE',14,'{"drug_id": 14, "quantity": 0, "updated_at": "2025-05-13T08:58:26.541638", "is_synced": false, "sync_status": "pending"}','2025-05-13 05:58:26','pending');
INSERT INTO sync_queue VALUES(2,'prescriptions','INSERT',1,'{"prescription_id": 1, "patient_id": 8, "user_id": 16, "diagnosis": "I don''t know", "notes": "Take after meal", "drug_id": 14, "dosage": "500mg", "frequency": "1 x 3", "duration": "5 days", "quantity_prescribed": 7, "prescription_date": "2025-05-13T08:58:27.730098", "updated_at": "2025-05-13T08:58:27.730139", "is_synced": false, "sync_status": "pending"}','2025-05-13 05:58:27','pending');
INSERT INTO sync_queue VALUES(3,'sales','INSERT',1,'{"sale_id": 1, "patient_id": 8, "user_id": 16, "total_price": 1260.0, "mode_of_payment": "Cash", "sale_date": "2025-05-13T09:19:38.401117", "updated_at": "2025-05-13T09:19:38.401158", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:19:38','pending');
INSERT INTO sync_queue VALUES(4,'drugs','UPDATE',8,'{"drug_id": 8, "quantity": 1, "updated_at": "2025-05-13T09:19:39.859182", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:19:39','pending');
INSERT INTO sync_queue VALUES(5,'sale_items','INSERT',1,'{"sale_item_id": 1, "sale_id": 1, "drug_id": 8, "quantity": 7, "price": 1260.0, "updated_at": "2025-05-13T09:19:41.548552", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:19:41','pending');
INSERT INTO sync_queue VALUES(6,'sales','INSERT',2,'{"sale_id": 2, "patient_id": 13, "user_id": 16, "total_price": 180.0, "mode_of_payment": "Cash", "sale_date": "2025-05-13T09:27:41.806280", "updated_at": "2025-05-13T09:27:41.806322", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:27:41','pending');
INSERT INTO sync_queue VALUES(7,'drugs','UPDATE',8,'{"drug_id": 8, "quantity": 0, "updated_at": "2025-05-13T09:27:42.983797", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:27:42','pending');
INSERT INTO sync_queue VALUES(8,'sale_items','INSERT',2,'{"sale_item_id": 2, "sale_id": 2, "drug_id": 8, "quantity": 1, "price": 180.0, "updated_at": "2025-05-13T09:27:44.161297", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:27:44','pending');
INSERT INTO sync_queue VALUES(9,'sales','INSERT',3,'{"sale_id": 3, "patient_id": 6, "user_id": 16, "total_price": 500.0, "mode_of_payment": "Mobile", "sale_date": "2025-05-13T09:29:13.795018", "updated_at": "2025-05-13T09:29:13.795060", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:29:13','pending');
INSERT INTO sync_queue VALUES(10,'drugs','UPDATE',11,'{"drug_id": 11, "quantity": 0, "updated_at": "2025-05-13T09:29:14.917413", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:29:14','pending');
INSERT INTO sync_queue VALUES(11,'sale_items','INSERT',3,'{"sale_item_id": 3, "sale_id": 3, "drug_id": 11, "quantity": 2, "price": 500.0, "updated_at": "2025-05-13T09:29:16.061921", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:29:16','pending');
INSERT INTO sync_queue VALUES(12,'sales','INSERT',4,'{"sale_id": 4, "patient_id": 1, "user_id": 16, "total_price": 1550.0, "mode_of_payment": "Cash", "sale_date": "2025-05-13T09:47:21.416008", "updated_at": "2025-05-13T09:47:21.416051", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:47:21','pending');
INSERT INTO sync_queue VALUES(13,'drugs','UPDATE',13,'{"drug_id": 13, "quantity": 25, "updated_at": "2025-05-13T09:47:22.604500", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:47:22','pending');
INSERT INTO sync_queue VALUES(14,'sale_items','INSERT',4,'{"sale_item_id": 4, "sale_id": 4, "drug_id": 13, "quantity": 5, "price": 500.0, "updated_at": "2025-05-13T09:47:23.782009", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:47:23','pending');
INSERT INTO sync_queue VALUES(15,'drugs','UPDATE',13,'{"drug_id": 13, "quantity": 20, "updated_at": "2025-05-13T09:47:24.882445", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:47:24','pending');
INSERT INTO sync_queue VALUES(16,'drugs','UPDATE',10,'{"drug_id": 10, "quantity": 33, "updated_at": "2025-05-13T09:47:26.060010", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:47:26','pending');
INSERT INTO sync_queue VALUES(17,'sale_items','INSERT',5,'{"sale_item_id": 5, "sale_id": 4, "drug_id": 10, "quantity": 7, "price": 770.0, "updated_at": "2025-05-13T09:47:27.204488", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:47:27','pending');
INSERT INTO sync_queue VALUES(18,'drugs','UPDATE',10,'{"drug_id": 10, "quantity": 26, "updated_at": "2025-05-13T09:47:28.359999", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:47:28','pending');
INSERT INTO sync_queue VALUES(19,'drugs','UPDATE',12,'{"drug_id": 12, "quantity": 58, "updated_at": "2025-05-13T09:47:29.493476", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:47:29','pending');
INSERT INTO sync_queue VALUES(20,'sale_items','INSERT',6,'{"sale_item_id": 6, "sale_id": 4, "drug_id": 12, "quantity": 2, "price": 280.0, "updated_at": "2025-05-13T09:47:30.704010", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:47:30','pending');
INSERT INTO sync_queue VALUES(21,'drugs','UPDATE',12,'{"drug_id": 12, "quantity": 56, "updated_at": "2025-05-13T09:47:32.035582", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:47:32','pending');
INSERT INTO sync_queue VALUES(22,'sales','INSERT',5,'{"sale_id": 5, "patient_id": 9, "user_id": 16, "total_price": 600.0, "mode_of_payment": "Mobile", "sale_date": "2025-05-13T09:49:18.440494", "updated_at": "2025-05-13T09:49:18.440537", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:49:18','pending');
INSERT INTO sync_queue VALUES(23,'drugs','UPDATE',5,'{"drug_id": 5, "quantity": 0, "updated_at": "2025-05-13T09:49:21.455721", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:49:21','pending');
INSERT INTO sync_queue VALUES(24,'sale_items','INSERT',7,'{"sale_item_id": 7, "sale_id": 5, "drug_id": 5, "quantity": 3, "price": 600.0, "updated_at": "2025-05-13T09:49:24.372042", "is_synced": false, "sync_status": "pending"}','2025-05-13 06:49:24','pending');
INSERT INTO sync_queue VALUES(25,'sales','INSERT',6,'{"sale_id": 6, "patient_id": 12, "user_id": 16, "total_price": 400.0, "mode_of_payment": "Card", "sale_date": "2025-05-13T10:00:05.156450", "updated_at": "2025-05-13T10:00:05.156500", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:00:05','pending');
INSERT INTO sync_queue VALUES(26,'drugs','UPDATE',3,'{"drug_id": 3, "quantity": 0, "updated_at": "2025-05-13T10:00:08.619466", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:00:08','pending');
INSERT INTO sync_queue VALUES(27,'sale_items','INSERT',8,'{"sale_item_id": 8, "sale_id": 6, "drug_id": 3, "quantity": 5, "price": 400.0, "updated_at": "2025-05-13T10:00:11.869318", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:00:11','pending');
INSERT INTO sync_queue VALUES(28,'drugs','UPDATE',10,'{"drug_id": 10, "quantity": 6, "updated_at": "2025-05-13T10:05:45.478323", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:05:45','pending');
INSERT INTO sync_queue VALUES(29,'drugs','UPDATE',10,'{"drug_id": 10, "quantity": 0, "updated_at": "2025-05-13T10:09:39.901669", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:09:39','pending');
INSERT INTO sync_queue VALUES(30,'sales','INSERT',7,'{"sale_id": 7, "patient_id": 11, "user_id": 16, "total_price": 660.0, "mode_of_payment": "Cash", "sale_date": "2025-05-13T10:09:54.229795", "updated_at": "2025-05-13T10:09:54.229835", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:09:54','pending');
INSERT INTO sync_queue VALUES(31,'suppliers','INSERT',16,'{"supplier_id": 16, "name": "ade", "phone": "+254867921385", "email": "jesnbjew@gmail.com", "address": "Kisumu", "products_supplied": "Nothing", "last_delivery_date": "2025-05-13", "responsible_person": "ehqbvhw qecbiue", "notes": "ecbrje vazswberh azisvlcnkjrd", "created_at": "2025-05-13T10:12:36.066162", "updated_at": "2025-05-13T10:12:36.066209", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:12:36','pending');
INSERT INTO sync_queue VALUES(32,'drugs','UPDATE',13,'{"drug_id": 13, "quantity": 0, "updated_at": "2025-05-13T10:18:53.352715", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:18:53','pending');
INSERT INTO sync_queue VALUES(33,'sales','INSERT',8,'{"sale_id": 8, "patient_id": 15, "user_id": 16, "total_price": 2000.0, "mode_of_payment": "Cash", "sale_date": "2025-05-13T10:19:01.639297", "updated_at": "2025-05-13T10:19:01.639337", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:19:01','pending');
INSERT INTO sync_queue VALUES(34,'drugs','UPDATE',7,'{"drug_id": 7, "quantity": 0, "updated_at": "2025-05-13T10:22:27.571411", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:22:27','pending');
INSERT INTO sync_queue VALUES(35,'sales','INSERT',9,'{"sale_id": 9, "patient_id": 4, "user_id": 16, "total_price": 6000.0, "mode_of_payment": "Cash", "sale_date": "2025-05-13T10:22:44.375553", "updated_at": "2025-05-13T10:22:44.375594", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:22:44','pending');
INSERT INTO sync_queue VALUES(36,'drugs','UPDATE',4,'{"drug_id": 4, "quantity": 0, "updated_at": "2025-05-13T10:32:56.900386", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:32:56','pending');
INSERT INTO sync_queue VALUES(37,'sales','INSERT',10,'{"sale_id": 10, "patient_id": 10, "user_id": 16, "total_price": 6000.0, "mode_of_payment": "Card", "sale_date": "2025-05-13T10:33:21.727156", "updated_at": "2025-05-13T10:33:21.727197", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:33:21','pending');
INSERT INTO sync_queue VALUES(38,'drugs','UPDATE',12,'{"drug_id": 12, "quantity": 0, "updated_at": "2025-05-13T10:52:15.206421", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:52:15','pending');
INSERT INTO sync_queue VALUES(39,'sales','INSERT',11,'{"sale_id": 11, "patient_id": 2, "user_id": 16, "total_price": 7840.0, "mode_of_payment": "Cash", "sale_date": "2025-05-13T10:52:32.076703", "updated_at": "2025-05-13T10:52:32.076742", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:52:32','pending');
INSERT INTO sync_queue VALUES(40,'drugs','UPDATE',9,'{"drug_id": 9, "quantity": 0, "updated_at": "2025-05-13T10:57:43.324421", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:57:43','pending');
INSERT INTO sync_queue VALUES(41,'sales','INSERT',12,'{"sale_id": 12, "patient_id": 12, "user_id": 16, "total_price": 6300.0, "mode_of_payment": "Cash", "sale_date": "2025-05-13T10:57:55.627728", "updated_at": "2025-05-13T10:57:55.627769", "is_synced": false, "sync_status": "pending"}','2025-05-13 07:57:55','pending');
INSERT INTO sync_queue VALUES(42,'drugs','UPDATE',15,'{"drug_id": 15, "quantity": 0, "updated_at": "2025-05-13T11:07:46.638538", "is_synced": false, "sync_status": "pending"}','2025-05-13 08:07:46','pending');
INSERT INTO sync_queue VALUES(43,'sales','INSERT',13,'{"sale_id": 13, "patient_id": 3, "user_id": 16, "total_price": 5950.0, "mode_of_payment": "Cash", "sale_date": "2025-05-13T11:07:57.973462", "updated_at": "2025-05-13T11:07:57.973503", "is_synced": false, "sync_status": "pending"}','2025-05-13 08:07:57','pending');
INSERT INTO sync_queue VALUES(44,'sale_items','INSERT',9,'{"sale_item_id": 9, "sale_id": 13, "drug_id": 15, "quantity": 85, "price": 5950.0, "updated_at": "2025-05-13T11:08:01.494999", "is_synced": false, "sync_status": "pending"}','2025-05-13 08:08:01','pending');
INSERT INTO sync_queue VALUES(45,'drugs','UPDATE',8,'{"drug_id": 8, "name": "Amlodipine", "quantity": 7, "batch_number": "AML2025", "expiry_date": "2026-05-31", "price": 180.0, "updated_at": "2025-05-13T11:13:07.900560", "is_synced": false, "sync_status": "pending"}','2025-05-13 08:13:07','pending');
INSERT INTO sync_queue VALUES(46,'drugs','INSERT',16,'{"drug_id": 16, "name": "ased", "quantity": 34, "batch_number": "dszv", "expiry_date": "2026-12-01", "price": 87998.0, "created_at": "2025-05-13T11:13:40.045491", "updated_at": "2025-05-13T11:13:40.045532", "is_synced": false, "sync_status": "pending"}','2025-05-13 08:13:40','pending');
INSERT INTO sync_queue VALUES(47,'drugs','DELETE',16,'{}','2025-05-13 08:13:53','pending');
INSERT INTO sync_queue VALUES(48,'patients','INSERT',16,'{"patient_id": 16, "first_name": "asD", "last_name": "svz", "age": 45, "gender": "Other", "contact": "+25413682792", "medical_history": "wkjnbjk", "registration_date": "2025-05-13T11:14:42.508563", "updated_at": "2025-05-13T11:14:42.508606", "is_synced": false, "sync_status": "pending"}','2025-05-13 08:14:42','pending');
INSERT INTO sync_queue VALUES(49,'patients','UPDATE',16,'{"patient_id": 16, "first_name": "Mbeumo", "last_name": "svz", "age": 45, "gender": "Other", "contact": "+25413682792", "medical_history": "wkjnbjk", "updated_at": "2025-05-13T11:31:07.941034", "is_synced": false, "sync_status": "pending"}','2025-05-13 08:31:07','pending');
INSERT INTO sync_queue VALUES(50,'patients','DELETE',16,'{}','2025-05-13 08:31:23','pending');
INSERT INTO sync_queue VALUES(51,'drugs','UPDATE',6,'{"drug_id": 6, "quantity": 81, "updated_at": "2025-05-13T12:40:43.927689", "is_synced": false, "sync_status": "pending"}','2025-05-13 09:40:43','pending');
INSERT INTO sync_queue VALUES(52,'prescriptions','INSERT',2,'{"prescription_id": 2, "patient_id": 9, "user_id": 16, "diagnosis": "rksnes", "notes": "sdjhmbew vecsukbgew vacbewh", "drug_id": 6, "dosage": "344", "frequency": "3 x 4", "duration": "12 weeks", "quantity_prescribed": 9, "prescription_date": "2025-05-13T12:40:45.039186", "updated_at": "2025-05-13T12:40:45.039226", "is_synced": false, "sync_status": "pending"}','2025-05-13 09:40:45','pending');
INSERT INTO sync_queue VALUES(53,'prescriptions','DELETE',2,'{}','2025-05-13 09:41:29','pending');
INSERT INTO sync_queue VALUES(54,'prescriptions','INSERT',3,'{"patient_id": 10, "user_id": 16, "diagnosis": "dsjnjcks eekjnrej", "notes": "ewjhe zchuew", "drug_id": 12, "dosage": "345", "frequency": "76", "duration": "36", "quantity_prescribed": 90, "prescription_date": "2025-05-13T12:59:38.677052", "is_synced": false, "sync_status": "pending"}','2025-05-13 09:59:38','pending');
INSERT INTO sync_queue VALUES(55,'prescriptions','DELETE',3,'{}','2025-05-13 10:17:03','pending');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('users',16);
INSERT INTO sqlite_sequence VALUES('patients',16);
INSERT INTO sqlite_sequence VALUES('drugs',16);
INSERT INTO sqlite_sequence VALUES('suppliers',16);
INSERT INTO sqlite_sequence VALUES('sync_queue',55);
INSERT INTO sqlite_sequence VALUES('prescriptions',3);
INSERT INTO sqlite_sequence VALUES('sales',13);
INSERT INTO sqlite_sequence VALUES('sale_items',9);
CREATE INDEX idx_patients_contact ON patients(contact);
CREATE INDEX idx_patients_name ON patients(first_name, last_name);
CREATE INDEX idx_drugs_name ON drugs(name);
CREATE INDEX idx_prescriptions_patient_id ON prescriptions(patient_id);
CREATE INDEX idx_prescriptions_drug_id ON prescriptions(drug_id);
CREATE INDEX idx_suppliers_name ON suppliers(name);
CREATE INDEX idx_sales_patient_id ON sales(patient_id);
CREATE INDEX idx_sales_sale_date ON sales(sale_date);
CREATE INDEX idx_sale_items_sale_id ON sale_items(sale_id);
COMMIT;
