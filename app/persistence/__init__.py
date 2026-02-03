"""Persistence Layer - SQLAlchemy implementations and transaction management

This module exposes a factory helper `create_unit_of_work()` which wires
the concrete repository implementations into an `SQLAlchemyUnitOfWork`.
"""

from app.persistence.unit_of_work import (
    SQLAlchemyUnitOfWork,
)

from app.persistence.repositories import (
    UserRepositoryImpl,
    DebtRepositoryImpl,
    CategoryRepositoryImpl,
    IncomeRepositoryImpl,
    ExpenseRepositoryImpl,
    SavingGoalRepositoryImpl,
    DebtPaymentsRepositoryImpl,
    SavingTransactionsRepositoryImpl,
)


def create_unit_of_work() -> SQLAlchemyUnitOfWork:
    """Create a SQLAlchemyUnitOfWork pre-wired with repository implementations.

    Returns:
        SQLAlchemyUnitOfWork: ready-to-use unit of work instance
    """
    user_repo = UserRepositoryImpl()
    debt_repo = DebtRepositoryImpl()
    category_repo = CategoryRepositoryImpl()
    income_repo = IncomeRepositoryImpl()
    expense_repo = ExpenseRepositoryImpl()
    saving_goal_repo = SavingGoalRepositoryImpl()
    debt_payments_repo = DebtPaymentsRepositoryImpl()
    saving_transactions_repo = SavingTransactionsRepositoryImpl()

    return SQLAlchemyUnitOfWork(
        user_repo,
        debt_repo,
        category_repo,
        income_repo,
        expense_repo,
        saving_goal_repo,
        debt_payments_repo,
        saving_transactions_repo,
    )


__all__ = [
    "create_unit_of_work",
]
