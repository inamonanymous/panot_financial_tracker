"""SavingGoal Repository Interface"""
from abc import abstractmethod
from typing import Optional, List
from app.domain.entities import SavingGoal
from app.repositories.repository import Repository


class SavingGoalRepository(Repository[SavingGoal]):
    """
    Repository interface for SavingGoal entity.
    
    Extends base Repository with saving goal-specific query methods.
    """
    
    @abstractmethod
    def get_by_id(self, goal_id: int) -> Optional[SavingGoal]:
        """Retrieve saving goal by ID"""
        pass
    
    @abstractmethod
    def get_by_id_and_user_id(self, goal_id: int, user_id: int) -> Optional[SavingGoal]:
        """
        Retrieve saving goal by ID and verify it belongs to user.
        
        Args:
            goal_id: Goal ID
            user_id: User ID (owner)
        
        Returns:
            SavingGoal or None if not found or doesn't belong to user
        """
        pass
    
    @abstractmethod
    def get_all_by_user_id(self, user_id: int) -> List[SavingGoal]:
        """
        Retrieve all saving goals for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of user's saving goals
        """
        pass
    
    @abstractmethod
    def get_active_by_user_id(self, user_id: int) -> List[SavingGoal]:
        """
        Retrieve active (incomplete) saving goals for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of active saving goals
        """
        pass
