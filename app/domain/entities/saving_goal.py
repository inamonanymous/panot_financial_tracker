"""SavingGoal Domain Entity"""
from datetime import date
from app.domain.exceptions import InvalidSavingGoalError


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
        
        Raises:
            InvalidSavingGoalError: If any field violates domain rules
        """
        self.id = id
        self.user_id = self._validate_user_id(user_id)
        self.name = self._validate_name(name)
        self.target_amount = self._validate_target_amount(target_amount)
        self.target_date = self._validate_target_date(target_date)
        self.remarks = remarks.strip() if isinstance(remarks, str) else ""
        self.current_amount = 0.0  # Tracked separately
    
    @staticmethod
    def _validate_user_id(user_id: int) -> int:
        if not isinstance(user_id, int) or user_id <= 0:
            raise InvalidSavingGoalError("user_id must be a positive integer")
        return user_id
    
    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            raise InvalidSavingGoalError("name must be a string")
        
        name = name.strip()
        
        if len(name) < 3:
            raise InvalidSavingGoalError("name must be at least 3 characters")
        
        return name
    
    @staticmethod
    def _validate_target_amount(amount: float) -> float:
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise InvalidSavingGoalError("target_amount must be a number")
        
        if amount <= 0:
            raise InvalidSavingGoalError("target_amount must be greater than zero")
        
        return amount
    
    @staticmethod
    def _validate_target_date(target_date: date) -> date:
        if not isinstance(target_date, date):
            raise InvalidSavingGoalError("target_date must be a date object")
        
        if target_date < date.today():
            raise InvalidSavingGoalError("target_date must be in the future")
        
        return target_date
    
    def update(
        self,
        name: str = None,
        target_amount: float = None,
        target_date: date = None,
        remarks: str = None
    ) -> None:
        """Update goal details with validation"""
        if name is not None:
            self.name = self._validate_name(name)
        
        if target_amount is not None:
            self.target_amount = self._validate_target_amount(target_amount)
        
        if target_date is not None:
            self.target_date = self._validate_target_date(target_date)
        
        if remarks is not None:
            self.remarks = remarks.strip() if isinstance(remarks, str) else ""
    
    def get_progress_percentage(self) -> float:
        """Calculate progress towards goal (0-100%)"""
        if self.target_amount <= 0:
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
