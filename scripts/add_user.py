import sqlite3
from pathlib import Path
import bcrypt

def add_user(username, password, role):
    db_path = Path("database/clinic.db")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (username, password_hash.decode('utf-8'), role))
            conn.commit()
            print(f"User {username} added successfully.")
        except sqlite3.IntegrityError:
            print(f"Error: Username {username} already exists.")

if __name__ == "__main__":
    # Example: Add a test user
    add_user("admin", "password123", "admin")
