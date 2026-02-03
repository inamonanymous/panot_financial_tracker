"""User Repository Interface"""
from abc import abstractmethod
from typing import Optional
from app.domain.entities import User
from app.repositories.repository import Repository


class UserRepository(Repository[User]):
    """
    Repository interface for User entity.
    
    Extends base Repository with user-specific query methods.
    """
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve user by email.
        
        Args:
            email: User's email address
        
        Returns:
            User or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID"""
        pass
