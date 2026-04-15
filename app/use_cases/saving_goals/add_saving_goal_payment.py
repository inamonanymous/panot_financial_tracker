from app.domain.policies.p_TransactionPolicy import TransactionPolicy
from app.domain.policies.p_CategoryPolicy import CategoryPolicy
from app.domain.policies.p_FinancialCalculations import FinancialCalculationsPolicy

class AddSavingGoalPaymentUseCase:
    """Add a payment to a saving goal by creating an expense and saving transaction record."""

    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()
        self.cat_policy = CategoryPolicy()
        self.fin_policy = FinancialCalculationsPolicy()

    def execute(self, saving_payment_data: dict, expense_data: dict):
        """
        Add a payment to a saving goal.

        Args:
            saving_payment_data: dict with 'user_id', 'goal_id', 'txt_type'
            expense_data: dict with expense details

        Returns:
            Created saving transaction record
        """
        # Validate saving transaction data
        clean_saving = self.tx_policy.validate_insert_saving_transaction(saving_payment_data)
        user_id = clean_saving["user_id"]
        goal_id = clean_saving["goal_id"]

        # Validate saving goal ownership
        goal = self._validate_saving_goal_ownership(goal_id, user_id)

        # Get or create saving goal payment category
        category = self._get_or_create_saving_goal_payment_category(goal, user_id)

        # Prepare and create expense
        expense_data = self._prepare_expense_data(user_id, category, goal, expense_data)
        expense = self._create_expense(expense_data)
        print("Created expense with ID:", expense)
        # Prepare and create saving transaction
        saving_transaction_data = self._prepare_saving_transaction_data(user_id, goal_id, expense)
        saving_transaction = self._create_saving_transaction(saving_transaction_data)

        # Save both records in transaction
        return self._save_payment_records(expense, saving_transaction)

    def _validate_saving_goal_ownership(self, goal_id: int, user_id: int):
        """Validate that the saving goal exists and belongs to the user."""
        goal = self.uow.saving_goals.get_by_id_and_user_id(goal_id, user_id)
        self.fin_policy.is_saving_goal_present(goal)
        return goal

    def _get_or_create_saving_goal_payment_category(self, goal, user_id: int):
        """Get existing saving goal payment category or create a new one."""
        category_name = f"Saving Goal Payment to {goal.name}"
        category = self.uow.categories.get_by_name_and_user_id(category_name, user_id)

        if category is None:
            # Create category data and validate
            category_data = {
                'user_id': user_id,
                'type': 'expense',
                'name': category_name
            }
            clean_category = self.cat_policy.validate_insert_category(category_data)
            # Check for duplicate category name
            duplicate_category = self.uow.categories.get_by_name_and_user_id(clean_category["name"], clean_category["user_id"])
            self.cat_policy.validate_duplicate_category_name_entry(duplicate_category)
            category = self.uow.categories.create(**clean_category)

        return category

    def _prepare_expense_data(self, user_id: int, category, goal, expense_data: dict) -> dict:
        """Prepare expense data dictionary."""
        return {
            'user_id': user_id,
            'category_id': category.id,
            'name': f"Saving Goal Payment - {goal.name}",
            'payee': f"Saving Goal Payment - {goal.name}",
            'amount': expense_data['amount'],
            'expense_date': expense_data['expense_date'],
            'payment_method': expense_data.get('payment_method', 'cash'),
            'remarks': expense_data.get('remarks', '')
        }

    def _create_expense(self, expense_data: dict):
        """Validate and create expense entity."""
        clean_expense = self.tx_policy.validate_insert_expense(expense_data)
        return self.uow.expenses.create(**clean_expense)

    def _prepare_saving_transaction_data(self, user_id: int, goal_id: int, expense) -> dict:
        """Prepare saving transaction data dictionary."""
        # Expense is not saved yet, so expense.id will be None until persisted.
        return {
            'user_id': user_id,
            'goal_id': goal_id,
            'txt_type': 'deposit',
        }

    def _create_saving_transaction(self, saving_transaction_data: dict):
        """Validate and create saving transaction entity."""
        clean_saving_transaction = self.tx_policy.validate_insert_saving_transaction(saving_transaction_data)
        return self.uow.saving_transactions.create(**clean_saving_transaction)

    def _save_payment_records(self, expense, saving_transaction):
        """Save both expense and saving transaction records in a transaction."""
        with self.uow.transaction():
            saved_expense = self.uow.expenses.save(expense)
            # Update saving transaction with the saved expense ID
            saving_transaction.expense_id = saved_expense.id
            saved_transaction = self.uow.saving_transactions.save(saving_transaction)
        return saved_transaction