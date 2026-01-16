from app.model.m_Income import db, Income
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService
from sqlalchemy import func

class IncomeService(BaseService):
    # -----------------------------------------------------
    # CREATE INCOME
    # -----------------------------------------------------        
    def insert_income(self, data: dict) -> object:
        """ 
        Creates a new income with validated and cleaned data. 
        """
        clean = self.create_resource(
            data,
            required=["category_id", "source", "amount", "payment_method"],
            allowed=["category_id", "source", "amount", "remarks", "payment_method"]
        )
        
        new_income = Income(**clean)
        
        return self.safe_execute(lambda: self._save(new_income),
                                 error_message="Failed to create income")
    
    # -----------------------------------------------------
    # GET INCOME BY ID
    # -----------------------------------------------------        
    def get_income_by_id(self, income_id) -> object:
        return Income.query.filter_by(id=income_id).first()
    # -----------------------------------------------------

    # GET INCOME BY ID AND USER ID
    # -----------------------------------------------------        
    def get_income_by_id_and_userid(self, income_id, user_id) -> object:
        return Income.query.filter_by(id=income_id, user_id=user_id).first()
    
    # -----------------------------------------------------
    # GET ALL INCOME BY USER
    # -----------------------------------------------------        
    def get_all_income_by_user(self, user_id):
        return Income.query.filter_by(user_id=user_id).all()
    
    # -----------------------------------------------------
    # UPDATE INCOME
    # ----------------------------------------------------- 
    def edit_income(self, user_id, income_id, data: dict) -> object:
        target_income = self.get_income_by_id_and_userid(income_id, user_id)        

        if target_income is None:
            raise ServiceError("No income record found")

        clean = self.update_resource(
            data,
            allowed=["source", "remarks"]
        )

        if clean["source"]:
            target_income.source = clean["source"]
        if clean["remarks"]:
            target_income.remarks = clean["remarks"]
        if clean["payment_method"]:
            target_income.payment_method = clean["payment_method"]

        return self.safe_execute(lambda: self._save(target_income),
                                 error_message="Failed to update income")
    
    # -----------------------------------------------------
    # DELETE INCOME
    # ----------------------------------------------------- 
    def delete_income(self, income_id, user_id) -> bool:
        income = self.get_income_by_id_and_userid(income_id, user_id)

        return self.safe_execute(
            lambda: self._delete(income),
            error_message="Failed to delete income"
        )


    def calculate_total_income_by_userid(self, user_id: int) -> float:
        total = (
            Income.query
            .with_entities(func.coalesce(func.sum(Income.amount), 0))
            .filter(Income.user_id == user_id)
            .scalar()
        )
        return float(total)
