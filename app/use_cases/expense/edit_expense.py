from app.domain.policies.p_TransactionPolicy import TransactionPolicy


class EditExpenseUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()

    def execute(self, expense_id: int, user_id: int, expense_data: dict):
        expense = self.uow.expenses.get_by_id_and_user_id(expense_id, user_id)
        clean_data = self.tx_policy.validate_expense_editing(expense_data, expense)

        if "category_id" in clean_data:
            category = self.uow.categories.get_by_id_and_user_id(clean_data["category_id"], user_id)
            if not category:
                raise Exception("Category not found or does not belong to user")
            expense.category_id = clean_data["category_id"]

        expense.update(
            name=clean_data.get("name"),
            payee=clean_data.get("payee"),
            amount=clean_data.get("amount"),
            payment_method=clean_data.get("payment_method"),
            remarks=clean_data.get("remarks"),
        )

        if "expense_date" in clean_data:
            expense.expense_date = clean_data["expense_date"]

        with self.uow.transaction():
            updated_expense = self.uow.expenses.update(expense)

        return updated_expense
