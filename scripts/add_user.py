import sqlite3
import bcrypt
import os

def init_database():
    """Initialize the database with schema.sql if it doesn't exist."""
    db_path = "database/clinic.db"
    schema_path = "database/schema.sql"
    
    if not os.path.exists(db_path) or not table_exists("users"):
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        conn.commit()
        conn.close()
        print("Database initialized with schema.")

def table_exists(table_name):
    """Check if a table exists in the database."""
    conn = sqlite3.connect("database/clinic.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def add_user(username, password, role):
    """Add a user to the users table with a hashed password."""
    if role not in ('admin', 'staff'):
        print(f"Error: Role must be 'admin' or 'staff', got '{role}'")
        return

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        conn = sqlite3.connect("database/clinic.db")
        cursor = conn.cursor()
        
        # Check for existing username
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"Error: Username '{username}' already exists.")
            return

        # Insert the new user
        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, password_hash, role))
        
        conn.commit()
        print(f"User '{username}' added successfully with role '{role}'.")
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    # Initialize database if needed
    init_database()
    # Example: Add admin user
    #add_user("admin2", "password123", "admin")  # Use 'admin2' to avoid conflict with schema.sql's default admin
    add_user("staff1", "password123", "staff")
