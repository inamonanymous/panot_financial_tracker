"""Email validation utilities"""
import re

def validate_email(email: str) -> str:
    if not isinstance(email, str):
        raise ValueError("email must be a string")
    e = email.strip()
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, e):
        raise ValueError("Invalid email format")
    return e
