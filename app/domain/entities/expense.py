"""Expense Domain Entity"""
from datetime import date, datetime
from app.domain.exceptions import InvalidExpenseError


class Expense:
    """
    Expense Domain Entity
    
    Represents money spent by a user.
    """
    
    VALID_PAYMENT_METHODS = {"cash", "gcash", "bank", "card", "other"}
    
    def __init__(
        self,
        user_id: int,
        category_id: int,
        payee: str,
        amount: float,
        expense_date: date,
        payment_method: str = "cash",
        remarks: str = "",
        id: int = None
    ):
        """
        Initialize an Expense entity.
        
        Args:
            user_id: Owner of the expense
            category_id: Expense category
            payee: Who/what the expense was paid to
            amount: Amount spent
            expense_date: When the expense occurred
            payment_method: How it was paid
            remarks: Optional notes
            id: Expense ID (optional, assigned by database)
        
        Raises:
            InvalidExpenseError: If any field violates domain rules
        """
        self.id = id
        self.user_id = self._validate_user_id(user_id)
        self.category_id = self._validate_category_id(category_id)
        self.payee = self._validate_payee(payee)
        self.amount = self._validate_amount(amount)
        self.expense_date = self._validate_expense_date(expense_date)
        self.payment_method = self._validate_payment_method(payment_method)
        self.remarks = remarks.strip() if isinstance(remarks, str) else ""
    
    @staticmethod
    def _validate_user_id(user_id: int) -> int:
        if not isinstance(user_id, int) or user_id <= 0:
            raise InvalidExpenseError("user_id must be a positive integer")
        return user_id
    
    @staticmethod
    def _validate_category_id(category_id: int) -> int:
        if not isinstance(category_id, int) or category_id <= 0:
            raise InvalidExpenseError("category_id must be a positive integer")
        return category_id
    
    @staticmethod
    def _validate_payee(payee: str) -> str:
        if not isinstance(payee, str):
            raise InvalidExpenseError("payee must be a string")
        
        payee = payee.strip()
        
        if len(payee) < 1:
            raise InvalidExpenseError("payee cannot be empty")
        
        return payee
    
    @staticmethod
    def _validate_amount(amount: float) -> float:
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise InvalidExpenseError("amount must be a number")
        
        if amount <= 0:
            raise InvalidExpenseError("amount must be greater than zero")
        
        return amount
    
    @staticmethod
    def _validate_expense_date(expense_date) -> date:
        """Convert datetime to date if needed, then validate."""
        # Handle datetime objects by converting to date
        if isinstance(expense_date, datetime):
            expense_date = expense_date.date()
        
        if not isinstance(expense_date, date):
            raise InvalidExpenseError("expense_date must be a date or datetime object")
        
        if expense_date > date.today():
            raise InvalidExpenseError("expense_date cannot be in the future")
        
        return expense_date
    
    @staticmethod
    def _validate_payment_method(method: str) -> str:
        if not isinstance(method, str):
            raise InvalidExpenseError("payment_method must be a string")
        
        method = method.strip().lower()
        
        if method not in Expense.VALID_PAYMENT_METHODS:
            raise InvalidExpenseError(
                f"payment_method must be one of {Expense.VALID_PAYMENT_METHODS}, got '{method}'"
            )
        
        return method
    
    def update(
        self,
        payee: str = None,
        amount: float = None,
        payment_method: str = None,
        remarks: str = None
    ) -> None:
        """Update expense details with validation"""
        if payee is not None:
            self.payee = self._validate_payee(payee)
        
        if amount is not None:
            self.amount = self._validate_amount(amount)
        
        if payment_method is not None:
            self.payment_method = self._validate_payment_method(payment_method)
        
        if remarks is not None:
            self.remarks = remarks.strip() if isinstance(remarks, str) else ""
    
    def __repr__(self) -> str:
        return (
            f"Expense(id={self.id}, payee={self.payee}, amount={self.amount}, "
            f"expense_date={self.expense_date})"
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Expense):
            return False
        return self.id == other.id if self.id else False
