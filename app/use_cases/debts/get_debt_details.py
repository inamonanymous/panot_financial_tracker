class GetDebtDetailsUseCase:
    """Get a specific debt with all its payment history."""
    
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, debt_id: int, user_id: int):
        """
        Retrieve debt details and all associated payments.
        
        Args:
            debt_id: ID of the debt
            user_id: ID of the user (for access control)
            
        Returns:
            dict with 'debt' and 'payments' keys
        """
        # Get the debt and verify ownership
        debt = self.uow.debts.get_by_id_and_user_id(debt_id, user_id)
        if debt is None:
            raise Exception("Debt not found")
        
        # Get all payments for this debt
        payments = self.uow.debt_payments.get_by_debt_id_and_user_id(debt_id, user_id)
        
        return {
            "debt": debt,
            "payments": payments if payments else []
        }
