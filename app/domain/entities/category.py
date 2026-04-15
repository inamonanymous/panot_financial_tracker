"""Category Domain Entity"""
from datetime import datetime


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
        """
        self.id = id
        self.user_id = user_id
        self.type = type
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.utcnow()
    


        return description
    
    def rename(self, new_name: str) -> None:
        """Update category name"""
        self.name = new_name

    def update_description(self, new_description: str | None) -> None:
        """Update category description"""
        self.description = new_description
    
    def __repr__(self) -> str:
        return f"Category(id={self.id}, type={self.type}, name={self.name})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Category):
            return False
        return self.id == other.id if self.id else (
            self.user_id == other.user_id and self.name == other.name
        )
