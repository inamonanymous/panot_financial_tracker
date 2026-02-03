"""Income Repository Interface"""
from abc import abstractmethod
from typing import Optional, List
from app.domain.entities import Income
from app.repositories.repository import Repository


class IncomeRepository(Repository[Income]):
    """
    Repository interface for Income entity.
    
    Extends base Repository with income-specific query methods.
    """
    
    @abstractmethod
    def get_by_id(self, income_id: int) -> Optional[Income]:
        """Retrieve income by ID"""
        pass
    
    @abstractmethod
    def get_by_id_and_user_id(self, income_id: int, user_id: int) -> Optional[Income]:
        """
        Retrieve income by ID and verify it belongs to user.
        
        Args:
            income_id: Income ID
            user_id: User ID (owner)
        
        Returns:
            Income or None if not found or doesn't belong to user
        """
        pass
    
    @abstractmethod
    def get_all_by_user_id(self, user_id: int) -> List[Income]:
        """
        Retrieve all income records for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of user's income records
        """
        pass
    
    @abstractmethod
    def calculate_total_by_user_id(self, user_id: int) -> float:
        """
        Calculate total income for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            Total income amount
        """
        pass
    
    @abstractmethod
    def get_by_category_id(self, category_id: int) -> List[Income]:
        """
        Retrieve all income records in a category.
        
        Args:
            category_id: Category ID
        
        Returns:
            List of income records
        """
        pass
