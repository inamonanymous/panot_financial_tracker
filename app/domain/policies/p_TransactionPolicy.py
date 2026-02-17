from app.domain.policies.BasePolicy import BasePolicy
from app.utils.exceptions import PolicyError
import re

class TransactionPolicy(BasePolicy):
    # INCOME
    def validate_insert_income(self, data: dict) -> dict:
        clean = self.create_resource(
            data,
            required=["user_id", "category_id", "name", "source", "amount", "payment_method", "received_date"],
            allowed=["user_id", "category_id", "name", "source", "amount", "remarks", "payment_method", "received_date"]
        )

        clean["user_id"] = self.validate_id_values(value=clean["user_id"], field_name="User ID")
        clean["category_id"] = self.validate_id_values(value=clean["category_id"], field_name="Category ID")
        clean["name"] = self.validate_string(clean["name"], "Income Name", min_len=1)
        clean["source"] = self.validate_string(clean["source"], "Income Source", min_len=1)
        clean["amount"] = self.validate_numeric_values(value=clean["amount"], field_name="Amount", allow_zero=False)
        clean["received_date"] = self.validate_date_value(value=clean["received_date"], field_name="Received Date", allow_future=False, allow_past=True)
        clean["payment_method"] = self.validate_payment_method(clean["payment_method"])
        clean["remarks"] = self.validate_string(clean.get("remarks", ""), "Remarks", min_len=0)

        return clean

    def validate_income_editing(self, data: dict, income: object) -> dict:
        if income is None:
            raise PolicyError("Income not found")

        clean = self.update_resource(data, allowed=["category_id", "name", "source", "amount", "received_date", "payment_method", "remarks"])

        if "category_id" in clean:
            clean["category_id"] =  self.validate_id_values(clean["category_id"], "Category ID")
        if "name" in clean:
            clean["name"] = self.validate_string(clean["name"], "Income Name", min_len=1)
        if "source" in clean:
            clean["source"] = self.validate_string(clean["source"], "Income Source", min_len=1)
        if "amount" in clean:
            clean["amount"] = self.validate_numeric_values(clean["amount"], "Amount", allow_zero=False)
        if "received_date" in clean:
            clean["received_date"] = self.validate_date_value(clean["received_date"], "Received Date", allow_future=False, allow_past=True)
        if "payment_method" in clean:
            clean["payment_method"] = self.validate_payment_method(clean["payment_method"])
        if "remarks" in clean:
            clean["remarks"] = self.validate_string(clean["remarks"], "Remarks", min_len=0)

        return clean

    def validate_income_deletion(self, income, debt_payment, saving_transaction):
        if income is None:
            raise PolicyError("No Income record found")
        if debt_payment:
            raise PolicyError("Cannot Delete Income record used in DebtPayments")
        if saving_transaction:
            raise PolicyError("Cannot Delete Income record used in SavingTranasctions")

    # EXPENSE
    def validate_insert_expense(self, data: dict) -> dict:
        clean = self.create_resource(
            data,
            required=["user_id", "category_id", "name", "payee", "amount", "expense_date", "payment_method"],
            allowed=["user_id", "category_id", "name", "payee", "amount", "expense_date", "payment_method", "remarks"],
        )

        clean["user_id"] = self.validate_id_values(value=clean["user_id"], field_name="User ID")
        clean["category_id"] = self.validate_id_values(value=clean["category_id"], field_name="Category ID")
        clean["name"] = self.validate_string(clean["name"], "Expense Name", min_len=1)
        clean["payee"] = self.validate_string(clean["payee"], "Expense Payee", min_len=1)
        clean["amount"] = self.validate_numeric_values(value=clean["amount"], field_name="Amount", allow_zero=False)
        clean["expense_date"] = self.validate_date_value(clean["expense_date"], "Expense Date", allow_future=False, allow_past=True)
        clean["payment_method"] = self.validate_payment_method(clean["payment_method"])
        clean["remarks"] = self.validate_string(clean.get("remarks", ""), "Remarks", min_len=0)

        return clean

    def validate_expense_editing(self, data: dict, expense: object) -> dict:
        if expense is None:
            raise PolicyError("Expense not found")

        clean = self.update_resource(data, allowed=["category_id", "name", "payee", "amount", "payment_method", "expense_date", "remarks"])

        if "category_id" in clean:
            clean["category_id"] =  self.validate_id_values(clean["category_id"], "Category ID")
        if "name" in clean:
            clean["name"] = self.validate_string(clean["name"], "Expense Name", min_len=1)
        if "payee" in clean:
            clean["payee"] = self.validate_string(clean["payee"], "Expense Payee", min_len=1)
        if "amount" in clean:
            clean["amount"] = self.validate_numeric_values(clean["amount"], "Amount", allow_zero=False)
        if "payment_method" in clean:
            clean["payment_method"] = self.validate_payment_method(clean["payment_method"])
        if "expense_date" in clean:
            clean["expense_date"] = self.validate_date_value(clean["expense_date"], "Expense Date", allow_future=False, allow_past=True)
        if "remarks" in clean:
            clean["remarks"] = self.validate_string(clean["remarks"], "Remarks", min_len=0)

        return clean

    def validate_expense_deletion(self, expense, debt_payment, saving_transaction):
        if expense is None:
            raise PolicyError("No Expense record found")
        if debt_payment:
            raise PolicyError("Cannot Delete Expense record used in DebtPayments")
        if saving_transaction:
            raise PolicyError("Cannot Delete Expense record used in SavingTranasctions")

    # DEBT PAYMENTS
    def validate_insert_debt_payment(self, data: dict) -> dict:
        clean = self.create_resource(
            data,
            required=["user_id","debt_id"],
            allowed=["user_id","debt_id","expense_id"]
        )
        clean["pymt_type"] = "deposit"
        clean["user_id"] = self.validate_id_values(clean["user_id"], "User ID")
        clean["debt_id"] = self.validate_id_values(clean["debt_id"], "Debt ID")
        clean["pymt_type"] = self.validate_payment_type(clean["pymt_type"])
        return clean

    def validate_payment_method(self, payment_method) -> str:
            payment_method = self.validate_string(payment_method, "Payment Method", min_len=4)
            if payment_method not in ("cash", "gcash", "bank", "card", "other"):
                raise PolicyError("Invalid Payment Method value")
            return payment_method

    def validate_payment_type(self, payment_type) -> str:
            payment_type = self.validate_string(payment_type, "Payment Type", min_len=7)
            if payment_type not in ("deposit", "withdraw"):
                raise PolicyError("Invalid Payment Type value")
            return payment_type
