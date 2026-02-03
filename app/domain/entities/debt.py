"""Debt Domain Entity"""
from datetime import date
from app.domain.exceptions import InvalidDebtError


class Debt:
    """
    Debt Domain Entity
    
    Represents a debt with principal, interest, and status tracking.
    Contains business rules for debt constraints.
    """
    
    VALID_STATUSES = {"active", "closed"}
    MIN_PRINCIPAL = 100  # Business rule: minimum debt principal is 100 PHP
    MAX_INTEREST_RATE = 6.0  # Business rule: max interest rate is 6%
    
    def __init__(
        self,
        user_id: int,
        lender: str,
        principal: float,
        interest_rate: float,
        start_date: date,
        due_date: date,
        name: str = None,
        status: str = "active",
        id: int = None
    ):
        """
        Initialize a Debt entity.
        
        Args:
            user_id: Owner of the debt
            lender: Creditor name
            principal: Loan amount
            interest_rate: Annual interest rate (%)
            start_date: When debt was incurred
            due_date: When debt is due
            name: Debt name/description (optional)
            status: "active" or "closed" (default "active")
            id: Debt ID (optional, assigned by database)
        
        Raises:
            InvalidDebtError: If any field violates domain rules
        """
        self.id = id
        self.user_id = self._validate_user_id(user_id)
        self.lender = self._validate_lender(lender)
        self.principal = self._validate_principal(principal)
        self.interest_rate = self._validate_interest_rate(interest_rate)
        self.start_date = self._validate_start_date(start_date)
        self.due_date = self._validate_due_date(due_date, self.start_date)
        self.name = name or f"Debt to {self.lender}"
        self.status = self._validate_status(status)
    
    @staticmethod
    def _validate_user_id(user_id: int) -> int:
        """Validate user ID"""
        if not isinstance(user_id, int) or user_id <= 0:
            raise InvalidDebtError("user_id must be a positive integer")
        return user_id
    
    @staticmethod
    def _validate_lender(lender: str) -> str:
        """Validate lender name (creditor)"""
        if not isinstance(lender, str):
            raise InvalidDebtError("lender must be a string")
        
        lender = lender.strip()
        
        if len(lender) < 3:
            raise InvalidDebtError("lender name must be at least 3 characters")
        
        return lender
    
    @staticmethod
    def _validate_principal(principal: float) -> float:
        """
        Validate principal amount.
        
        Business Rule: Minimum principal is 100 PHP
        """
        try:
            principal = float(principal)
        except (TypeError, ValueError):
            raise InvalidDebtError("principal must be a number")
        
        if principal < Debt.MIN_PRINCIPAL:
            raise InvalidDebtError(
                f"principal must be at least {Debt.MIN_PRINCIPAL} PHP, got {principal}"
            )
        
        return principal
    
    @staticmethod
    def _validate_interest_rate(interest_rate: float) -> float:
        """
        Validate interest rate.
        
        Business Rules:
        - Must be positive
        - Cannot exceed 6%
        """
        try:
            interest_rate = float(interest_rate)
        except (TypeError, ValueError):
            raise InvalidDebtError("interest_rate must be a number")
        
        if interest_rate < 0:
            raise InvalidDebtError("interest_rate cannot be negative")
        
        if interest_rate > Debt.MAX_INTEREST_RATE:
            raise InvalidDebtError(
                f"interest_rate cannot exceed {Debt.MAX_INTEREST_RATE}%, got {interest_rate}%"
            )
        
        return interest_rate
    
    @staticmethod
    def _validate_start_date(start_date: date) -> date:
        """Validate start date (must be in the past or today)"""
        if not isinstance(start_date, date):
            raise InvalidDebtError("start_date must be a date object")
        
        if start_date > date.today():
            raise InvalidDebtError("start_date cannot be in the future")
        
        return start_date
    
    @staticmethod
    def _validate_due_date(due_date: date, start_date: date) -> date:
        """Validate due date (must be after start date and in the future)"""
        if not isinstance(due_date, date):
            raise InvalidDebtError("due_date must be a date object")
        
        if due_date <= start_date:
            raise InvalidDebtError("due_date must be after start_date")
        
        if due_date < date.today():
            raise InvalidDebtError("due_date must be in the future")
        
        return due_date
    
    @staticmethod
    def _validate_status(status: str) -> str:
        """Validate debt status"""
        if not isinstance(status, str):
            raise InvalidDebtError("status must be a string")
        
        status = status.strip().lower()
        
        if status not in Debt.VALID_STATUSES:
            raise InvalidDebtError(
                f"status must be one of {Debt.VALID_STATUSES}, got '{status}'"
            )
        
        return status
    
    def close(self) -> None:
        """Mark debt as closed (business logic)"""
        if self.status == "closed":
            raise InvalidDebtError("Debt is already closed")
        self.status = "closed"
    
    def reopen(self) -> None:
        """Reopen a closed debt"""
        if self.status == "active":
            raise InvalidDebtError("Debt is already active")
        self.status = "active"
    
    def update_terms(self, principal: float = None, interest_rate: float = None) -> None:
        """
        Update debt terms with validation.
        
        Args:
            principal: New principal amount (optional)
            interest_rate: New interest rate (optional)
        
        Raises:
            InvalidDebtError: If new values violate rules
        """
        if principal is not None:
            self.principal = self._validate_principal(principal)
        
        if interest_rate is not None:
            self.interest_rate = self._validate_interest_rate(interest_rate)
    
    def calculate_interest_amount(self, months: int = 12) -> float:
        """Calculate interest accrued over a period"""
        return self.principal * (self.interest_rate / 100) * (months / 12)
    
    def __repr__(self) -> str:
        return (
            f"Debt(id={self.id}, lender={self.lender}, principal={self.principal}, "
            f"interest_rate={self.interest_rate}%, status={self.status})"
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Debt):
            return False
        return self.id == other.id if self.id else (
            self.user_id == other.user_id and self.lender == other.lender
        )
