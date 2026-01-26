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
        """ 
            Calculates current amount of a user in the record and returns difference of expense, debt payments, and saving deposits from income
            Param:
                * total_income: Float
                * total_expense: Float
                * total_debt_payments: Float
                * total_saving_deposits: Float
            Return:
                Float
        """


        return float(
            total_income 
             - total_expense
             - total_debt_payments
             - total_saving_deposits
        )
    
    

