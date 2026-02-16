"""Base Repository Interface - All repositories implement this contract"""
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')  # Generic type for entity


class Repository(ABC, Generic[T]):
    """
    Abstract base repository.
    
    All concrete repositories (UserRepository, DebtRepository, etc.) 
    must implement these methods.
    
    This ensures consistent data access patterns and makes services
    independent of specific database implementations.
    """
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save a new entity to database.
        
        Args:
            entity: Domain entity to persist
        
        Returns:
            Saved entity (with ID assigned)
        
        Raises:
            RepositoryError: If save fails
        """
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Retrieve an entity by ID.
        
        Args:
            entity_id: Primary key
        
        Returns:
            Entity or None if not found
        """
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """
        Update an existing entity.
        
        Args:
            entity: Domain entity with updated values
        
        Returns:
            Updated entity
        
        Raises:
            RepositoryError: If update fails
        """
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Create a new entity.
        
        Args:
            entity: Domain entity to persist
        
        Returns:
            Created entity
        
        Raises:
            RepositoryError: If creation fails
        """
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """
        Delete an entity by ID.
        
        Args:
            entity_id: Primary key to delete
        
        Returns:
            True if deleted, False if not found
        
        Raises:
            RepositoryError: If delete fails
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Retrieve all entities.
        
        Returns:
            List of all entities
        """
        pass
