from app.model.m_SavingTransactions import db, SavingTransactions
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService
from sqlalchemy import func

class SavingTransactionsService(BaseService):
    # -----------------------------------------------------
    # CREATE SAVING TRANSACTIONS
    # -----------------------------------------------------
    def insert_saving_transaction(self, data: dict) -> object:
        """ 
            Creates a new saving transaction with validated and cleaned data.
            
            Param:
                data: Dictionary
                    * txt_type : Enum('deposit', 'withdraw')
                    * amount : Float
                    * remarks : String
            Return:
                SavingTransactions Instance        
        """
        clean = self.create_resource(
            data,
            required=[
                "txt_type",
                "amount",
                "remarks"
            ],
            allowed=[
                "txt_type",
                "amount",
                "remarks"
            ]
        )

        new_saving_transaction = SavingTransactions(**clean)

        return self.safe_execute(lambda: self._save(new_saving_transaction),
                                 error_message="Failed to create saving transaction")
    
    # -----------------------------------------------------
    # GET SAVING TRANSACTION BY ID
    # -----------------------------------------------------
    def get_saving_transaction_by_id(self, id: int) -> object:
        return SavingTransactions.query.filter_by(id=id).first()

    # -----------------------------------------------------
    # GET SAVING TRANSACTION BY ID AND USER ID
    # -----------------------------------------------------
    def get_saving_transaction_by_id_and_userid(self, id: int, user_id: int) -> object:
        return SavingTransactions.query.filter_by(id=id, user_id=user_id).first()
    
    # -----------------------------------------------------
    # UPDATE SAVING TRANSACTION
    # -----------------------------------------------------
    def edit_saving_transaction(self, id: int, user_id: int, data: dict) -> object:
        """ 
            Updates saving transactions record by id and user_id
            
            Param:
                data: Dictionary
                    * txt_date : Date
                    * remarks : String
            Return:
                SavingTransactions Instance        
        """
        target_saving_transaction = self.get_saving_transaction_by_id_and_userid(id, user_id)

        if target_saving_transaction is None:
            raise ServiceError("No saving_transaction record found")
        
        clean = self.update_resource(
            data,
            allowed=["txt_date", "remarks"]
        )
        if clean["txt_date"]:
            target_saving_transaction.txt_date = clean["txt_date"]
        if clean["remarks"]:
            target_saving_transaction.remarks = clean["remarks"]

        return self.safe_execute(lambda: self._save(target_saving_transaction),
                                 error_message="Failed to update saving transaction")
    

    # -----------------------------------------------------
    # DELETE SAVING TRANSACTION
    # -----------------------------------------------------
    def delete_saving_transaction(self, id: int, user_id: int) -> bool:
        saving_transaction = self.get_saving_transaction_by_id_and_userid(id, user_id)

        return self.safe_execute(
            lambda: self._delete(saving_transaction),
            error_message="Failed to delete saving_transaction"
        )  
    
    def calculate_total_saving_deposits_by_userid(self, user_id: int) -> float:
        total = (
            SavingTransactions.query
            .with_entities(func.coalesce(func.sum(SavingTransactions.amount), 0))
            .filter(SavingTransactions.user_id == user_id)
            .filter(SavingTransactions.txt_type == "deposit")
            .scalar()
        )
        return float(total)
        
    def calculate_total_saving_withdraws_by_userid(self, user_id: int) -> float:
        total = (
            SavingTransactions.query
            .with_entities(func.coalesce(func.sum(SavingTransactions.amount), 0))
            .filter(SavingTransactions.user_id == user_id)
            .filter(SavingTransactions.txt_type == "withdraw")
            .scalar()
        )
        return float(total)
        
