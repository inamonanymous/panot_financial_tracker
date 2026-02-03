"""Transaction Analyzer - Analyzes income and expense patterns"""
from datetime import date, timedelta
from typing import List, Dict, Tuple
from app.domain.entities import Income, Expense


class TransactionAnalyzer:
    """
    Analyzes income and expense transactions for patterns and insights.
    
    Pure business logic, no database access.
    """
    
    @staticmethod
    def categorize_expenses_by_category(
        expenses: List[Expense],
    ) -> Dict[int, float]:
        """
        Group expenses by category and sum amounts.
        
        Args:
            expenses: List of expense entities
        
        Returns:
            Dictionary: {category_id: total_amount}
        """
        result = {}
        for expense in expenses:
            result[expense.category_id] = result.get(expense.category_id, 0) + expense.amount
        return result
    
    @staticmethod
    def categorize_income_by_category(
        incomes: List[Income],
    ) -> Dict[int, float]:
        """
        Group income by category and sum amounts.
        
        Args:
            incomes: List of income entities
        
        Returns:
            Dictionary: {category_id: total_amount}
        """
        result = {}
        for income in incomes:
            result[income.category_id] = result.get(income.category_id, 0) + income.amount
        return result
    
    @staticmethod
    def get_transactions_by_date_range(
        transactions: List[Income | Expense],
        start_date: date,
        end_date: date,
    ) -> List[Income | Expense]:
        """
        Filter transactions within a date range.
        
        Args:
            transactions: List of income or expense entities
            start_date: Filter start date (inclusive)
            end_date: Filter end date (inclusive)
        
        Returns:
            Filtered list of transactions
        """
        return [
            t for t in transactions
            if hasattr(t, 'received_date') and start_date <= t.received_date <= end_date
            or hasattr(t, 'expense_date') and start_date <= t.expense_date <= end_date
        ]
    
    @staticmethod
    def get_transactions_this_month(
        transactions: List[Income | Expense],
    ) -> List[Income | Expense]:
        """Get transactions for current month"""
        today = date.today()
        first_day = date(today.year, today.month, 1)
        
        # Last day of month
        if today.month == 12:
            last_day = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(today.year, today.month + 1, 1) - timedelta(days=1)
        
        return TransactionAnalyzer.get_transactions_by_date_range(
            transactions, first_day, last_day
        )
    
    @staticmethod
    def get_transactions_this_year(
        transactions: List[Income | Expense],
    ) -> List[Income | Expense]:
        """Get transactions for current year"""
        today = date.today()
        first_day = date(today.year, 1, 1)
        last_day = date(today.year, 12, 31)
        
        return TransactionAnalyzer.get_transactions_by_date_range(
            transactions, first_day, last_day
        )
    
    @staticmethod
    def calculate_average_transaction_amount(
        transactions: List[Income | Expense],
    ) -> float:
        """
        Calculate average transaction amount.
        
        Args:
            transactions: List of transactions
        
        Returns:
            Average amount (0 if no transactions)
        """
        if not transactions:
            return 0.0
        
        total = sum(t.amount for t in transactions)
        return float(total / len(transactions))
    
    @staticmethod
    def get_highest_transaction(
        transactions: List[Income | Expense],
    ) -> Tuple[Income | Expense, float] | None:
        """
        Get highest value transaction.
        
        Args:
            transactions: List of transactions
        
        Returns:
            Tuple of (transaction, amount) or None if empty
        """
        if not transactions:
            return None
        
        return max((t, t.amount) for t in transactions)
    
    @staticmethod
    def get_lowest_transaction(
        transactions: List[Income | Expense],
    ) -> Tuple[Income | Expense, float] | None:
        """
        Get lowest value transaction.
        
        Args:
            transactions: List of transactions
        
        Returns:
            Tuple of (transaction, amount) or None if empty
        """
        if not transactions:
            return None
        
        return min((t, t.amount) for t in transactions)
    
    @staticmethod
    def calculate_total(transactions: List[Income | Expense]) -> float:
        """
        Calculate total of all transactions.
        
        Args:
            transactions: List of transactions
        
        Returns:
            Total amount
        """
        return float(sum(t.amount for t in transactions))
    
    @staticmethod
    def get_spending_trend(
        expenses: List[Expense],
        num_months: int = 3,
    ) -> List[Tuple[str, float]]:
        """
        Get spending trend by month (last N months).
        
        Args:
            expenses: List of expense entities
            num_months: Number of months to analyze (default 3)
        
        Returns:
            List of (month_label, total_spent) tuples
        """
        today = date.today()
        months_data = []
        
        for i in range(num_months):
            # Go back i months
            month_date = today - timedelta(days=today.day)
            for _ in range(i):
                if month_date.month == 1:
                    month_date = date(month_date.year - 1, 12, 1)
                else:
                    month_date = date(month_date.year, month_date.month - 1, 1)
            
            # Sum expenses for this month
            month_label = month_date.strftime("%B %Y")
            month_total = sum(
                e.amount for e in expenses
                if e.expense_date.year == month_date.year
                and e.expense_date.month == month_date.month
            )
            
            months_data.append((month_label, float(month_total)))
        
        return list(reversed(months_data))
