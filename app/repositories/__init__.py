"""Repository Interfaces - Abstract data access contracts"""

from app.repositories.repository import Repository
from app.repositories.user_repository import UserRepository
from app.repositories.debt_repository import DebtRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.income_repository import IncomeRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.saving_goal_repository import SavingGoalRepository
from app.repositories.debt_payments_repository import DebtPaymentsRepository
from app.repositories.saving_transactions_repository import SavingTransactionsRepository
from app.repositories.exceptions import (
    RepositoryError,
    EntityNotFoundError,
    EntityAlreadyExistsError,
    RepositoryOperationError,
)

__all__ = [
    "Repository",
    "UserRepository",
    "DebtRepository",
    "CategoryRepository",
    "IncomeRepository",
    "ExpenseRepository",
    "SavingGoalRepository",
    "DebtPaymentsRepository",
    "SavingTransactionsRepository",
    "RepositoryError",
    "EntityNotFoundError",
    "EntityAlreadyExistsError",
    "RepositoryOperationError",
]
