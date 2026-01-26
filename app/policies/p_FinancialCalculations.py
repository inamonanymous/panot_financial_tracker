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
    

    def validate_insert_debt(self, data: dict) -> dict:
        """
        Validates debt insertion with validated and cleaned data.

        Param:
            data: Dictionary
                * user_id : String
                * lender : String 
                * principal : Float 
                * interest_rate : Float 
                * start_date : Date 
                * due_date : Date 
        Return: 
            Debts Instance
        """

        clean = self.create_resource(
            data,
            required=[
                "user_id",
                "lender", 
                "principal", 
                "interest_rate", 
                "start_date", 
                "due_date"
                ],
            allowed=[
                "user_id", 
                "lender", 
                "principal", 
                "interest_rate", 
                "start_date", 
                "due_date"
                ]
        )
        
        clean["principal"] = self.validate_numeric_values(
            value=clean["principal"], 
            field_name="Principal",
            allow_zero=False
        )
        clean["interest_rate"] = self.validate_numeric_values(
            clean["interest_rate"],
            field_name="Interest Rate",
            allow_zero=False
        )
        self.validate_allowed_debt_amounts(
            principal=clean["principal"],
            interest_rate=clean["interest_rate"]
        )

        return clean
    
    def validate_debt_editing(self, data: dict, debt: object) -> dict:
        """
        Validates debt insertion with validated and cleaned data.

        Param:
            data: Dictionary
                * lender : String 
                * principal : Float 
                * interest_rate : Float 
            debt: Object
        Return: 
            clean : Dictionary
        """
        if debt is None:
            raise PolicyError("Debt not found")
        
        clean = self.update_resource(
            data,
            allowed=["lender", "principal", "interest_rate"]
        )

        if "lender" in clean:
            clean["lender"] = self.validate_string(clean["lender"], "Lender", 3)

        if "principal" in clean:
            clean["principal"] = self.validate_numeric_values(
                value=clean["principal"], 
                field_name="Principal",
                allow_zero=False
            )
        if "interest_rate" in clean:
            clean["interest_rate"] = self.validate_numeric_values(
                clean["interest_rate"],
                field_name="Interest Rate",
                allow_zero=False
            )

        self.validate_allowed_debt_amounts(
            principal=clean["principal"],
            interest_rate=clean["interest_rate"]
        )

        return clean
    
    def validate_allowed_debt_amounts(self, principal=None, interest_rate=None):
        """ 
            Validates debt amount fields raises PolicyError
            Param:
                * principal : Float
                * interest_rate : Float
            Return:
                None
            Exception:
                Raise PolicyError when principal is less than 100
                Raise PolicyError when interest_rate is greater than 6
                Raise PolicyError when interest_rate is negative number
        """
        if principal is not None:
            if principal < 100:
                raise PolicyError("Principal should not be less than 100php")
        if interest_rate is not None:
            if interest_rate > 6:
                raise PolicyError("Interest rate should not exceed by 6%")
            if interest_rate < 0:
                raise PolicyError("Interest rate should not accept negative values")
            
        
    def validate_debt_deletion(debt: object, current_user_id):
        """ 
            Validates debt deletion fields raises PolicyError
            Param:
                * debt: Object
                * current_user_id : Int
            Return:
                None
            Exception:
                Raise PolicyError when no debt is found
                Raise PolicyError when current user's target debt does not belong to user
        """

        if debt is None:
            raise PolicyError("No debt record found")
        if debt.user_id != current_user_id:
            raise PolicyError(f"Cannot delete debt user don't own '{debt.name}'")
        


