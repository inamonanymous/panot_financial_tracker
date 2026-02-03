"""
Domain Service for financial calculations and business rules.
Pure business logic - NO validation, NO persistence.
"""


class FinancialCalculator:
    """Calculates financial metrics for users."""
    
    def calculate_current_balance(
            self,
            total_income: float, 
            total_expense: float, 
            total_debt_payments: float,
            total_saving_deposits: float
    ) -> float:
        """
        Calculate user's current balance.
        
        Formula: Income - Expenses - Debt Payments - Savings Deposits
        
        Args:
            total_income: Sum of all income
            total_expense: Sum of all expenses
            total_debt_payments: Sum of all debt payments made
            total_saving_deposits: Sum of all savings deposits
            
        Returns:
            Float: Current balance (can be negative if user spent more than earned)
        """
        return float(
            total_income 
            - total_expense
            - total_debt_payments
            - total_saving_deposits
        )
    
    def calculate_available_balance(
            self,
            total_income: float,
            total_expense: float,
            total_debt_payments: float,
            total_saving_deposits: float,
            minimum_balance: float = 500.0
    ) -> float:
        """
        Calculate available balance (current balance - minimum required buffer).
        
        Args:
            total_income: Sum of all income
            total_expense: Sum of all expenses
            total_debt_payments: Sum of all debt payments made
            total_saving_deposits: Sum of all savings deposits
            minimum_balance: Minimum balance to maintain (default: 500php)
            
        Returns:
            Float: Available balance for spending
        """
        current_balance = self.calculate_current_balance(
            total_income,
            total_expense,
            total_debt_payments,
            total_saving_deposits
        )
        return max(current_balance - minimum_balance, 0.0)
    
    def calculate_savings_percentage(
            self,
            total_saving_deposits: float,
            total_income: float
    ) -> float:
        """
        Calculate what percentage of income is being saved.
        
        Args:
            total_saving_deposits: Sum of savings deposits
            total_income: Sum of income
            
        Returns:
            Float: Percentage (0-100)
        """
        if total_income == 0:
            return 0.0
        return (total_saving_deposits / total_income) * 100
    
    def calculate_expense_ratio(
            self,
            total_expense: float,
            total_income: float
    ) -> float:
        """
        Calculate what percentage of income is spent.
        
        Args:
            total_expense: Sum of expenses
            total_income: Sum of income
            
        Returns:
            Float: Percentage (0-100)
        """
        if total_income == 0:
            return 0.0
        return (total_expense / total_income) * 100
