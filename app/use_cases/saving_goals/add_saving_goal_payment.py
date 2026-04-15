from app.domain.policies.p_TransactionPolicy import TransactionPolicy
from app.domain.policies.p_CategoryPolicy import CategoryPolicy
from app.domain.policies.p_FinancialCalculations import FinancialCalculationsPolicy
from app.domain.entities.category import Category
from app.domain.entities.expense import Expense
from app.model.m_SavingTransactions import SavingTransactions as SavingTransactionsORM
from datetime import datetime

class AddSavingGoalPaymentUseCase:
    """Orchestrates adding a payment to a saving goal (category -> expense -> saving_transaction)

    The use-case expects repositories to be provided via a UnitOfWork instance
    that exposes `saving_goals`, `categories`, `expenses`, and `saving_transactions`.
    """

    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.tx_policy = TransactionPolicy()
        self.cat_policy = CategoryPolicy()
        self.fin_policy = FinancialCalculationsPolicy()

    def execute(self, saving_payment_data: dict, expense_data: dict):
        clean_saving = self.tx_policy.validate_insert_saving_transaction(saving_payment_data)
        user_id = clean_saving["user_id"]
        goal_id = clean_saving["goal_id"]

        with self.uow.transaction() as uow:
            goal = uow.saving_goals.get_by_id_and_user_id(goal_id, user_id)
            self.fin_policy.is_saving_goal_present(goal)

            # Category handling
            generated_category_string = f"Saving Goal Payment to {goal.name}"
            category = uow.categories.get_by_name_and_user_id(generated_category_string, user_id)

            if category is None:
                # create domain category and persist
                new_cat = Category(user_id=user_id, type="expense", name=generated_category_string)
                saved_category = uow.categories.save(new_cat)
                expense_data["category_id"] = saved_category.id
            else:
                expense_data["category_id"] = category.id

            expense_data["name"] = f"Saving Goal Payment - {goal.name}"
            expense_data["payee"] = expense_data["name"]

            cleaned_expense = self.tx_policy.validate_insert_expense(expense_data)

            # create domain Expense and persist
            exp_entity = Expense(
                user_id=cleaned_expense["user_id"],
                category_id=cleaned_expense["category_id"],
                name=cleaned_expense["name"],
                payee=cleaned_expense["payee"],
                amount=cleaned_expense["amount"],
                expense_date=cleaned_expense["expense_date"],
                payment_method=cleaned_expense.get("payment_method", "cash"),
                remarks=cleaned_expense.get("remarks", ""),
            )

            saved_expense = uow.expenses.save(exp_entity)

            # create saving transaction ORM and persist (using ORM class to match existing DB model)
            st_payload = {
                "user_id": user_id,
                "goal_id": goal_id,
                "txt_type": "deposit",
                "expense_id": saved_expense.id,
            }
            st_orm = SavingTransactionsORM(**st_payload)
            saved_st = uow.saving_transactions.save(st_orm)

            return saved_st