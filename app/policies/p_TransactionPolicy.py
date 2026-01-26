from app.policies.BasePolicy import BasePolicy
from app.utils.exceptions import PolicyError
import re

class TransactionPolicy(BasePolicy):
    def validate_insert_debt_payment(self, data: dict) -> dict:
        """
        Validates debt_payment insertion validated and cleaned data.

        Param:
            data: Dictionary
                * user_id : Integer
                * debt_id : Integer
                * amount : Float
                * payment_date : Date  
                * remarks : String  
        Return: 
            clean : Dictionary
        """
        clean = self.create_resource(
            data,
            required=[
                "debt_id",
                "user_id"
                "amount",
                "payment_date",
                "remarks"
            ],
            allowed=[
                "debt_id",
                "user_id"
                "amount",
                "payment_date",
                "remarks"
            ]
        )

        clean["user_id"] = self.validate_numeric_values(
            value=clean["user_id"],
            field_name="User ID",
            allow_zero=False
        )

        clean["debt_id"] = self.validate_numeric_values(
            value=clean["debt_id"],
            field_name="Debt ID",
            allow_zero=False
        )
        clean["amount"] = self.validate_numeric_values(
            value=clean["amount"],
            field_name="Amount",
            allow_zero=False
        )
        clean["payment_date"] = self.validate_date_value(
            clean["payment_date"],
            "Payment Date",
            allow_future=False,
            allow_past=True
        )
        clean["remarks"] = self.validate_string(
            clean["remarks"],
            "Remarks",
            min_len=1
        )

        if clean["amount"] < 0:
            raise PolicyError("Cannot accept netagive values")

        return clean

