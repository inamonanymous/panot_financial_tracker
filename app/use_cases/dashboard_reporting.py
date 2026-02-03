"""Dashboard Reporting Use Case - Orchestrates dashboard data aggregation using UOW and domain services."""
from sqlalchemy import func
from app.model.m_Income import Income
from app.model.m_Expenses import Expenses
from app.model.m_SavingTransactions import SavingTransactions
from app.ext import db


class DashboardReportingUseCase:
    """Aggregates dashboard metrics using repositories and domain services."""

    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, user_id: int) -> dict:
        """
        Calculate all dashboard metrics for a user.
        
        Returns:
            dict with keys:
                - total_income: float
                - total_expense: float
                - total_saving_deposits: float
                - user_total_value: float (income - expense - saving_deposits)
        """
        # Get all incomes for user and sum
        incomes = self.uow.incomes.get_all_by_user_id(user_id)
        total_income = sum(inc.amount for inc in incomes) if incomes else 0.0

        # Get all expenses for user and sum
        expenses = self.uow.expenses.get_all_by_user_id(user_id)
        total_expense = sum(exp.amount for exp in expenses) if expenses else 0.0

        # Get total saving deposits (via raw query like legacy code)
        total_saving_deposits = self._calculate_total_saving_deposits(user_id)

        # Calculate net value
        user_total_value = total_income - total_expense - total_saving_deposits

        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "total_saving_deposits": float(total_saving_deposits),
            "user_total_value": float(user_total_value),
        }

    def _calculate_total_saving_deposits(self, user_id: int) -> float:
        """Calculate total saving transaction deposits using income relationship."""
        total = (
            db.session.query(func.coalesce(func.sum(Income.amount), 0))
            .join(
                SavingTransactions,
                SavingTransactions.income_id == Income.id
            )
            .filter(SavingTransactions.user_id == user_id)
            .filter(SavingTransactions.txt_type == "deposit")
            .scalar()
        )
        return float(total)
