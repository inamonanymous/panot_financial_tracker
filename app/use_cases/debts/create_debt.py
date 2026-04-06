from app.domain.policies.p_FinancialCalculations import FinancialCalculationsPolicy
from datetime import date

class CreateDebtUseCase:
    def __init__(self, uow):
        self.uow = uow
        self.finance_policy = FinancialCalculationsPolicy()

    def execute(self, debt_data: dict):
        # Create debt entity
        clean_debt = self.finance_policy.validate_insert_debt(debt_data)
        
        debt = self.uow.debts.create(**clean_debt)
        
        with self.uow.transaction():
            saved_debt = self.uow.debts.save(debt)

        return saved_debt