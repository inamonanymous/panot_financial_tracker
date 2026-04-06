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
        created_at: date = None,
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
        self.user_id = user_id
        self.lender = lender
        self.principal = principal
        self.interest_rate = interest_rate
        self.start_date = start_date
        self.due_date = due_date
        self.name = name
        self.status = status
        self.created_at = created_at

    def update(
        self,
        name: str = None,
        lender: str = None,
        principal: float = None,
        interest_rate: float = None,
        start_date: date = None,
        due_date: date = None,
        status: str = None,
    ):
        """Update debt fields on the entity."""
        if name is not None:
            self.name = name
        if lender is not None:
            self.lender = lender
        if principal is not None:
            self.principal = principal
        if interest_rate is not None:
            self.interest_rate = interest_rate
        if start_date is not None:
            self.start_date = start_date
        if due_date is not None:
            self.due_date = due_date
        if status is not None:
            self.status = status
