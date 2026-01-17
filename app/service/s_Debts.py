from app.model.m_Debts import db, Debts
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService
from sqlalchemy import func

class DebtsService(BaseService):
    # -----------------------------------------------------
    # CREATE DEBT
    # -----------------------------------------------------        
    def insert_debt(self, data: dict) -> object:
        """
        Creates a new debt with validated and cleaned data.

        Param:
            data: Dictionary
                * user_id : String
                * lender : String 
                * principal : Float 
                * interest_rate : Float 
                * start_date : Date 
                * due_date : Date 
                * min_payment : Float  
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
    def get_debt_by_id_and_userid(self, debt_id:int, user_id: int) -> object: 
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
        """ 
            Updates debt record by id and user_id
            
            Param:
                data: Dictionary
                    * lender : String
                    * principal : Float
                    * interest_rate : Float
            Return:
                Debts Instance        
        """
        target_debt = self.get_debt_by_id_and_userid(debt_id, user_id)

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
    def delete_debt(self, id: int, user_id: int) -> bool:
        debt = self.get_debt_by_id_and_userid(id, user_id)

        return self.safe_execute(
            lambda: self._delete(debt),
            error_message="Failed to delete debt"
        )
    
    def calculate_total_debts_by_userid(self, user_id: int) -> float:
        total = (
            Debts.query
            .with_entities(func.coalesce(func.sum(Debts.principal), 0))
            .filter(Debts.user_id == user_id)
            .filter(Debts.status == "active")
            .scalar()
        )

        return float(total)
