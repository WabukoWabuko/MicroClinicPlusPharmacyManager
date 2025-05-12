-- Seed data for testing MicroClinicPlusPharmacyManager
-- Note: Ensure the schema is applied before running this seed data

-- Users: 15 users (admins and staff)
-- Passwords are hashed versions of "password123" using bcrypt
INSERT INTO users (username, password_hash, role, created_at, updated_at) VALUES
('admin1', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'admin', '2025-01-01 08:00:00', '2025-01-01 08:00:00'),
('staff1', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'staff', '2025-01-01 08:05:00', '2025-01-01 08:05:00'),
('admin2', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'admin', '2025-01-01 08:10:00', '2025-01-01 08:10:00'),
('staff2', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'staff', '2025-01-01 08:15:00', '2025-01-01 08:15:00'),
('admin3', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'admin', '2025-01-01 08:20:00', '2025-01-01 08:20:00'),
('staff3', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'staff', '2025-01-01 08:25:00', '2025-01-01 08:25:00'),
('staff4', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'staff', '2025-01-01 08:30:00', '2025-01-01 08:30:00'),
('staff5', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'staff', '2025-01-01 08:35:00', '2025-01-01 08:35:00'),
('staff6', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'staff', '2025-01-01 08:40:00', '2025-01-01 08:40:00'),
('staff7', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'staff', '2025-01-01 08:45:00', '2025-01-01 08:45:00'),
('staff8', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'staff', '2025-01-01 08:50:00', '2025-01-01 08:50:00'),
('staff9', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'staff', '2025-01-01 08:55:00', '2025-01-01 08:55:00'),
('staff10', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'staff', '2025-01-01 09:00:00', '2025-01-01 09:00:00'),
('admin4', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'admin', '2025-01-01 09:05:00', '2025-01-01 09:05:00'),
('admin5', '$2b$12$z5Y5nJ5tJqW5lK5vU5x5ye5u5i5o5p5a5s5d5f5g5h5j5k5l', 'admin', '2025-01-01 09:10:00', '2025-01-01 09:10:00');

-- Patients: 15 patients with varied details
INSERT INTO patients (first_name, last_name, age, gender, contact, medical_history, registration_date, updated_at) VALUES
('John', 'Doe', 45, 'Male', '0712345678', 'Hypertension', '2025-01-02 09:00:00', '2025-01-02 09:00:00'),
('Mary', 'Jane', 30, 'Female', '0723456789', 'Asthma', '2025-01-02 09:05:00', '2025-01-02 09:05:00'),
('Peter', 'Smith', 60, 'Male', '0734567890', 'Diabetes', '2025-01-02 09:10:00', '2025-01-02 09:10:00'),
('Sarah', 'Wambui', 25, 'Female', '0745678901', 'None', '2025-01-02 09:15:00', '2025-01-02 09:15:00'),
('James', 'Otieno', 50, 'Male', '0756789012', 'Allergies', '2025-01-02 09:20:00', '2025-01-02 09:20:00'),
('Grace', 'Njeri', 35, 'Female', '0767890123', 'Migraines', '2025-01-02 09:25:00', '2025-01-02 09:25:00'),
('Michael', 'Kamau', 70, 'Male', '0778901234', 'Arthritis', '2025-01-02 09:30:00', '2025-01-02 09:30:00'),
('Lucy', 'Muthoni', 40, 'Female', '0789012345', 'Hypothyroidism', '2025-01-02 09:35:00', '2025-01-02 09:35:00'),
('David', 'Kiptoo', 28, 'Male', '0790123456', 'None', '2025-01-02 09:40:00', '2025-01-02 09:40:00'),
('Esther', 'Achieng', 55, 'Female', '0711234567', 'High Cholesterol', '2025-01-02 09:45:00', '2025-01-02 09:45:00'),
('Joseph', 'Mwangi', 65, 'Male', '0722345678', 'Heart Disease', '2025-01-02 09:50:00', '2025-01-02 09:50:00'),
('Faith', 'Kariuki', 22, 'Female', '0733456789', 'None', '2025-01-02 09:55:00', '2025-01-02 09:55:00'),
('Brian', 'Odhiambo', 33, 'Male', '0744567890', 'Asthma', '2025-01-02 10:00:00', '2025-01-02 10:00:00'),
('Ruth', 'Nyambura', 48, 'Female', '0755678901', 'Diabetes', '2025-01-02 10:05:00', '2025-01-02 10:05:00'),
('Samuel', 'Njoroge', 52, 'Male', '0766789012', 'Hypertension', '2025-01-02 10:10:00', '2025-01-02 10:10:00');

-- Drugs: 15 drugs with varied quantities (some low stock)
INSERT INTO drugs (name, quantity, batch_number, expiry_date, price, created_at, updated_at) VALUES
('Paracetamol', 100, 'PARA2025', '2026-12-31', 50.0, '2025-01-03 10:00:00', '2025-01-03 10:00:00'),
('Amoxicillin', 80, 'AMOX2025', '2026-11-30', 150.0, '2025-01-03 10:05:00', '2025-01-03 10:05:00'),
('Ibuprofen', 5, 'IBU2025', '2026-10-31', 80.0, '2025-01-03 10:10:00', '2025-01-03 10:10:00'),
('Metformin', 50, 'MET2025', '2026-09-30', 120.0, '2025-01-03 10:15:00', '2025-01-03 10:15:00'),
('Lisinopril', 3, 'LIS2025', '2026-08-31', 200.0, '2025-01-03 10:20:00', '2025-01-03 10:20:00'),
('Cetirizine', 90, 'CET2025', '2026-07-31', 60.0, '2025-01-03 10:25:00', '2025-01-03 10:25:00'),
('Salbutamol', 20, 'SAL2025', '2026-06-30', 300.0, '2025-01-03 10:30:00', '2025-01-03 10:30:00'),
('Amlodipine', 8, 'AML2025', '2026-05-31', 180.0, '2025-01-03 10:35:00', '2025-01-03 10:35:00'),
('Omeprazole', 70, 'OME2025', '2026-04-30', 90.0, '2025-01-03 10:40:00', '2025-01-03 10:40:00'),
('Levothyroxine', 40, 'LEV2025', '2026-03-31', 110.0, '2025-01-03 10:45:00', '2025-01-03 10:45:00'),
('Atorvastatin', 2, 'ATO2025', '2026-02-28', 250.0, '2025-01-03 10:50:00', '2025-01-03 10:50:00'),
('Ciprofloxacin', 60, 'CIP2025', '2026-01-31', 140.0, '2025-01-03 10:55:00', '2025-01-03 10:55:00'),
('Diazepam', 30, 'DIA2025', '2025-12-31', 100.0, '2025-01-03 11:00:00', '2025-01-03 11:00:00'),
('Hydrochlorothiazide', 7, 'HCT2025', '2025-11-30', 130.0, '2025-01-03 11:05:00', '2025-01-03 11:05:00'),
('Prednisolone', 85, 'PRE2025', '2025-10-31', 70.0, '2025-01-03 11:10:00', '2025-01-03 11:10:00');

-- Suppliers: 15 suppliers with varied details
INSERT INTO suppliers (name, phone, email, address, products_supplied, last_delivery_date, responsible_person, notes, created_at, updated_at) VALUES
('MediCorp', '0711111111', 'contact@medicorp.com', '123 Nairobi Rd', 'Paracetamol, Amoxicillin', '2025-04-01', 'Alice Kim', 'Reliable supplier', '2025-01-04 11:00:00', '2025-01-04 11:00:00'),
('PharmaPlus', '0722222222', 'sales@pharmaplus.com', '456 Mombasa St', 'Ibuprofen, Metformin', '2025-03-15', 'Bob Otieno', 'Fast delivery', '2025-01-04 11:05:00', '2025-01-04 11:05:00'),
('HealthDist', '0733333333', 'info@healthdist.com', '789 Kisumu Ave', 'Lisinopril, Cetirizine', '2025-02-28', 'Clara Wanjiku', 'Good pricing', '2025-01-04 11:10:00', '2025-01-04 11:10:00'),
('BioMed', '0744444444', 'support@biomed.com', '101 Eldoret Ln', 'Salbutamol, Amlodipine', '2025-03-01', 'David Kiptoo', 'Bulk orders', '2025-01-04 11:15:00', '2025-01-04 11:15:00'),
('CureLabs', '0755555555', 'orders@curelabs.com', '202 Nakuru Rd', 'Omeprazole, Levothyroxine', '2025-04-10', 'Emma Njoroge', 'Quality products', '2025-01-04 11:20:00', '2025-01-04 11:20:00'),
('VitalSupply', '0766666666', 'vital@vitalsupply.com', '303 Thika St', 'Atorvastatin, Ciprofloxacin', '2025-03-20', 'Frank Mwangi', 'Flexible terms', '2025-01-04 11:25:00', '2025-01-04 11:25:00'),
('MediSource', '0777777777', 'source@medisource.com', '404 Nyeri Ave', 'Diazepam, Hydrochlorothiazide', '2025-04-05', 'Grace Achieng', 'Good support', '2025-01-04 11:30:00', '2025-01-04 11:30:00'),
('PharmaCore', '0788888888', 'core@pharmacore.com', '505 Meru Rd', 'Prednisolone', '2025-03-25', 'Henry Kamau', 'On-time delivery', '2025-01-04 11:35:00', '2025-01-04 11:35:00'),
('GlobalMed', '0799999999', 'global@globalmed.com', '606 Machakos Ln', 'Paracetamol, Ibuprofen', '2025-04-15', 'Irene Muthoni', 'Wide range', '2025-01-04 11:40:00', '2025-01-04 11:40:00'),
('CarePharm', '0710101010', 'care@carepharm.com', '707 Kitale St', 'Metformin, Lisinopril', '2025-03-30', 'James Odhiambo', 'Competitive prices', '2025-01-04 11:45:00', '2025-01-04 11:45:00'),
('PureMed', '0721212121', 'pure@puremed.com', '808 Kakamega Rd', 'Cetirizine, Salbutamol', '2025-04-20', 'Kelly Nyambura', 'Reliable stock', '2025-01-04 11:50:00', '2025-01-04 11:50:00'),
('LifeDist', '0732323232', 'life@lifedist.com', '909 Kericho Ave', 'Amlodipine, Omeprazole', '2025-04-01', 'Liam Kariuki', 'Good communication', '2025-01-04 11:55:00', '2025-01-04 11:55:00'),
('HealthCore', '0743434343', 'health@healthcore.com', '1010 Bungoma St', 'Levothyroxine, Atorvastatin', '2025-03-10', 'Mary Wambui', 'Prompt service', '2025-01-04 12:00:00', '2025-01-04 12:00:00'),
('PharmaLife', '0754545454', 'pharma@pharmalife.com', '1111 Nanyuki Rd', 'Ciprofloxacin, Diazepam', '2025-04-25', 'Nick Kiptoo', 'High quality', '2025-01-04 12:05:00', '2025-01-04 12:05:00'),
('MediCare', '0765656565', 'medi@medicare.com', '1212 Embu Ln', 'Hydrochlorothiazide, Prednisolone', '2025-03-05', 'Olivia Njeri', 'Excellent service', '2025-01-04 12:10:00', '2025-01-04 12:10:00');

-- Prescriptions: 15 prescriptions linking patients, users, and drugs
INSERT INTO prescriptions (patient_id, user_id, diagnosis, notes, drug_id, dosage, frequency, duration, quantity_prescribed, prescription_date, updated_at) VALUES
(1, 1, 'Fever', 'Rest advised', 1, '500mg', 'Twice daily', '3 days', 6, '2025-01-05 12:00:00', '2025-01-05 12:00:00'),
(2, 2, 'Infection', 'Drink fluids', 2, '250mg', 'Three times daily', '5 days', 15, '2025-01-05 12:05:00', '2025-01-05 12:05:00'),
(3, 3, 'Pain', 'Avoid strain', 3, '400mg', 'Once daily', '4 days', 4, '2025-01-05 12:10:00', '2025-01-05 12:10:00'),
(4, 4, 'Diabetes', 'Monitor sugar', 4, '500mg', 'Twice daily', '30 days', 60, '2025-01-05 12:15:00', '2025-01-05 12:15:00'),
(5, 5, 'Hypertension', 'Reduce salt', 5, '10mg', 'Once daily', '30 days', 30, '2025-01-05 12:20:00', '2025-01-05 12:20:00'),
(6, 6, 'Allergies', 'Avoid dust', 6, '10mg', 'Once daily', '7 days', 7, '2025-01-05 12:25:00', '2025-01-05 12:25:00'),
(7, 7, 'Asthma', 'Use inhaler', 7, '2 puffs', 'As needed', '30 days', 2, '2025-01-05 12:30:00', '2025-01-05 12:30:00'),
(8, 8, 'Hypertension', 'Monitor BP', 8, '5mg', 'Once daily', '30 days', 30, '2025-01-05 12:35:00', '2025-01-05 12:35:00'),
(9, 9, 'GERD', 'Avoid spicy food', 9, '20mg', 'Once daily', '14 days', 14, '2025-01-05 12:40:00', '2025-01-05 12:40:00'),
(10, 10, 'Hypothyroidism', 'Regular checkup', 10, '50mcg', 'Once daily', '30 days', 30, '2025-01-05 12:45:00', '2025-01-05 12:45:00'),
(11, 11, 'High Cholesterol', 'Diet control', 11, '20mg', 'Once daily', '30 days', 30, '2025-01-05 12:50:00', '2025-01-05 12:50:00'),
(12, 12, 'Infection', 'Complete course', 12, '500mg', 'Twice daily', '7 days', 14, '2025-01-05 12:55:00', '2025-01-05 12:55:00'),
(13, 13, 'Anxiety', 'Therapy advised', 13, '5mg', 'As needed', '10 days', 5, '2025-01-05 13:00:00', '2025-01-05 13:00:00'),
(14, 14, 'Hypertension', 'Lifestyle change', 14, '25mg', 'Once daily', '30 days', 30, '2025-01-05 13:05:00', '2025-01-05 13:05:00'),
(15, 15, 'Inflammation', 'Rest advised', 15, '5mg', 'Twice daily', '5 days', 10, '2025-01-05 13:10:00', '2025-01-05 13:10:00');

-- Sales: 15 sales linking patients and users
INSERT INTO sales (patient_id, user_id, total_price, mode_of_payment, sale_date, updated_at) VALUES
(1, 1, 300.0, 'Cash', '2025-01-06 13:00:00', '2025-01-06 13:00:00'),
(2, 2, 450.0, 'Mobile', '2025-01-06 13:05:00', '2025-01-06 13:05:00'),
(3, 3, 240.0, 'Card', '2025-01-06 13:10:00', '2025-01-06 13:10:00'),
(4, 4, 720.0, 'Cash', '2025-01-06 13:15:00', '2025-01-06 13:15:00'),
(5, 5, 600.0, 'Mobile', '2025-01-06 13:20:00', '2025-01-06 13:20:00'),
(6, 6, 180.0, 'Card', '2025-01-06 13:25:00', '2025-01-06 13:25:00'),
(7, 7, 600.0, 'Cash', '2025-01-06 13:30:00', '2025-01-06 13:30:00'),
(8, 8, 540.0, 'Mobile', '2025-01-06 13:35:00', '2025-01-06 13:35:00'),
(9, 9, 270.0, 'Card', '2025-01-06 13:40:00', '2025-01-06 13:40:00'),
(10, 10, 330.0, 'Cash', '2025-01-06 13:45:00', '2025-01-06 13:45:00'),
(11, 11, 750.0, 'Mobile', '2025-01-06 13:50:00', '2025-01-06 13:50:00'),
(12, 12, 420.0, 'Card', '2025-01-06 13:55:00', '2025-01-06 13:55:00'),
(13, 13, 200.0, 'Cash', '2025-01-06 14:00:00', '2025-01-06 14:00:00'),
(14, 14, 390.0, 'Mobile', '2025-01-06 14:05:00', '2025-01-06 14:05:00'),
(15, 15, 210.0, 'Card', '2025-01-06 14:10:00', '2025-01-06 14:10:00');

-- Sale Items: 15 sale items linking sales and drugs
INSERT INTO sale_items (sale_id, drug_id, quantity, price, updated_at) VALUES
(1, 1, 6, 50.0, '2025-01-06 13:00:00'),
(2, 2, 3, 150.0, '2025-01-06 13:05:00'),
(3, 3, 3, 80.0, '2025-01-06 13:10:00'),
(4, 4, 6, 120.0, '2025-01-06 13:15:00'),
(5, 5, 3, 200.0, '2025-01-06 13:20:00'),
(6, 6, 3, 60.0, '2025-01-06 13:25:00'),
(7, 7, 2, 300.0, '2025-01-06 13:30:00'),
(8, 8, 3, 180.0, '2025-01-06 13:35:00'),
(9, 9, 3, 90.0, '2025-01-06 13:40:00'),
(10, 10, 3, 110.0, '2025-01-06 13:45:00'),
(11, 11, 3, 250.0, '2025-01-06 13:50:00'),
(12, 12, 3, 140.0, '2025-01-06 13:55:00'),
(13, 13, 2, 100.0, '2025-01-06 14:00:00'),
(14, 14, 3, 130.0, '2025-01-06 14:05:00'),
(15, 15, 3, 70.0, '2025-01-06 14:10:00');
