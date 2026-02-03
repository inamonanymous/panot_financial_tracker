"""Expense Repository Interface"""
from abc import abstractmethod
from typing import Optional, List
from app.domain.entities import Expense
from app.repositories.repository import Repository


class ExpenseRepository(Repository[Expense]):
    """
    Repository interface for Expense entity.
    
    Extends base Repository with expense-specific query methods.
    """
    
    @abstractmethod
    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        """Retrieve expense by ID"""
        pass
    
    @abstractmethod
    def get_by_id_and_user_id(self, expense_id: int, user_id: int) -> Optional[Expense]:
        """
        Retrieve expense by ID and verify it belongs to user.
        
        Args:
            expense_id: Expense ID
            user_id: User ID (owner)
        
        Returns:
            Expense or None if not found or doesn't belong to user
        """
        pass
    
    @abstractmethod
    def get_all_by_user_id(self, user_id: int) -> List[Expense]:
        """
        Retrieve all expense records for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of user's expense records
        """
        pass
    
    @abstractmethod
    def calculate_total_by_user_id(self, user_id: int) -> float:
        """
        Calculate total expenses for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            Total expense amount
        """
        pass
    
    @abstractmethod
    def get_by_category_id(self, category_id: int) -> List[Expense]:
        """
        Retrieve all expense records in a category.
        
        Args:
            category_id: Category ID
        
        Returns:
            List of expense records
        """
        pass
