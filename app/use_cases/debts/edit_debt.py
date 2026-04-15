from app.domain.policies.p_FinancialCalculations import FinancialCalculationsPolicy


class EditDebtUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.finance_policy = FinancialCalculationsPolicy()

    def execute(self, debt_id: int, user_id: int, debt_data: dict):
        debt = self.uow.debts.get_by_id_and_user_id(debt_id, user_id)
        clean_data = self.finance_policy.validate_debt_editing(debt_data, debt)

        debt.update(
            name=clean_data.get("name"),
            lender=clean_data.get("lender"),
            principal=clean_data.get("principal"),
            interest_rate=clean_data.get("interest_rate"),
        )

        with self.uow.transaction():
            updated_debt = self.uow.debts.update(debt)

        return updated_debt
