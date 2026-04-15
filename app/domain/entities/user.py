"""User Domain Entity - Pure business logic, no database access"""


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
        """
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password_hash = password_hash
        self.current_value = 0.0  # Will be calculated by domain services
    
    def set_password_hash(self, password_hash: str) -> None:
        """Set password hash (used during persistence)"""
        self.password_hash = password_hash
    
    def update_profile(self, firstname: str = None, lastname: str = None) -> None:
        """
        Update user profile information.
        
        Args:
            firstname: New first name (optional)
            lastname: New last name (optional)
        """
        if firstname is not None:
            self.firstname = firstname
        
        if lastname is not None:
            self.lastname = lastname
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, name={self.firstname} {self.lastname})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id if self.id else self.email == other.email
