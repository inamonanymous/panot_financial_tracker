class GetIncomeDetailsUseCase:
    """Get a specific income record with details."""
    
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, income_id: int, user_id: int):
        """
        Retrieve income details.
        
        Args:
            income_id: ID of the income
            user_id: ID of the user (for access control)
            
        Returns:
            dict with 'income' key
        """
        # Get the income and verify ownership
        income = self.uow.incomes.get_by_id_and_user_id(income_id, user_id)
        if income is None:
            raise Exception("Income not found")
        
        # Get the category
        category = self.uow.categories.get_by_id(income.category_id)
        
        return {
            "income": income,
            "category": category
        }