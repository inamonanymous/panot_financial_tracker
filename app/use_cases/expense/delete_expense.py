class DeleteExpenseUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, expense_id: int, user_id: int):
        expense = self.uow.expenses.get_by_id_and_user_id(expense_id, user_id)
        if expense is None:
            raise Exception("Expense not found")

        with self.uow.transaction():
            deleted = self.uow.expenses.delete(expense.id)

        if not deleted:
            raise Exception("Failed to delete expense")

        return True