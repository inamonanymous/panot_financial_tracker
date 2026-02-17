from app.domain.policies.p_TransactionPolicy import TransactionPolicy


class EditIncomeUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()

    def execute(self, income_id: int, user_id: int, income_data: dict):
        income = self.uow.incomes.get_by_id_and_user_id(income_id, user_id)
        clean_data = self.tx_policy.validate_income_editing(income_data, income)

        if "category_id" in clean_data:
            category = self.uow.categories.get_by_id_and_user_id(clean_data["category_id"], user_id)
            if not category:
                raise Exception("Category not found or does not belong to user")
            income.category_id = clean_data["category_id"]

        income.update(
            name=clean_data.get("name"),
            source=clean_data.get("source"),
            amount=clean_data.get("amount"),
            payment_method=clean_data.get("payment_method"),
            remarks=clean_data.get("remarks"),
        )

        if "received_date" in clean_data:
            income.received_date = clean_data["received_date"]

        with self.uow.transaction():
            updated_income = self.uow.incomes.update(income)

        return updated_income
