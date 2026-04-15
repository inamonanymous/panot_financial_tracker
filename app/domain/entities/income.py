"""Income Domain Entity"""
from datetime import date, datetime


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
        amount: float,
        received_date: date,
        name: str,
        source: str,
        payment_method: str = "cash",
        remarks: str = "",
        id: int = None,
        created_at: datetime = None
    ):
        """
        Initialize an Income entity.
        
        Args:
            user_id: Owner of the income
            category_id: Income category
            name: Income name/title (e.g., "January Salary")
            source: Income source (e.g., Employer, Client, Business)
            amount: Amount received
            received_date: When income was received
            payment_method: How it was received
            remarks: Optional notes
            id: Income ID (optional, assigned by database)
            created_at: When the record was created (optional, assigned by database)
        """
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        resolved_name = name if name is not None else source
        resolved_source = source if source is not None else name
        self.name = resolved_name
        self.source = resolved_source
        self.amount = amount
        self.received_date = received_date
        self.payment_method = payment_method
        self.remarks = remarks.strip() if isinstance(remarks, str) else ""
        self.created_at = created_at
    
    def update(
        self,
        name: str = None,
        source: str = None,
        amount: float = None,
        payment_method: str = None,
        remarks: str = None
    ) -> None:
        """Update income details"""
        if name is not None:
            self.name = name

        if source is not None:
            self.source = source
        
        if amount is not None:
            self.amount = amount
        
        if payment_method is not None:
            self.payment_method = payment_method
        
        if remarks is not None:
            self.remarks = remarks.strip() if isinstance(remarks, str) else ""
    
    def __repr__(self) -> str:
        return (
            f"Income(id={self.id}, name={self.name}, amount={self.amount}, "
            f"received_date={self.received_date})"
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Income):
            return False
        return self.id == other.id if self.id else False
