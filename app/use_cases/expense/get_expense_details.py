class GetExpenseDetailsUseCase:
    """Get a specific expense record with details."""
    
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, expense_id: int, user_id: int):
        """
        Retrieve expense details.
        
        Args:
            expense_id: ID of the expense
            user_id: ID of the user (for access control)
            
        Returns:
            dict with 'expense' key
        """
        # Get the expense and verify ownership
        expense = self.uow.expenses.get_by_id_and_user_id(expense_id, user_id)
        if expense is None:
            raise Exception("Expense not found")
        
        # Get the category
        category = self.uow.categories.get_by_id(expense.category_id)
        
        return {
            "expense": expense,
            "category": category
        }