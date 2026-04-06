class GetUserExpenseUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, user_id: int):
        # Step 1: Get all expense for user
        expense_records = self.uow.expenses.get_all_by_user_id(user_id)
        
        # Step 2: Enrich with category names
        result = []
        for expense in expense_records:
            category = self.uow.categories.get_by_id(expense.category_id)
            result.append({
                "id": expense.id,
                "name": expense.name,
                "payee": expense.payee,
                "amount": expense.amount,
                "category_name": category.name if category else "Unknown",
                "expense_date": expense.expense_date,
                "payment_method": expense.payment_method,
                "remarks": expense.remarks,
                "created_at": expense.created_at
            })
        
        return result