from app.domain.policies.p_TransactionPolicy import TransactionPolicy

class CreateIncomeUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()

    def execute(self, income_data: dict):
        clean_income = self.tx_policy.validate_insert_income(income_data)

        category = self.uow.categories.get_by_id_and_user_id(clean_income["category_id"], clean_income["user_id"])
        if not category:
            raise Exception("Category not found or does not belong to user")

        income = self.uow.incomes.create(**clean_income)

        with self.uow.transaction():
            saved = self.uow.incomes.save(income)

        return saved