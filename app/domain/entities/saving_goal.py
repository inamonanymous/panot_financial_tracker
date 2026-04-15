"""SavingGoal Domain Entity"""
from datetime import date


class SavingGoal:
    """
    SavingGoal Domain Entity
    
    Represents a savings target.
    """
    
    def __init__(
        self,
        user_id: int,
        name: str,
        target_amount: float,
        target_date: date,
        remarks: str = "",
        created_at: date = None,
        id: int = None
    ):
        """
        Initialize a SavingGoal entity.
        
        Args:
            user_id: Owner of the goal
            name: Goal name (e.g., "Emergency Fund")
            target_amount: Amount to save
            target_date: Target completion date
            remarks: Optional notes
            id: Goal ID (optional, assigned by database)
        """
        self.id = id
        self.user_id = user_id
        self.name = name
        self.target_amount = target_amount
        self.target_date = target_date
        self.remarks = remarks.strip() if isinstance(remarks, str) else ""
        self.current_amount = 0.0  # Tracked separately
        self.created_at = created_at
    
    def update(
        self,
        name: str = None,
        target_amount: float = None,
        target_date: date = None,
        remarks: str = None
    ) -> None:
        """Update goal details"""
        if name is not None:
            self.name = name
        
        if target_amount is not None:
            self.target_amount = target_amount
        
        if target_date is not None:
            self.target_date = target_date
        
        if remarks is not None:
            self.remarks = remarks.strip() if isinstance(remarks, str) else ""
    
    def get_progress_percentage(self) -> float:
        """Calculate progress towards goal (0-100%)"""
        if self.target_amount <= 0:
            print("Warning: Target amount is zero or negative, cannot calculate progress percentage.")
            return 0.0
        return min(100.0, (self.current_amount / self.target_amount) * 100)
    
    def is_completed(self) -> bool:
        """Check if goal has been met"""
        return self.current_amount >= self.target_amount
    
    def is_overdue(self) -> bool:
        """Check if target date has passed without reaching goal"""
        return date.today() > self.target_date and not self.is_completed()
    
    def __repr__(self) -> str:
        return (
            f"SavingGoal(id={self.id}, name={self.name}, "
            f"target={self.target_amount}, current={self.current_amount})"
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, SavingGoal):
            return False
        return self.id == other.id if self.id else (
            self.user_id == other.user_id and self.name == other.name
        )
