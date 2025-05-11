-- Create a role for PowerSync with replication privileges
CREATE ROLE powersync_role WITH REPLICATION BYPASSRLS LOGIN PASSWORD 'myhighlyrandompassword';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO powersync_role;

-- Create a publication for PowerSync
CREATE PUBLICATION powersync FOR ALL TABLES;

-- Create a function to log changes for sync
CREATE OR REPLACE FUNCTION log_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO sync_log (table_name, operation, record_id, data)
    VALUES (TG_TABLE_NAME, TG_OP, NEW.id, row_to_json(NEW));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a sync log table
CREATE TABLE sync_log (
    log_id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    record_id INTEGER,
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add triggers for each table
CREATE TRIGGER sync_users_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION log_change();

CREATE TRIGGER sync_patients_trigger
AFTER INSERT OR UPDATE OR DELETE ON patients
FOR EACH ROW EXECUTE FUNCTION log_change();

CREATE TRIGGER sync_drugs_trigger
AFTER INSERT OR UPDATE OR DELETE ON drugs
FOR EACH ROW EXECUTE FUNCTION log_change();

CREATE TRIGGER sync_prescriptions_trigger
AFTER INSERT OR UPDATE OR DELETE ON prescriptions
FOR EACH ROW EXECUTE FUNCTION log_change();

CREATE TRIGGER sync_sales_trigger
AFTER INSERT OR UPDATE OR DELETE ON sales
FOR EACH ROW EXECUTE FUNCTION log_change();

CREATE TRIGGER sync_sale_items_trigger
AFTER INSERT OR UPDATE OR DELETE ON sale_items
FOR EACH ROW EXECUTE FUNCTION log_change();
