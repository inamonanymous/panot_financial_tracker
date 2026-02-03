"""Saving Goal Analyzer - Analyzes savings progress"""
from datetime import date
from typing import List, Dict
from app.domain.entities import SavingGoal


class SavingGoalAnalyzer:
    """
    Analyzes savings goals and progress.
    
    Pure business logic, no database access.
    """
    
    @staticmethod
    def calculate_remaining_amount(goal: SavingGoal) -> float:
        """
        Calculate amount still needed to reach goal.
        
        Args:
            goal: SavingGoal entity
        
        Returns:
            Remaining amount (0 if already met)
        """
        remaining = goal.target_amount - goal.current_amount
        return max(0.0, float(remaining))
    
    @staticmethod
    def calculate_progress_percentage(goal: SavingGoal) -> float:
        """
        Calculate progress as percentage.
        
        Args:
            goal: SavingGoal entity
        
        Returns:
            Progress percentage (0-100)
        """
        if goal.target_amount <= 0:
            return 0.0
        return min(100.0, (goal.current_amount / goal.target_amount) * 100)
    
    @staticmethod
    def calculate_months_to_target(goal: SavingGoal, monthly_savings: float = 0) -> int:
        """
        Calculate estimated months to reach goal.
        
        Args:
            goal: SavingGoal entity
            monthly_savings: Average monthly savings rate
        
        Returns:
            Estimated months remaining (0 if no progress possible)
        """
        remaining = SavingGoalAnalyzer.calculate_remaining_amount(goal)
        
        if monthly_savings <= 0:
            return 0
        
        return int((remaining / monthly_savings) + 0.5)  # Round to nearest month
    
    @staticmethod
    def is_on_track(goal: SavingGoal, months_elapsed: int) -> bool:
        """
        Check if goal is on track based on time and progress.
        
        Args:
            goal: SavingGoal entity
            months_elapsed: Months since goal was created
        
        Returns:
            True if progress >= (months_elapsed / total_months) * target
        """
        today = date.today()
        
        if today >= goal.target_date:
            # Goal deadline has passed
            return goal.is_completed()
        
        # Calculate expected progress ratio
        start_date = date(today.year, today.month, 1)  # Approximate start
        total_days = (goal.target_date - start_date).days
        days_elapsed = (today - start_date).days
        
        if total_days <= 0:
            return True
        
        expected_progress_ratio = days_elapsed / total_days
        actual_progress_ratio = goal.current_amount / goal.target_amount
        
        return actual_progress_ratio >= expected_progress_ratio * 0.9  # 90% threshold
    
    @staticmethod
    def categorize_goals(goals: List[SavingGoal]) -> Dict[str, List[SavingGoal]]:
        """
        Categorize goals by status.
        
        Args:
            goals: List of SavingGoal entities
        
        Returns:
            Dictionary with keys: "completed", "on_track", "at_risk", "overdue"
        """
        categorized = {
            "completed": [],
            "on_track": [],
            "at_risk": [],
            "overdue": [],
        }
        
        for goal in goals:
            if goal.is_completed():
                categorized["completed"].append(goal)
            elif goal.is_overdue():
                categorized["overdue"].append(goal)
            else:
                categorized["at_risk"].append(goal)
        
        return categorized
    
    @staticmethod
    def get_highest_priority_goal(goals: List[SavingGoal]) -> SavingGoal | None:
        """
        Get goal closest to due date (highest priority).
        
        Args:
            goals: List of SavingGoal entities
        
        Returns:
            SavingGoal with closest target_date or None if empty
        """
        if not goals:
            return None
        
        active_goals = [g for g in goals if not g.is_completed()]
        
        if not active_goals:
            return None
        
        return min(active_goals, key=lambda g: g.target_date)
