"""String validation utilities"""
from datetime import datetime


def validate_string(value, field_name: str, min_len: int = 1) -> str:
    if value is None:
        raise ValueError(f"{field_name} is required")
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    v = value.strip()
    if len(v) < min_len:
        raise ValueError(f"{field_name} must be at least {min_len} characters long")
    return v

def normalize_strings(data: dict) -> dict:
    return {k: (v.strip() if isinstance(v, str) else v) for k, v in data.items()}
