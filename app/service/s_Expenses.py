from app.model.m_Expenses import db, Expenses
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService
from sqlalchemy import func

class ExpenseService(BaseService):
    # -----------------------------------------------------
    # CREATE EXPENSE
    # -----------------------------------------------------
    def insert_expense(self, data: dict) -> object:
        """ 
        Creates a new expense with validated and cleaned data. 
        """
        clean = self.create_resource(
            data,
            required=["user_id", "category_id", "payee", "amount", "expense_date", "payment_method"],
            allowed=["user_id", "category_id", "payee", "amount", "expense_date", "payment_method", "remarks"]
        )

        new_expense = Expenses(**clean)
        
        return self.safe_execute(lambda: self._save(new_expense),
                                 error_message="Failed to create expense")
    
    # -----------------------------------------------------
    # GET EXPENSE BY ID
    # -----------------------------------------------------
    def get_expense_by_id(self, expense_id) -> object:
        return Expenses.query.filter_by(id=expense_id).first()
    
    # -----------------------------------------------------
    # GET EXPENSE BY ID and USER ID
    # -----------------------------------------------------
    def get_expenses_by_id_and_userid(self, expense_id, user_id) -> object:
        return Expenses.query.filter_by(id=expense_id, user_id=user_id).first()

    # -----------------------------------------------------
    # GET ALL EXPENSE BY USER
    # -----------------------------------------------------    
    def get_all_expense_by_user(self, user_id):
        return Expenses.query.filter_by(user_id=user_id).all()
    
    # -----------------------------------------------------
    # UPDATE EXPENSE
    # -----------------------------------------------------
    def edit_expense(self, user_id, income_id, data: dict) -> object:
        target_expense = self.get_expenses_by_id_and_userid(income_id, user_id)

        if target_expense is None:
            raise ServiceError("No expense record found")
        
        clean = self.update_resource(
            data,
            allowed=["category_id", "payee", "payment_method", "remarks"]
        )

        if clean["category_id"]:
            #should have category checker
            target_expense.category_id = clean["category_id"]
        if clean["payee"]:
            target_expense.payee = clean["payee"]
        if clean["payment_method"]:
            target_expense.payment_method = clean["payment_method"]
        if clean["remarks"]:
            target_expense.remarks = clean["remarks"]

        return self.safe_execute(lambda: self._save(target_expense),
                                 error_message="Failed to update expense")
    
    # -----------------------------------------------------
    # DELETE EXPENSE
    # -----------------------------------------------------
    def delete_expense(self, expense_id, user_id) -> bool:
        expense = self.get_expenses_by_id_and_userid(expense_id, user_id)

        return self.safe_execute(
            lambda: self._delete(expense),
            error_message="Failed to delete expense"
        )
    

    def calculate_total_expense_by_userid(self, user_id: int) -> float:
        total = (
            Expenses.query
            .with_entities(func.coalesce(func.sum(Expenses.amount), 0))
            .filter(Expenses.user_id == user_id)
            .scalar()
        )
        return float(total)
