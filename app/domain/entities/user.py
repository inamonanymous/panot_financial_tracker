"""User Domain Entity - Pure business logic, no database access"""
import re
from app.domain.exceptions import InvalidUserError


class User:
    """
    User Domain Entity
    
    Represents a user in the finance tracker system.
    Contains ONLY business logic and validation rules.
    No SQLAlchemy, no database access.
    """
    
    def __init__(self, firstname: str, lastname: str, email: str, password_hash: str = None, id: int = None):
        """
        Initialize a User entity.
        
        Args:
            firstname: User's first name
            lastname: User's last name
            email: User's email address
            password_hash: Hashed password (optional, for persistence)
            id: User ID (optional, assigned by database)
        
        Raises:
            InvalidUserError: If any field violates domain rules
        """
        self.id = id
        self.firstname = self._validate_name(firstname, "firstname")
        self.lastname = self._validate_name(lastname, "lastname")
        self.email = self._validate_email(email)
        self.password_hash = password_hash
        self.current_value = 0.0  # Will be calculated by domain services
    
    @staticmethod
    def _validate_name(name: str, field_name: str) -> str:
        """
        Validate user name (firstname or lastname).
        
        Rules:
        - At least 2 characters
        - Letters and spaces only
        - Single spaces between words
        
        Raises:
            InvalidUserError: If name violates rules
        """
        if not isinstance(name, str):
            raise InvalidUserError(f"{field_name} must be a string")
        
        name = name.strip()
        
        if len(name) < 2:
            raise InvalidUserError(f"{field_name} must be at least 2 characters")
        
        if not re.fullmatch(r"^[A-Za-z]+(?: [A-Za-z]+)*$", name):
            raise InvalidUserError(
                f"{field_name} must contain letters only, with single spaces between words"
            )
        
        return name
    
    @staticmethod
    def _validate_email(email: str) -> str:
        """
        Validate email format.
        
        Raises:
            InvalidUserError: If email is invalid
        """
        if not isinstance(email, str):
            raise InvalidUserError("email must be a string")
        
        email = email.strip()
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        
        if not re.match(pattern, email):
            raise InvalidUserError("email format is invalid")
        
        return email
    
    def set_password_hash(self, password_hash: str) -> None:
        """Set password hash (used during persistence)"""
        if not password_hash:
            raise InvalidUserError("password_hash cannot be empty")
        self.password_hash = password_hash
    
    def update_profile(self, firstname: str = None, lastname: str = None) -> None:
        """
        Update user profile information.
        
        Args:
            firstname: New first name (optional)
            lastname: New last name (optional)
        
        Raises:
            InvalidUserError: If new values violate rules
        """
        if firstname is not None:
            self.firstname = self._validate_name(firstname, "firstname")
        
        if lastname is not None:
            self.lastname = self._validate_name(lastname, "lastname")
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, name={self.firstname} {self.lastname})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id if self.id else self.email == other.email
