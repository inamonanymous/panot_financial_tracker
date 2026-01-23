from abc import ABC
from app.utils.exceptions.PolicyError import PolicyError
from app.ext import db
import re

class BasePolicy(ABC):
    """
    BaseService gives you reusable tools for:
    - safe error handling
    - validating input data
    - filtering/cleaning request data
    - preparing data before inserting into the database

    Every Service class in your app should inherit from BaseService.
    """

    # ==============================================================
    # 2. VALIDATION HELPERS
    # ==============================================================

    def require_fields(self, data: dict, required_fields: list):
        """
        Ensures the incoming data contains ALL required fields.

        Example:
            required_fields = ["name", "email"]

            If data = {"name": "John"} -> ERROR
        """
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise PolicyError(f"Missing fields: {', '.join(missing)}")

    def validate_type(self, field_name: str, value, type_):
        """
        Ensures a field has the correct type.

        Example:
            validate_type("age", 25, int)  -> OK
            validate_type("age", "25", int) -> ERROR
        """
        if not isinstance(value, type_):
            raise PolicyError(
                f"Field '{field_name}' must be type {type_.__name__}"
            )

    # ==============================================================
    # 3. FILTERING ALLOWED FIELDS
    # ==============================================================

    def filter_allowed_fields(self, data: dict, whitelist: list):
        """
        ONLY keeps the allowed fields and removes everything else.
        
        Why:
        - Prevents users from sending unwanted data
        - Protects your database models
        - Prevents accidental overwrites

        Example:
            whitelist = ["name", "email"]
            data = {"name": "John", "email": "a@b.com", "role": "admin"}

            Result -> {"name": "John", "email": "a@b.com"}
        """
        return {k: v for k, v in data.items() if k in whitelist}

    # ==============================================================
    # 4. NORMALIZE STRING FIELDS
    # ==============================================================

    def normalize_strings(self, data: dict):
        """
        Automatically strips whitespace for all string fields.

        Example:
            " John  " -> "John"

        This runs on every input to keep the database neat.
        """
        return {
            k: (v.strip() if isinstance(v, str) else v)
            for k, v in data.items()
        }

    def create_resource(self, data: dict, *, required: list, allowed: list):
        """
        This is your MAIN INPUT CLEANER.
        You will use this for every POST / CREATE request.

        PROCESS:
        1. Check if required fields exist
        2. Clean string data (strip spaces)
        3. Remove unwanted fields
        4. Return cleaned data ready for model use

        Example usage inside a service:
            clean = self.create_resource(
                data,
                required=["name", "type"],
                allowed=["name", "type", "user_id"]
            )
        """

        # Step 1: Required fields check
        self.require_fields(data, required)

        # Step 2: Normalize string fields
        normalized = self.normalize_strings(data)

        # Step 3: Keep only allowed fields
        filtered = self.filter_allowed_fields(normalized, allowed)

        # Step 4: Return the clean data
        return filtered


    # ---------------------------
    # 6. VALIDATE STRING FIELD
    # ---------------------------
    def validate_string(self, value: str, field: str, min_len=1):
        if not isinstance(value, str) or len(value.strip()) < min_len:
            raise PolicyError(f"{field} must be at least {min_len} characters long")
        return value.strip()

    # ---------------------------
    # 7. EMAIL REGEX VALIDATION
    # ---------------------------
    def validate_email_string(self, email: str):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email):
            raise PolicyError("Invalid Email format")
        return email

    # ---------------------------
    # 8. PASSWORD VALIDATION
    # ---------------------------
    def validate_password_string(self, password: str, confirm: str = None, min_len=8):
        if len(password) < min_len:
            raise PolicyError(f"Password must be at least {min_len} characters long")

        if confirm is not None and password != confirm:
            raise PolicyError("Passwords do not match")

        return password

    # ---------------------------
    # 9. UPDATE RESOURCE CLEANER
    # ---------------------------
    def update_resource(self, data: dict, *, allowed: list):
        """
        INPUT CLEANER FOR UPDATE / EDIT REQUESTS

        PROCESS:
        1. Normalize string fields
        2. Remove unwanted fields
        3. Ensure at least one valid field is being updated
        """

        if not data:
            raise PolicyError("No data provided for update")

        normalized = self.normalize_strings(data)
        filtered = self.filter_allowed_fields(normalized, allowed)

        if not filtered:
            raise PolicyError("No valid fields provided for update")

        return filtered
