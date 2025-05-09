import re
from datetime import datetime

def is_valid_phone(phone):
    """Validate phone number (e.g., +254 or 10 digits)."""
    if not phone:
        return False, "Phone number is required."
    pattern = r"^\+?\d{10}$"
    if not re.match(pattern, phone):
        return False, "Phone number must be 10 digits or start with + (e.g., +254700123456)."
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
