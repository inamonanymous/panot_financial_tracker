from app.domain.policies.p_TransactionPolicy import TransactionPolicy
from app.domain.entities.expense import Expense

class CreateExpenseUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()

    def execute(self, expense_data: dict):
        clean_expense = self.tx_policy.validate_insert_expense(expense_data)

        category = self.uow.categories.get_by_id_and_user_id(clean_expense["category_id"], clean_expense["user_id"])
        if not category:
            raise Exception("Category not found or does not belong to user")
        
        expense = Expense(
            user_id=clean_expense["user_id"],
            category_id=clean_expense["category_id"],
            payee=clean_expense["payee"],
            amount=clean_expense["amount"],
            expense_date=clean_expense["expense_date"],
            payment_method=clean_expense["payment_method"],
            remarks=clean_expense.get("remarks", "")
        )

        with self.uow.transaction():
            saved = self.uow.expenses.save(expense)

        return saved