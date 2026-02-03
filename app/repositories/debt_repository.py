"""Debt Repository Interface"""
from abc import abstractmethod
from typing import Optional, List
from app.domain.entities import Debt
from app.repositories.repository import Repository


class DebtRepository(Repository[Debt]):
    """
    Repository interface for Debt entity.
    
    Extends base Repository with debt-specific query methods.
    """
    
    @abstractmethod
    def get_by_id(self, debt_id: int) -> Optional[Debt]:
        """Retrieve debt by ID"""
        pass
    
    @abstractmethod
    def get_by_id_and_user_id(self, debt_id: int, user_id: int) -> Optional[Debt]:
        """
        Retrieve debt by ID and verify it belongs to user.
        
        Args:
            debt_id: Debt ID
            user_id: User ID (owner)
        
        Returns:
            Debt or None if not found or doesn't belong to user
        """
        pass
    
    @abstractmethod
    def get_all_by_user_id(self, user_id: int) -> List[Debt]:
        """
        Retrieve all debts for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of user's debts
        """
        pass
    
    @abstractmethod
    def get_active_by_user_id(self, user_id: int) -> List[Debt]:
        """
        Retrieve active (non-closed) debts for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of active debts
        """
        pass
    
    @abstractmethod
    def calculate_total_principal_by_user_id(self, user_id: int) -> float:
        """
        Calculate sum of all active debt principals for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            Total principal amount
        """
        pass
