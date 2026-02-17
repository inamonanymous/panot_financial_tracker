"""Category Domain Entity"""
from datetime import datetime
from app.domain.exceptions import InvalidCategoryError


class Category:
    """
    Category Domain Entity
    
    Represents income/expense categories for organizing transactions.
    """
    
    VALID_TYPES = {"income", "expense"}
    
    def __init__(
        self,
        user_id: int,
        type: str,
        name: str,
        description: str | None = None,
        id: int = None,
        created_at: datetime = None,
    ):
        """
        Initialize a Category entity.
        
        Args:
            user_id: Owner of the category
            type: "income" or "expense"
            name: Category name (e.g., "Salary", "Groceries")
            description: Optional category description
            id: Category ID (optional, assigned by database)
            created_at: Creation timestamp (optional)
        
        Raises:
            InvalidCategoryError: If any field violates domain rules
        """
        self.id = id
        self.user_id = self._validate_user_id(user_id)
        self.type = self._validate_type(type)
        self.name = self._validate_name(name)
        self.description = self._validate_description(description)
        self.created_at = created_at or datetime.utcnow()
    
    @staticmethod
    def _validate_user_id(user_id: int) -> int:
        """Validate user ID is a positive integer"""
        if not isinstance(user_id, int) or user_id <= 0:
            raise InvalidCategoryError("user_id must be a positive integer")
        return user_id
    
    @staticmethod
    def _validate_type(cat_type: str) -> str:
        """Validate category type is 'income' or 'expense'"""
        if not isinstance(cat_type, str):
            raise InvalidCategoryError("type must be a string")
        
        cat_type = cat_type.strip().lower()
        
        if cat_type not in Category.VALID_TYPES:
            raise InvalidCategoryError(
                f"type must be one of {Category.VALID_TYPES}, got '{cat_type}'"
            )
        
        return cat_type
    
    @staticmethod
    def _validate_name(name: str) -> str:
        """
        Validate category name.
        
        Rules:
        - At least 3 characters
        - Not empty
        """
        if not isinstance(name, str):
            raise InvalidCategoryError("name must be a string")
        
        name = name.strip()
        
        if len(name) < 3:
            raise InvalidCategoryError("name must be at least 3 characters")
        
        return name

    @staticmethod
    def _validate_description(description: str | None) -> str | None:
        if description is None:
            return None

        if not isinstance(description, str):
            raise InvalidCategoryError("description must be a string")

        description = description.strip()
        if not description:
            return None

        if len(description) > 255:
            raise InvalidCategoryError("description must be 255 characters or less")

        return description
    
    def rename(self, new_name: str) -> None:
        """Update category name with validation"""
        self.name = self._validate_name(new_name)

    def update_description(self, new_description: str | None) -> None:
        """Update category description with validation"""
        self.description = self._validate_description(new_description)
    
    def __repr__(self) -> str:
        return f"Category(id={self.id}, type={self.type}, name={self.name})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Category):
            return False
        return self.id == other.id if self.id else (
            self.user_id == other.user_id and self.name == other.name
        )
