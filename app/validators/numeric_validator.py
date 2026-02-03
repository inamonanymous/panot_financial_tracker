"""Numeric validation utilities"""

def validate_numeric(value, field_name: str = "Amount", allow_zero: bool = False) -> float:
    if value is None or value == "":
        raise ValueError(f"{field_name} is required")
    try:
        n = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number")
    if allow_zero:
        if n < 0:
            raise ValueError(f"{field_name} cannot be negative")
    else:
        if n <= 0:
            raise ValueError(f"{field_name} must be greater than zero")
    return n
