"""Net Worth Calculator - Pure business logic"""
from typing import List
from app.domain.entities import Income, Expense, Debt, SavingGoal


class NetWorthCalculator:
    """
    Calculates user's financial net worth.
    
    Formula:
        Net Worth = Total Income - Total Expenses - Total Debt Principal + Savings
    
    Pure business logic, no database access.
    """
    
    @staticmethod
    def calculate_net_worth(
        total_income: float,
        total_expenses: float,
        total_debt_principal: float,
        total_savings: float = 0.0,
    ) -> float:
        """
        Calculate net worth from aggregate amounts.
        
        Args:
            total_income: Sum of all income
            total_expenses: Sum of all expenses
            total_debt_principal: Sum of active debt principals
            total_savings: Sum of savings deposits (optional)
        
        Returns:
            Net worth amount (can be negative)
        
        Example:
            net_worth = NetWorthCalculator.calculate_net_worth(
                total_income=10000,
                total_expenses=3000,
                total_debt_principal=2000,
                total_savings=1500
            )
            # Result: 10000 - 3000 - 2000 + 1500 = 6500
        """
        return float(total_income - total_expenses - total_debt_principal + total_savings)
    
    @staticmethod
    def calculate_net_value(total_income: float, total_expense:float, total_saving_deposits: float) -> float:
        """
        Calculate net value (income - expenses - saving deposits).
        
        Args:
            total_income: Sum of all income
            total_expense: Sum of all expenses
            total_saving_deposits: Sum of all saving deposits
        
        Returns:
            Net value amount (can be negative)
        
        Example:
            net_value = NetWorthCalculator.calculate_net_value(
                total_income=10000,
                total_expense=3000,
                total_saving_deposits=1500
            )
            # Result: 10000 - 3000 - 1500 = 5500
        """
        return float(total_income - total_expense - total_saving_deposits)

    @staticmethod
    def calculate_net_income(total_income: float, total_expenses: float) -> float:
        """
        Calculate net income (income - expenses, excluding debts).
        
        Args:
            total_income: Sum of income
            total_expenses: Sum of expenses
        
        Returns:
            Net income amount
        """
        return float(total_income - total_expenses)
    
    @staticmethod
    def calculate_savings_rate(total_income: float, total_savings: float) -> float:
        """
        Calculate savings rate as percentage.
        
        Args:
            total_income: Sum of income
            total_savings: Sum of savings deposits
        
        Returns:
            Savings rate percentage (0-100)
        """
        if total_income <= 0:
            return 0.0
        return min(100.0, (total_savings / total_income) * 100)
    
    @staticmethod
    def calculate_expense_ratio(total_income: float, total_expenses: float) -> float:
        """
        Calculate expense-to-income ratio as percentage.
        
        Args:
            total_income: Sum of income
            total_expenses: Sum of expenses
        
        Returns:
            Expense ratio percentage (0-100+)
        """
        if total_income <= 0:
            return 0.0
        return (total_expenses / total_income) * 100
    
    @staticmethod
    def calculate_debt_to_income_ratio(total_debt_principal: float, total_income: float) -> float:
        """
        Calculate debt-to-income ratio as percentage.
        
        Args:
            total_debt_principal: Sum of active debt principals
            total_income: Sum of income
        
        Returns:
            Debt-to-income ratio percentage
        """
        if total_income <= 0:
            return 0.0
        return (total_debt_principal / total_income) * 100
