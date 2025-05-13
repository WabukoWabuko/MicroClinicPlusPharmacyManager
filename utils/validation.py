import re
from datetime import datetime

def is_valid_name(name):
    if not name:
        return False, "Name is required."
    if not name.isalpha():
        return False, "Name must contain only letters."
    if len(name) < 2:
        return False, "Name must be at least 2 characters long."
    return True, ""

def is_valid_phone(phone):
    if not phone:
        return False, "Phone number is required."
    # Check format: starts with +, followed by 1-3 digits (country code), then exactly 9 digits
    if not re.match(r'^\+\d{1,3}\d{9}$', phone):
        return False, "Phone number must start with a country code (e.g., +254) followed by exactly 9 digits (total 12 characters including +)."
    # Verify total length is exactly 12 characters
    if len(phone) != 13:
        return False, "Phone number must be exactly 13 characters including the country code (e.g., +254700123456)."
    return True, ""

def is_valid_date(date_str):
    """Validate date in YYYY-MM-DD format."""
    if not date_str:
        return False, "Date is required."
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format."

def is_valid_quantity(quantity):
    """Validate quantity as a positive integer."""
    if not quantity:
        return False, "Quantity is required."
    try:
        qty = int(quantity)
        if qty <= 0:
            return False, "Quantity must be positive."
        return True, ""
    except ValueError:
        return False, "Quantity must be a number."

def is_valid_price(price):
    """Validate price as a non-negative float."""
    if not price:
        return False, "Price is required."
    try:
        pr = float(price)
        if pr < 0:
            return False, "Price cannot be negative."
        return True, ""
    except ValueError:
        return False, "Price must be a number."

def is_valid_name(name):
    """Validate non-empty name."""
    if not name or not name.strip():
        return False, "Name is required."
    return True, ""

def is_valid_password(password):
    """Validate password (min 8 characters)."""
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters."
    return True, ""

def is_valid_username(username):
    """Validate non-empty username."""
    if not username or not username.strip():
        return False, "Username is required."
    return True, ""
