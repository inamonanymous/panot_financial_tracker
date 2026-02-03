"""Date validation utilities"""
from datetime import date, datetime


def validate_date(value, field_name: str = "Date", allow_future: bool = True, allow_past: bool = True) -> date:
    if value is None or value == "":
        raise ValueError(f"{field_name} is required")

    if isinstance(value, datetime):
        parsed = value.date()
    elif isinstance(value, date):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = date.fromisoformat(value.strip())
        except ValueError:
            # try datetime
            try:
                parsed = datetime.fromisoformat(value.strip()).date()
            except ValueError:
                raise ValueError(f"{field_name} must be a valid ISO date (YYYY-MM-DD)")
    else:
        raise ValueError(f"{field_name} must be a date")

    today = date.today()
    if not allow_future and parsed > today:
        raise ValueError(f"{field_name} cannot be in the future")
    if not allow_past and parsed < today:
        raise ValueError(f"{field_name} cannot be in the past")
    return parsed
