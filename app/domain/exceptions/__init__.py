"""Domain Layer Exceptions - Pure business rule violations"""


class DomainError(Exception):
    """Base exception for all domain logic errors"""
    pass


class InvalidUserError(DomainError):
    """User data violates domain rules"""
    pass


class InvalidDebtError(DomainError):
    """Debt data violates domain rules"""
    pass


class InvalidIncomeError(DomainError):
    """Income data violates domain rules"""
    pass


class InvalidExpenseError(DomainError):
    """Expense data violates domain rules"""
    pass


class InvalidCategoryError(DomainError):
    """Category data violates domain rules"""
    pass


class InvalidSavingGoalError(DomainError):
    """Saving goal data violates domain rules"""
    pass
