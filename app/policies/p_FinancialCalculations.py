from app.policies.BasePolicy import BasePolicy
from app.utils.exceptions import PolicyError

class FinancialCalculationsPolicy(BasePolicy):

    def caculate_current_amount_of_user(
            self,
            total_income: float, 
            total_expense: float, 
            total_debt_payments: float,
            total_saving_deposits:float
    ) -> float:

        return float(
            total_income 
             - total_expense
             - total_debt_payments
             - total_saving_deposits
        )

