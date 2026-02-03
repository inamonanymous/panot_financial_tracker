"""Repository Layer Exceptions"""


class RepositoryError(Exception):
    """Base exception for repository operations"""
    pass


class EntityNotFoundError(RepositoryError):
    """Entity not found in repository"""
    pass


class EntityAlreadyExistsError(RepositoryError):
    """Entity already exists (e.g., duplicate email)"""
    pass


class RepositoryOperationError(RepositoryError):
    """Generic repository operation failure"""
    pass
