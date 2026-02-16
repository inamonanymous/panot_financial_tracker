from app.domain.policies.p_TransactionPolicy import TransactionPolicy
from app.domain.policies.p_CategoryPolicy import CategoryPolicy
from app.domain.policies.p_FinancialCalculations import FinancialCalculationsPolicy
from app.domain.entities.category import Category
from app.domain.entities.expense import Expense
from app.model.m_DebtPayments import DebtPayments as DebtPaymentsORM
from datetime import datetime

class CreateDebtPaymentUseCase:
    """Orchestrates creating a debt payment (category -> expense -> debt_payment)

    The use-case expects repositories to be provided via a UnitOfWork instance
    that exposes `debts`, `categories`, `expenses`, and `debt_payments`.
    """

    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()
        self.cat_policy = CategoryPolicy()
        self.fin_policy = FinancialCalculationsPolicy()

    def execute(self, debt_data: dict, expense_data: dict):
        clean_debt = self.tx_policy.validate_insert_debt_payment(debt_data)
        user_id = clean_debt["user_id"]
        debt_id = clean_debt["debt_id"]

        with self.uow.transaction() as uow:
            debt = uow.debts.get_by_id_and_user_id(debt_id, user_id)
            self.fin_policy.is_debt_present(debt)

            # Category handling
            generated_category_string = f"Debt payment to {debt.lender}"
            category = uow.categories.get_by_name_and_user_id(generated_category_string, user_id)

            if category is None:
                # create domain category and persist
                new_cat = Category(user_id=user_id, type="expense", name=generated_category_string)
                saved_category = uow.categories.save(new_cat)
                expense_data["category_id"] = saved_category.id
            else:
                expense_data["category_id"] = category.id

            expense_data["payee"] = debt.lender

            cleaned_expense = self.tx_policy.validate_insert_expense(expense_data)

            # create domain Expense and persist
            exp_entity = Expense(
                user_id=cleaned_expense["user_id"],
                category_id=cleaned_expense["category_id"],
                payee=cleaned_expense["payee"],
                amount=cleaned_expense["amount"],
                expense_date=cleaned_expense["expense_date"],
                payment_method=cleaned_expense.get("payment_method", "cash"),
                remarks=cleaned_expense.get("remarks", ""),
            )

            saved_expense = uow.expenses.save(exp_entity)

            # create debt payment ORM and persist (using ORM class to match existing DB model)
            dp_payload = {
                "user_id": user_id,
                "debt_id": debt_id,
                "expense_id": saved_expense.id,
                "pymt_type": "deposit",
            }
            dp_orm = DebtPaymentsORM(**dp_payload)
            saved_dp = uow.debt_payments.save(dp_orm)

            return saved_dp
