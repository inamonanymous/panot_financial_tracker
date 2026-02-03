"""Unit of Work Pattern - Manages database transactions"""
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator
from app.ext import db
from app.repositories import (
    UserRepository,
    DebtRepository,
    CategoryRepository,
    IncomeRepository,
    ExpenseRepository,
    SavingGoalRepository,
    DebtPaymentsRepository,
    SavingTransactionsRepository,
)
from app.repositories.exceptions import RepositoryOperationError


class UnitOfWork(ABC):
    """
    Unit of Work Pattern
    
    Manages database transactions and provides access to all repositories
    within a transaction context.
    
    Usage:
        with unit_of_work.transaction():
            user = unit_of_work.users.save(new_user)
            debt = unit_of_work.debts.save(new_debt)
            # Automatically commits on success, rolls back on failure
    """
    
    users: UserRepository
    debts: DebtRepository
    categories: CategoryRepository
    incomes: IncomeRepository
    expenses: ExpenseRepository
    saving_goals: SavingGoalRepository
    debt_payments: DebtPaymentsRepository
    saving_transactions: SavingTransactionsRepository
    
    @abstractmethod
    def commit(self) -> None:
        """Commit current transaction"""
        pass
    
    @abstractmethod
    def rollback(self) -> None:
        """Rollback current transaction"""
        pass
    
    @abstractmethod
    @contextmanager
    def transaction(self) -> Generator:
        """
        Context manager for database transactions.
        
        Automatically commits on success, rolls back on exception.
        
        Example:
            with unit_of_work.transaction():
                # All operations here are atomic
                entity1 = unit_of_work.users.save(user)
                entity2 = unit_of_work.debts.save(debt)
        
        Yields:
            Self (for access to repositories)
        """
        pass


class SQLAlchemyUnitOfWork(UnitOfWork):
    """
    SQLAlchemy implementation of Unit of Work.
    
    Uses Flask-SQLAlchemy session for transaction management.
    """
    
    def __init__(
        self,
        user_repo: UserRepository,
        debt_repo: DebtRepository,
        category_repo: CategoryRepository,
        income_repo: IncomeRepository,
        expense_repo: ExpenseRepository,
        saving_goal_repo: SavingGoalRepository,
        debt_payments_repo: DebtPaymentsRepository,
        saving_transactions_repo: SavingTransactionsRepository,
    ):
        """
        Initialize Unit of Work with repository implementations.
        
        Args:
            user_repo: UserRepository implementation
            debt_repo: DebtRepository implementation
            category_repo: CategoryRepository implementation
            income_repo: IncomeRepository implementation
            expense_repo: ExpenseRepository implementation
            saving_goal_repo: SavingGoalRepository implementation
        """
        self.users = user_repo
        self.debts = debt_repo
        self.categories = category_repo
        self.incomes = income_repo
        self.expenses = expense_repo
        self.saving_goals = saving_goal_repo
        self.debt_payments = debt_payments_repo
        self.saving_transactions = saving_transactions_repo
    
    def commit(self) -> None:
        """Commit changes to database"""
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RepositoryOperationError(f"Failed to commit transaction: {str(e)}")
    
    def rollback(self) -> None:
        """Rollback changes"""
        db.session.rollback()
    
    @contextmanager
    def transaction(self) -> Generator:
        """
        Context manager for atomic transactions.
        
        Yields:
            Self for repository access
        """
        try:
            yield self
            self.commit()
        except Exception as e:
            self.rollback()
            raise RepositoryOperationError(f"Transaction failed: {str(e)}")


class TransactionScope:
    """
    Helper for managing transaction state.
    
    Useful for nested transactions and complex workflows.
    """
    
    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work
        self.is_active = False
    
    def __enter__(self):
        self.is_active = True
        return self.unit_of_work
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.unit_of_work.rollback()
            self.is_active = False
            return False
        else:
            self.unit_of_work.commit()
            self.is_active = False
            return True
