from app.service import db
from app.model.m_DebtPayments import DebtPayments
from app.model.m_Debts import Debts
from app.model.m_Categories import Categories
from app.model.m_Income import Income
from app.model.m_Expenses import Expenses
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions.ServiceError import ServiceError
from app.utils.exceptions.PolicyError import PolicyError
from app.service.BaseService import BaseService
from sqlalchemy import func

class DebtPaymentsService(BaseService):
    def insert_debt_payment(self, debt_data: dict, expense_data: dict) -> object:
        """
        Creates a new debt_payment with validated and cleaned data.

        Param:
            debt_data: Dictionary
                * user_id : Integer
                * debt_id : Integer
            expense_data: Dictionary
                * user_id : Integer
                * category_id : Integer
                * amount : Float
                * expense_date : String
                * payment_method : Enum("cash", "gcash", "bank", "card", "other")
                * remarks : String
        Return: 
            DebtPayments Persistence: Object
        """
        filtered_debt_payment_data = self.TRANSACTION_POLICY.validate_insert_debt_payment(debt_data)
        
        #query debt by id and user id
        debt = self.get_debt_by_id_and_userid(filtered_debt_payment_data["debt_id"], filtered_debt_payment_data["user_id"])
        #check if debt is present here ------------------
        self.FINANCIALCALCULATIONS_POLICY.is_debt_present(debt)

        #create category string from debt.lender
        generated_category_string = self.create_category_string(debt.lender)

        #check if this string is already at users category
        category = self.get_category_by_name_and_userid(generated_category_string, filtered_debt_payment_data["user_id"])
        
        try:
            #if no save this string to a new category under this user
            self.CATEGORY_POLICY.validate_duplicate_category_name_entry(category)
            categories_data = self.CATEGORY_POLICY.validate_insert_category({
                "user_id": filtered_debt_payment_data["user_id"],
                "type": "expense",
                "name": generated_category_string
            })
            new_category = Categories(**categories_data)
            new_category = self.safe_execute(
                lambda: self._save(new_category),
                error_message="Failed to save new category"
            )
            expense_data["category_id"] = new_category.id
        #if yes get this category id and add it to expense_data
        except PolicyError as e:
            expense_data["category_id"] = category.id
        finally:
            expense_data["payee"] = debt.lender

        filtered_expense_data = self.TRANSACTION_POLICY.validate_insert_expense(expense_data)
        new_expense = Expenses(**filtered_expense_data)
        db.session.add(new_expense)
        db.session.flush()
        filtered_debt_payment_data["expense_id"] = new_expense.id
        new_debt_payment = DebtPayments(**filtered_debt_payment_data)
        

        return self.safe_execute(
            lambda: self._save(new_debt_payment),
            error_message="Failed to create debt"
        )

    def create_category_string(self, lender):
        return f"Debt payment to {lender}"

    def get_debt_by_id_and_userid(self, debt_id, user_id):
        """ 
            Get Debt record by id
            
            Param:
                * debt_id : int
           Return:
                Debts Persistence: Object        
        """ 
        return Debts.query.filter_by(id=debt_id, user_id=user_id).first()

    def get_debt_payment_by_id(self, id: int) -> object:
        return DebtPayments.query.filter_by(id=id).first()

    def get_debt_payment_by_id_and_userid(self, id: int, user_id: int) -> object:
        return DebtPayments.query.filter_by(id=id, user_id=user_id).first()
    
    # -----------------------------------------------------
    # GET ALL DEBT_PAYMENTS BY USER
    # -----------------------------------------------------
    def get_all_debt_payments_by_user(self, user_id: int) -> object:
        return DebtPayments.query.filter_by(user_id=user_id).all()
    
    
    # -----------------------------------------------------
    # UPDATE DEBT_PAYMENT
    # -----------------------------------------------------
    """ 
        payment_date:
        remarks
    """
    def edit_debt_payment(self, id: int, user_id: int, data: dict) -> object:
        target_debt_payment = self.get_debt_payment_by_id_and_userid(id, user_id)

        if target_debt_payment is None: 
            raise ServiceError("No debt payment record is found")
        
        clean = self.update_resource(
            data,
            allowed=["payment_date", "remarks"]
        )

        if clean["payment_date"]:
            target_debt_payment.payment_date = clean["payment_date"]
        if clean["remarks"]:
            target_debt_payment.remarks = clean["remarks"]
        
        return self.safe_execute(lambda: self._save(target_debt_payment),
                                 error_message="Failed to update debt payment")


    # -----------------------------------------------------
    # DELETE DEBT PAYMENT
    # -----------------------------------------------------
    def delete_debt_payment(self, id: int, user_id: int) -> bool:
        debt_payment = self.get_debt_payment_by_id_and_userid(id, user_id)

        return self.safe_execute(
            lambda: self._delete(debt_payment),
            error_message="Failed to delete debt payment"
        )
    
    def calculate_total_debt_payments_by_userid(self, id, user_id: int) -> float:
        total = (
            db.session.query(func.coalesce(func.sum(Income.amount), 0))
            .join(
                DebtPayments,
                DebtPayments.income_id == Income.id
            )
            .filter(DebtPayments.user_id == user_id)
            .filter(DebtPayments.pymt_type == "deposit")
            .scalar()
        )

        return total
    

    def get_category_by_name_and_userid(self, name: str, user_id) -> object:
        """ 
            Get Category record by name and user id
            
            Param:
                * name : int
                * user_id : int
            Return:
                Categories Persistence: Object        
        """
        return Categories.query.filter_by(name=name, user_id=user_id).first()
