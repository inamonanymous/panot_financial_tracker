from app.domain.policies.p_CategoryPolicy import CategoryPolicy
from app.domain.services.transaction_analyzer import TransactionAnalyzer


class DeleteCategoryUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.category_policy = CategoryPolicy()
        self.transaction_analyzer = TransactionAnalyzer()

    def execute(self, category_id: int, user_id: int):
        category = self.uow.categories.get_by_id_and_user_id(category_id, user_id)
        user_incomes = self.uow.incomes.get_all_by_user_id(user_id)
        user_expenses = self.uow.expenses.get_all_by_user_id(user_id)
        category_in_use = self.transaction_analyzer.is_category_used_by_transactions(
            category_id=category_id,
            incomes=user_incomes,
            expenses=user_expenses,
        )
        self.category_policy.validate_category_deletion(
            category=category,
            current_user_id=user_id,
            category_in_use_checker=category_in_use,
        )

        with self.uow.transaction():
            deleted = self.uow.categories.delete(category.id)
        return deleted