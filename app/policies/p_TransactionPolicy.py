from app.policies.BasePolicy import BasePolicy
from app.utils.exceptions import PolicyError
import re

class TransactionPolicy(BasePolicy):
    # -----------------------------------------------------
    # INCOME
    # -----------------------------------------------------
    def validate_insert_income(self, data: dict) -> dict:
        """ 
            Validates Income insertion validated and cleaned data.

            Param:  
                data: Dictionary
                    * user_id : Integer
                    * category_id : Integer
                    * source : String
                    * amount : Float
                    * remarks : String
                    * received_date: Date
                    * payment_method : Enum("cash", "gcash", "bank", "card", "other")
            Return:
                clean : Dictionary
        """
        clean = self.create_resource(
            data,
            required=["user_id", 
                      "category_id", 
                      "source", 
                      "amount", 
                      "payment_method",
                      "received_date"
            ],
            allowed=[
                "user_id", 
                "category_id", 
                "source", 
                "amount", 
                "remarks", 
                "payment_method",
                "received_date"
            ]
        )

        clean["user_id"] = self.validate_numeric_values(
            value=clean["user_id"],
            field_name="User ID",
            allow_zero=False
        )

        clean["category_id"] = self.validate_numeric_values(
            value=clean["category_id"],
            field_name="Category ID",
            allow_zero=False
        )

        clean["source"] = self.validate_string(
            clean["source"],
            "Source",
            min_len=0
        )

        clean["amount"] = self.validate_numeric_values(
            value=clean["amount"],
            field_name="Amount",
            allow_zero=False
        )

        clean["received_date"] = self.validate_date_value(
            value=clean["received_date"],
            field_name="Received Date",
            allow_future=False,
            allow_past=True
        )

        clean["payment_method"] = self.validate_payment_method(
            clean["payment_method"]
        )

        clean["remarks"] = self.validate_string(
            clean["remarks"],
            "Remarks",
            min_len=0
        )

        return clean

    def validate_income_editing(self, data: dict, income: object) -> dict:
        """ 
            Validates Income editing returns validated and cleaned data.

            Param:  
                data: Dictionary
                    * category_id : Integer
                    * source : String
                    * payment_method : Enum("cash", "gcash", "bank", "card", "other")
                    * remarks : String
                income: Object
            Return:
                clean : Dictionary
        """
        if income is None:
            raise PolicyError("Income not found")

        clean = self.create_resource(
            data,
            allowed=["category_id", "source", "payment_method","remarks"]
        )

        if "category_id" in clean:
            clean["category_id"] =  self.validate_numeric_values(
                clean["category_id"],
                "Category ID",
                allow_zero=False
            )
        
        if "source" in clean:
            clean["source"] = self.validate_string(
                clean["source"],
                "Source",
                min_len=3
            )

        if "payment_method" in clean:
            clean["payment_method"] = self.validate_payment_method(clean["payment_method"])
        
        if "remarks" in clean["remarks"]:
            clean["remarks"] = self.validate_string(
                clean["remarks"],
                "Remarks",
                min_len=0
            )
        
        return clean
        
    def validate_income_deletion(self, income, debt_payment, saving_transaction):
        """ 
            Validates income deletion fields raises PolicyError
            Param:
                * income: Object
            Return:
                None
            Exception:
                Raise PolicyError when no income is found
                
        """
        if income is None:
            raise PolicyError("No Income record found")
        if debt_payment:
            raise PolicyError("Cannot Delete Income record used in DebtPayments")
        if saving_transaction:
            raise PolicyError("Cannot Delete Income record used in SavingTranasctions")

    # -----------------------------------------------------
    # EXPENSE
    # -----------------------------------------------------
    def validate_insert_expense(self, data: dict) -> dict:
        """ 
            Validates Expense insertion validated and cleaned data.

            Param:  
                data: Dictionary
                    * user_id : Integer
                    * category_id : Integer
                    * payee : String
                    * amount : Float
                    * expense_date : String
                    * payment_method : Enum("cash", "gcash", "bank", "card", "other")
                    * remarks : String
            Return:
                clean : Dictionary
        """
        clean = self.create_resource(
            data,
            required=[
                "user_id", 
                "category_id", 
                "payee", 
                "amount", 
                "expense_date", 
                "payment_method"
            ],
            allowed=[
                "user_id", 
                "category_id", 
                "payee", 
                "amount", 
                "expense_date", 
                "payment_method",
                "remarks"
            ],
        )

        clean["user_id"] = self.validate_numeric_values(
            value=clean["user_id"],
            field_name="User ID",
            allow_zero=False
        )

        clean["category_id"] = self.validate_numeric_values(
            value=clean["category_id"],
            field_name="Category ID",
            allow_zero=False
        )

        clean["payee"] = self.validate_string(
            clean["payee"],
            "Payee",
            min_len=0
        )

        clean["amount"] = self.validate_numeric_values(
            value=clean["amount"],
            field_name="Amount",
            allow_zero=False
        )

        clean["expense_date"] = self.validate_date_value(
            clean["expense_date"],
            "Expense Date",
            allow_future=False,
            allow_past=True
        )

        clean["payment_method"] = self.validate_payment_method(
            clean["payment_method"]
        )

        clean["remarks"] = self.validate_string(
            clean["remarks"],
            "Remarks",
            min_len=0
        )

        return clean

    def validate_expense_editing(self, data: dict, expense: object) -> dict:
        """ 
            Validates Expense editing returns validated and cleaned data.

            Param:  
                data: Dictionary
                    * category_id : Integer
                    * source : String
                    * payment_method : Enum("cash", "gcash", "bank", "card", "other")
                    * remarks : String
                income: Object
            Return:
                clean : Dictionary
        """
        if expense is None:
            raise PolicyError("Expense not found")

        clean = self.create_resource(
            data,
            allowed=[
                "category_id", 
                "payee", 
                "payment_method",
                "expense_date",
                "remarks"]
        )

        if "category_id" in clean:
            clean["category_id"] =  self.validate_numeric_values(
                clean["category_id"],
                "Category ID",
                allow_zero=False
            )
        
        if "payee" in clean:
            clean["payee"] = self.validate_string(
                clean["payee"],
                "Payee",
                min_len=3
            )

        if "payment_method" in clean:
            clean["payment_method"] = self.validate_payment_method(clean["payment_method"])
        
        if "expense_date" in clean:
            clean["expense_date"] = self.validate_date_value(
                clean["expense_date"],
                "Expense Date",
                allow_future=False,
                allow_past=True
            )

        if "remarks" in clean["remarks"]:
            clean["remarks"] = self.validate_string(
                clean["remarks"],
                "Remarks",
                min_len=0
            )
        
        return clean
        
    def validate_expense_deletion(self, expense, debt_payment, saving_transaction):
        """ 
            Validates Expense deletion fields raises PolicyError
            Param:
                * expense: Object
            Return:
                None
            Exception:
                Raise PolicyError when no expense is found
                
        """
        if expense is None:
            raise PolicyError("No Expense record found")
        if debt_payment:
            raise PolicyError("Cannot Delete Expense record used in DebtPayments")
        if saving_transaction:
            raise PolicyError("Cannot Delete Expense record used in SavingTranasctions")

    # -----------------------------------------------------
    # DEBT PAYMENTS
    # -----------------------------------------------------
    def validate_insert_debt_payment(self, data: dict) -> dict:
        """
        Validates debt_payment insertion validated and cleaned data.

        Param:
            data: Dictionary
                * user_id : Integer
                * debt_id : Integer
        Return: 
            clean : Dictionary
        """

        clean = self.create_resource(
            data,
            required=[
                "user_id",
                "debt_id",
            ],
            allowed=[
                "user_id",
                "debt_id",
                "expense_id"
            ]
        )
        clean["pymt_type"] = "deposit"
        clean["user_id"] = self.validate_numeric_values(
            clean["user_id"],
            "User ID",
            allow_zero=False
        )

        clean["debt_id"] = self.validate_numeric_values(
            clean["debt_id"],
            "Debt ID",
            allow_zero=False
        )
        
        clean["pymt_type"] = "deposit"

        clean["pymt_type"] = self.validate_payment_type(
            clean["pymt_type"]
        )

        return clean
        

    def validate_payment_method(self, payment_method) -> str:
            """ 
                Validates Payment Method value
                
                Valid Values:
                    * cash
                    * gcash
                    * bank
                    * card
                    * other
                Param:  
                    payment_method : String
                Return:
                    payment_method : String
                Exception:
                    Returns Policy error if payment_method value is invalid
            """
            payment_method = self.validate_string(payment_method, "Payment Method", min_len=4)
            if payment_method not in ("cash", "gcash", "bank", "card", "other"):
                raise PolicyError("Invalid Payment Method value")
            return payment_method

    def validate_payment_type(self, payment_type) -> str:
            """ 
                Validates Payment Method value
                
                Valid Values:
                    *deposit
                    *withdraw
                Param:  
                    payment_type : String
                Return:
                    payment_type : String
                Exception:
                    Returns Policy error if payment_type value is invalid
            """
            payment_type = self.validate_string(payment_type, "Payment Type", min_len=7)
            if payment_type not in ("deposit", "withdraw"):
                raise PolicyError("Invalid Payment Type value")
            return payment_type

