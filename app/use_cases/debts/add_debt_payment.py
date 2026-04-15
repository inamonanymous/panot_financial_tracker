from app.domain.policies.p_TransactionPolicy import TransactionPolicy
from app.domain.policies.p_CategoryPolicy import CategoryPolicy

class AddDebtPaymentUseCase:
    """Add a payment to an existing debt by creating an expense and debt payment record."""

    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()
        self.cat_policy = CategoryPolicy()

    def execute(self, debt_id: int, user_id: int, payment_data: dict):
        """
        Add a payment to a debt.

        Args:
            debt_id: ID of the debt to add payment to
            user_id: ID of the user making the payment
            payment_data: dict with 'amount', 'payment_date', 'payment_method', 'remarks'

        Returns:
            Created debt payment record
        """
        # Validate debt ownership
        debt = self._validate_debt_ownership(debt_id, user_id)

        # Get or create debt payment category
        category = self._get_or_create_debt_payment_category(debt, user_id)

        # Prepare and create expense
        expense_data = self._prepare_expense_data(user_id, category, debt, payment_data)
        expense = self._create_expense(expense_data)

        # Prepare and create debt payment
        debt_payment_data = self._prepare_debt_payment_data(user_id, debt_id)
        debt_payment = self._create_debt_payment(debt_payment_data)

        # Save both records in transaction
        return self._save_payment_records(expense, debt_payment)

    def _validate_debt_ownership(self, debt_id: int, user_id: int):
        """Validate that the debt exists and belongs to the user."""
        debt = self.uow.debts.get_by_id_and_user_id(debt_id, user_id)
        if debt is None:
            raise Exception("Debt not found")
        return debt

    def _get_or_create_debt_payment_category(self, debt, user_id: int):
        """Get existing debt payment category or create a new one."""
        category_name = f"Debt payment to {debt.lender}"
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

    def _prepare_expense_data(self, user_id: int, category, debt, payment_data: dict) -> dict:
        """Prepare expense data dictionary."""
        return {
            'user_id': user_id,
            'category_id': category.id,
            'name': f"Debt payment - {debt.lender}",
            'payee': f"Debt payment - {debt.lender}",
            'amount': payment_data['amount'],
            'expense_date': payment_data['payment_date'],
            'payment_method': payment_data.get('payment_method', 'cash'),
            'remarks': payment_data.get('remarks', '')
        }

    def _create_expense(self, expense_data: dict):
        """Validate and create expense entity."""
        clean_expense = self.tx_policy.validate_insert_expense(expense_data)
        return self.uow.expenses.create(**clean_expense)

    def _prepare_debt_payment_data(self, user_id: int, debt_id: int) -> dict:
        """Prepare debt payment data dictionary."""
        return {
            'user_id': user_id,
            'debt_id': debt_id,
            'pymt_type': 'deposit'
        }

    def _create_debt_payment(self, debt_payment_data: dict):
        """Validate and create debt payment entity."""
        clean_debt_payment = self.tx_policy.validate_insert_debt_payment(debt_payment_data)
        return self.uow.debt_payments.create(**clean_debt_payment)

    def _save_payment_records(self, expense, debt_payment):
        """Save both expense and debt payment records in a transaction."""
        with self.uow.transaction():
            saved_expense = self.uow.expenses.save(expense)
            # Update debt payment with the saved expense ID
            debt_payment.expense_id = saved_expense.id
            saved_payment = self.uow.debt_payments.save(debt_payment)
        return saved_payment