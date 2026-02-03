"""Income Domain Entity"""
from datetime import date
from app.domain.exceptions import InvalidIncomeError


class Income:
    """
    Income Domain Entity
    
    Represents income received by a user.
    """
    
    VALID_PAYMENT_METHODS = {"cash", "gcash", "bank", "card", "other"}
    
    def __init__(
        self,
        user_id: int,
        category_id: int,
        source: str,
        amount: float,
        received_date: date,
        payment_method: str = "cash",
        remarks: str = "",
        id: int = None
    ):
        """
        Initialize an Income entity.
        
        Args:
            user_id: Owner of the income
            category_id: Income category
            source: Source of income (e.g., "Salary", "Freelance")
            amount: Amount received
            received_date: When income was received
            payment_method: How it was received
            remarks: Optional notes
            id: Income ID (optional, assigned by database)
        
        Raises:
            InvalidIncomeError: If any field violates domain rules
        """
        self.id = id
        self.user_id = self._validate_user_id(user_id)
        self.category_id = self._validate_category_id(category_id)
        self.source = self._validate_source(source)
        self.amount = self._validate_amount(amount)
        self.received_date = self._validate_received_date(received_date)
        self.payment_method = self._validate_payment_method(payment_method)
        self.remarks = remarks.strip() if isinstance(remarks, str) else ""
    
    @staticmethod
    def _validate_user_id(user_id: int) -> int:
        if not isinstance(user_id, int) or user_id <= 0:
            raise InvalidIncomeError("user_id must be a positive integer")
        return user_id
    
    @staticmethod
    def _validate_category_id(category_id: int) -> int:
        if not isinstance(category_id, int) or category_id <= 0:
            raise InvalidIncomeError("category_id must be a positive integer")
        return category_id
    
    @staticmethod
    def _validate_source(source: str) -> str:
        if not isinstance(source, str):
            raise InvalidIncomeError("source must be a string")
        
        source = source.strip()
        
        if len(source) < 1:
            raise InvalidIncomeError("source cannot be empty")
        
        return source
    
    @staticmethod
    def _validate_amount(amount: float) -> float:
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise InvalidIncomeError("amount must be a number")
        
        if amount <= 0:
            raise InvalidIncomeError("amount must be greater than zero")
        
        return amount
    
    @staticmethod
    def _validate_received_date(received_date: date) -> date:
        if not isinstance(received_date, date):
            raise InvalidIncomeError("received_date must be a date object")
        
        if received_date > date.today():
            raise InvalidIncomeError("received_date cannot be in the future")
        
        return received_date
    
    @staticmethod
    def _validate_payment_method(method: str) -> str:
        if not isinstance(method, str):
            raise InvalidIncomeError("payment_method must be a string")
        
        method = method.strip().lower()
        
        if method not in Income.VALID_PAYMENT_METHODS:
            raise InvalidIncomeError(
                f"payment_method must be one of {Income.VALID_PAYMENT_METHODS}, got '{method}'"
            )
        
        return method
    
    def update(
        self,
        source: str = None,
        amount: float = None,
        payment_method: str = None,
        remarks: str = None
    ) -> None:
        """Update income details with validation"""
        if source is not None:
            self.source = self._validate_source(source)
        
        if amount is not None:
            self.amount = self._validate_amount(amount)
        
        if payment_method is not None:
            self.payment_method = self._validate_payment_method(payment_method)
        
        if remarks is not None:
            self.remarks = remarks.strip() if isinstance(remarks, str) else ""
    
    def __repr__(self) -> str:
        return (
            f"Income(id={self.id}, source={self.source}, amount={self.amount}, "
            f"received_date={self.received_date})"
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Income):
            return False
        return self.id == other.id if self.id else False
