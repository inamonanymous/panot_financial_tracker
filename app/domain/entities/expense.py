"""Expense Domain Entity"""
from datetime import date, datetime


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
        amount: float,
        expense_date: date,
        name: str,
        payee: str,
        payment_method: str = "cash",
        remarks: str = "",
        id: int = None,
        created_at: datetime = None
    ):
        """
        Initialize an Expense entity.
        
        Args:
            user_id: Owner of the expense
            category_id: Expense category
            name: Expense name/title
            payee: Payee (person/company/account receiving payment)
            amount: Amount spent
            expense_date: When the expense occurred
            payment_method: How it was paid
            remarks: Optional notes
            id: Expense ID (optional, assigned by database)
            created_at: When the record was created (optional, assigned by database)
        """
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        resolved_name = name if name is not None else payee
        resolved_payee = payee if payee is not None else name
        self.name = resolved_name
        self.payee = resolved_payee
        self.amount = amount
        self.expense_date = expense_date
        self.payment_method = payment_method
        self.remarks = remarks.strip() if isinstance(remarks, str) else ""
        self.created_at = created_at
    
    def update(
        self,
        name: str = None,
        payee: str = None,
        amount: float = None,
        payment_method: str = None,
        remarks: str = None
    ) -> None:
        """Update expense details"""
        if name is not None:
            self.name = name

        if payee is not None:
            self.payee = payee
        
        if amount is not None:
            self.amount = amount
        
        if payment_method is not None:
            self.payment_method = payment_method
        
        if remarks is not None:
            self.remarks = remarks.strip() if isinstance(remarks, str) else ""
    
    def __repr__(self) -> str:
        return (
            f"Expense(id={self.id}, name={self.name}, amount={self.amount}, "
            f"expense_date={self.expense_date})"
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Expense):
            return False
        return self.id == other.id if self.id else False
