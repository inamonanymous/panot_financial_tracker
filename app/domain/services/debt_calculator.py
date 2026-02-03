"""Debt Calculator - Pure business logic for debt operations"""
from datetime import date, timedelta
from app.domain.entities import Debt
from app.domain.exceptions import InvalidDebtError


class DebtCalculator:
    """
    Calculates debt-related metrics and interest.
    
    Pure business logic, no database access.
    """
    
    @staticmethod
    def calculate_interest_accrued(
        principal: float,
        annual_interest_rate: float,
        months: int = 1,
    ) -> float:
        """
        Calculate interest accrued over a period.
        
        Formula: Interest = Principal × (Rate % / 100) × (Months / 12)
        
        Args:
            principal: Loan amount
            annual_interest_rate: Annual rate as percentage (e.g., 5 for 5%)
            months: Number of months (default 1)
        
        Returns:
            Interest amount
        
        Example:
            interest = DebtCalculator.calculate_interest_accrued(
                principal=10000,
                annual_interest_rate=6,
                months=3
            )
            # Result: 10000 × (6/100) × (3/12) = 150
        """
        if principal < 0:
            raise InvalidDebtError("Principal cannot be negative")
        if annual_interest_rate < 0:
            raise InvalidDebtError("Interest rate cannot be negative")
        if months < 0:
            raise InvalidDebtError("Months cannot be negative")
        
        return float(principal * (annual_interest_rate / 100) * (months / 12))
    
    @staticmethod
    def calculate_total_amount_due(
        principal: float,
        annual_interest_rate: float,
        months: int = 1,
    ) -> float:
        """
        Calculate total amount to pay (principal + interest).
        
        Args:
            principal: Loan amount
            annual_interest_rate: Annual rate as percentage
            months: Number of months
        
        Returns:
            Total amount (principal + interest)
        """
        interest = DebtCalculator.calculate_interest_accrued(
            principal, annual_interest_rate, months
        )
        return float(principal + interest)
    
    @staticmethod
    def calculate_monthly_payment(
        principal: float,
        annual_interest_rate: float,
        months_remaining: int,
    ) -> float:
        """
        Calculate approximate monthly payment (simple interest, equal installments).
        
        Note: This is simplified. Real loans use amortization formulas.
        
        Args:
            principal: Loan amount
            annual_interest_rate: Annual rate as percentage
            months_remaining: Months until due date
        
        Returns:
            Approximate monthly payment amount
        
        Raises:
            InvalidDebtError: If months_remaining is 0
        """
        if months_remaining <= 0:
            raise InvalidDebtError("Months remaining must be greater than zero")
        
        total_due = DebtCalculator.calculate_total_amount_due(
            principal, annual_interest_rate, months_remaining
        )
        return float(total_due / months_remaining)
    
    @staticmethod
    def calculate_months_until_due(due_date: date) -> int:
        """
        Calculate number of months from today until due date.
        
        Args:
            due_date: Debt due date
        
        Returns:
            Number of months remaining (0 if overdue)
        """
        today = date.today()
        
        if due_date <= today:
            return 0
        
        # Simple month calculation
        months = (due_date.year - today.year) * 12 + (due_date.month - today.month)
        return max(0, months)
    
    @staticmethod
    def is_overdue(due_date: date) -> bool:
        """Check if debt is overdue"""
        return due_date < date.today()
    
    @staticmethod
    def is_due_soon(due_date: date, days_threshold: int = 7) -> bool:
        """
        Check if debt is due soon (within threshold days).
        
        Args:
            due_date: Debt due date
            days_threshold: Number of days to consider "soon" (default 7)
        
        Returns:
            True if due within threshold and not overdue
        """
        today = date.today()
        days_until_due = (due_date - today).days
        
        return 0 < days_until_due <= days_threshold
    
    @staticmethod
    def get_debt_status_label(debt: Debt) -> str:
        """
        Get human-readable status label for a debt.
        
        Args:
            debt: Debt entity
        
        Returns:
            Status label ("Active", "Overdue", "Due Soon", "Closed")
        """
        if debt.status == "closed":
            return "Closed"
        
        if DebtCalculator.is_overdue(debt.due_date):
            return "Overdue"
        
        if DebtCalculator.is_due_soon(debt.due_date):
            return "Due Soon"
        
        return "Active"
