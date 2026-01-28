from app.model.m_Debts import db, Debts
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService
from sqlalchemy import func

class DebtsService(BaseService):
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
        
        clean = self.FINANCIALCALCULATIONS_POLICY.validate_insert_debt(data)
        
        new_debt = Debts(**clean)

        return self.safe_execute(lambda: self._save(new_debt), 
                                 error_message="Failed to create debt")

    def get_debt_by_id(self, debt_id:int) -> object:
        """ 
            Get Debt record by id
            
            Param:
                * debt_id : int
           Return:
                Debts Persistence: Object        
        """ 
        return Debts.query.filter_by(id=debt_id).first()
        
    def get_debt_by_id_and_userid(self, debt_id:int, user_id: int) -> object: 
        """ 
            Get Debt record by id and user id
            
            Param:
                * debt_id : int
                * user_id : int
            Return:
                Debts Persistence: Object        
        """
        return Debts.query.filter_by(id=debt_id, user_id=user_id).first()
        
    def get_all_debts_by_user(self, user_id: int):
        """ 
            Returns list of all debt objects by a user stored in database
            
            Return:
                Debts Persistence Objects: List        
        """
        return Debts.query.filter_by(user_id=user_id).all()

    def edit_debt(self, debt_id: int, user_id: int, data: dict) -> object:
        """ 
            Updates debt record by id and user_id
            
            Param:
                data: Dictionary
                    * lender : String
                    * principal : Float
                    * interest_rate : Float
            Return:
                Debts Instance : Object        
        """
        target_debt = self.get_debt_by_id_and_userid(debt_id, user_id)

        filtered_debt_data = self.FINANCIALCALCULATIONS_POLICY.validate_debt_editing(data, target_debt)

        for field, value in filtered_debt_data.items():
            setattr(target_debt, field, value)


        return self.safe_execute(lambda: self._save(target_debt),
                                 error_message="Failed to update debt")

    def delete_debt(self, id: int, user_id: int) -> bool:
        """ 
            Delete debt record by id
            Param:
                * id : Int
                * user_id: Int
            Return:
                Boolean
        """
        debt = self.get_debt_by_id_and_userid(id, user_id)
        self.FINANCIALCALCULATIONS_POLICY.validate_debt_deletion(debt, user_id)

        return self.safe_execute(
            lambda: self._delete(debt),
            error_message="Failed to delete debt"
        )
    
    def calculate_total_debts_by_userid(self, user_id: int) -> float:
        """ 
            Returns sum of a user total debts with principal
            Param:
                * user_id: Int
            Return:
                float
        """
        total = (
            Debts.query
            .with_entities(func.coalesce(func.sum(Debts.principal), 0))
            .filter(Debts.user_id == user_id)
            .filter(Debts.status == "active")
            .scalar()
        )

        return float(total)
