from app.domain.policies.p_TransactionPolicy import TransactionPolicy
from app.domain.entities.income import Income

class CreateIncomeUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()

    def execute(self, income_data: dict):
        clean_income = self.tx_policy.validate_insert_income(income_data)

        category = self.uow.categories.get_by_id_and_user_id(clean_income["category_id"], clean_income["user_id"])
        if not category:
            raise Exception("Category not found or does not belong to user")
        
        income = Income(
            user_id=clean_income["user_id"],
            category_id=clean_income["category_id"],
            source=clean_income["source"],
            amount=clean_income["amount"],
            received_date=clean_income["received_date"],
            payment_method=clean_income["payment_method"],
            remarks=clean_income.get("remarks", "")
        )

        with self.uow.transaction():
            saved = self.uow.incomes.save(income)

        return saved