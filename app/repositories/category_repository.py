"""Category Repository Interface"""
from abc import abstractmethod
from typing import Optional, List
from app.domain.entities import Category
from app.repositories.repository import Repository


class CategoryRepository(Repository[Category]):
    """
    Repository interface for Category entity.
    
    Extends base Repository with category-specific query methods.
    """
    
    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Retrieve category by ID"""
        pass
    
    @abstractmethod
    def get_by_id_and_user_id(self, category_id: int, user_id: int) -> Optional[Category]:
        """
        Retrieve category by ID and verify it belongs to user.
        
        Args:
            category_id: Category ID
            user_id: User ID (owner)
        
        Returns:
            Category or None if not found or doesn't belong to user
        """
        pass
    
    @abstractmethod
    def get_by_name_and_user_id(self, name: str, user_id: int) -> Optional[Category]:
        """
        Retrieve category by name for a specific user.
        
        Args:
            name: Category name
            user_id: User ID (owner)
        
        Returns:
            Category or None if not found
        """
        pass
    
    @abstractmethod
    def get_all_by_user_id(self, user_id: int) -> List[Category]:
        """
        Retrieve all categories for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of user's categories
        """
        pass
    
    @abstractmethod
    def get_all_by_user_and_type(self, user_id: int, category_type: str) -> List[Category]:
        """
        Retrieve categories by user and type.
        
        Args:
            user_id: User ID
            category_type: "income" or "expense"
        
        Returns:
            List of matching categories
        """
        pass
    
    @abstractmethod
    def exists_with_name_and_user(self, name: str, user_id: int) -> bool:
        """
        Check if category with name exists for user.
        
        Args:
            name: Category name
            user_id: User ID
        
        Returns:
            True if exists
        """
        pass
    
    @abstractmethod
    def is_in_use(self, category_id: int) -> bool:
        """
        Check if category is used in any transactions.
        
        Args:
            category_id: Category ID
        
        Returns:
            True if used in income/expense records
        """
        pass
