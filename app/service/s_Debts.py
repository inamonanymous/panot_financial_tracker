from app.model.m_Debts import db, Debts
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService


class DebtsService(BaseService):
    # -----------------------------------------------------
    # CREATE DEBT
    # -----------------------------------------------------        
    def insert_debt(self, data: dict) -> object:
        """
        Creates a new debt with validated and cleaned data.
        """
        clean = self.create_resource(
            data,
            required=[
                "user_id",
                "lender", 
                "principal", 
                "interest_rate", 
                "start_date", 
                "due_date", 
                "min_payment"
                ],
            allowed=[
                "user_id", 
                "lender", 
                "principal", 
                "interest_rate", 
                "start_date", 
                "due_date", 
                "min_payment"
                ]
        )
        
        new_debt = Debts(**clean)

        return self.safe_execute(lambda: self._save(new_debt), 
                                 error_message="Failed to create debt")


    # -----------------------------------------------------
    # GET DEBT BY ID
    # -----------------------------------------------------
    def get_debt_by_id(self, debt_id:int) -> object: 
        return Debts.query.filter_by(id=debt_id).first()
        
    
    # -----------------------------------------------------
    # GET DEBT BY ID AND USER ID
    # -----------------------------------------------------
    def get_debt_by_user_and_id(self, debt_id:int, user_id: int) -> object: 
        return Debts.query.filter_by(id=debt_id, user_id=user_id).first()
        
    # -----------------------------------------------------
    # GET ALL DEBTS BY USER
    # -----------------------------------------------------  
    def get_all_debts_by_user(self, user_id: int):
        return Debts.query.filter_by(user_id=user_id).all()

    # -----------------------------------------------------
    # UPDATE DEBT
    # -----------------------------------------------------
    def edit_debt(self, debt_id: int, user_id: int, data: dict) -> object:
        target_debt = self.get_debt_by_user_and_id(debt_id)

        if target_debt is None:
            raise ServiceError("No debt record found")

        clean = self.update_resource(
            data,
            allowed=["lender", "principal", "interest_rate"]
        )
        if clean["lender"]:
            target_debt.lender = clean['lender']
        if clean["principal"]:
            target_debt.principal = clean['principal']
        if clean["interest_rate"]:
            target_debt.interest_rate = clean['interest_rate']
        
        return self.safe_execute(lambda: self._save(target_debt),
                                 error_message="Failed to update debt")

    
    # -----------------------------------------------------
    # DELETE DEBT
    # -----------------------------------------------------

    def delete_debt(self, id: int) -> bool:
        debt = self.get_debt_by_id(id)

        return self.safe_execute(
            lambda: self._delete(debt),
            error_message="Failed to delete debt"
        )