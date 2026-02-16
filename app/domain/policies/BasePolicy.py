from abc import ABC
from app.utils.exceptions.PolicyError import PolicyError
from app.ext import db
import re
from datetime import date, datetime

class BasePolicy(ABC):
    """
    BasePolicy: reusable validation helpers.
    """

    def require_fields(self, data: dict, required_fields: list):
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise PolicyError(f"Missing fields: {', '.join(missing)}")

    def validate_type(self, field_name: str, value, type_):
        if not isinstance(value, type_):
            raise PolicyError(
                f"Field '{field_name}' must be type {type_.__name__}"
            )

    def filter_allowed_fields(self, data: dict, whitelist: list):
        return {k: v for k, v in data.items() if k in whitelist}

    def normalize_strings(self, data: dict):
        return {
            k: (v.strip() if isinstance(v, str) else v)
            for k, v in data.items()
        }

    def create_resource(self, data: dict, *, required: list, allowed: list):
        self.require_fields(data, required)
        normalized = self.normalize_strings(data)
        filtered = self.filter_allowed_fields(normalized, allowed)
        return filtered

    def validate_string(self, value: str, field: str, min_len=1):
        if not isinstance(value, str) or len(value.strip()) < min_len:
            raise PolicyError(f"{field} must be at least {min_len} characters long")
        return value.strip()

    def validate_email_string(self, email: str):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email):
            raise PolicyError("Invalid Email format")
        return email

    def validate_password_string(self, password: str, confirm: str = None, min_len=8):
        if len(password) < min_len:
            raise PolicyError(f"Password must be at least {min_len} characters long")

        if confirm is not None and password != confirm:
            raise PolicyError("Passwords do not match")

        return password

    def update_resource(self, data: dict, *, allowed: list):
        if not data:
            raise PolicyError("No data provided for update")

        normalized = self.normalize_strings(data)
        filtered = self.filter_allowed_fields(normalized, allowed)

        if not filtered:
            raise PolicyError("No valid fields provided for update")

        return filtered

    def validate_numeric_values(
        self,
        value,
        field_name: str = "Amount",
        *,
        allow_zero: bool = False
    ) -> float:
        if value is None:
            raise PolicyError(f"{field_name} is required")

        try:
            amount = float(value)
        except (TypeError, ValueError):
            raise PolicyError(f"{field_name} must be a number")

        if allow_zero:
            if amount < 0:
                raise PolicyError(f"{field_name} cannot be negative")
        else:
            if amount <= 0:
                raise PolicyError(f"{field_name} must be greater than zero")

        return amount

    def validate_id_values(
            self,
            value,
            field_name: str = "ID"
    ) -> int:
        return int(self.validate_numeric_values(value=value, field_name=field_name, allow_zero=False))

    def validate_date_value(
        self,
        value,
        field_name: str = "Date",
        *,
        allow_future: bool = True,
        allow_past: bool = True
    ) -> date:
        if value is None or value == "":
            raise PolicyError(f"{field_name} is required")

        if isinstance(value, datetime):
            parsed_date = value.date()
        elif isinstance(value, date):
            parsed_date = value
        elif isinstance(value, str):
            value = value.strip()

            try:
                parsed_date = date.fromisoformat(value)
            except ValueError:
                try:
                    parsed_date = datetime.fromisoformat(value).date()
                except ValueError:
                    raise PolicyError(
                        f"{field_name} must be a valid date (YYYY-MM-DD)"
                    )
        else:
            raise PolicyError(f"{field_name} must be a valid date")

        today = date.today()

        if not allow_future and parsed_date > today:
            raise PolicyError(f"{field_name} cannot be in the future")

        if not allow_past and parsed_date < today:
            raise PolicyError(f"{field_name} cannot be in the past")

        return parsed_date
