from app.model.m_Income import db, Income
from app.model.m_Categories import Categories
from app.model.m_DebtPayments import DebtPayments
from app.model.m_SavingTransactions import SavingTransactions
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService
from sqlalchemy import func

class IncomeService(BaseService):      
    def insert_income(self, data: dict) -> object:
        """ 
        Creates a new income with validated and cleaned data. 
            Param:  
                data: Dictionary
                    * user_id : Integer
                    * category_id : Integer
                    * source : String
                    * amount : Float
                    * payment_method : Enum("cash", "gcash", "bank", "card", "other")
                    * remarks : String
            Return:
                Income Persistence : Object

        """
        filtered_income_data = self.TRANSACTION_POLICY.validate_insert_income(data)
        
        category = self.get_category_by_id_and_userid(filtered_income_data["category_id", "user_id"])

        self.CATEGORY_POLICY.validate_users_category_existence(category)

        new_income = Income(**filtered_income_data)
        
        return self.safe_execute(lambda: self._save(new_income),
                                 error_message="Failed to create income")

    def get_income_by_id(self, income_id) -> object:
        """ 
            Get Income record by id
            
            Param:
                * income_id : int
           Return:
                Income Persistence: Object        
        """
        return Income.query.filter_by(id=income_id).first()

    def get_income_by_id_and_userid(self, income_id, user_id) -> object:
        """ 
            Get Income record by id and user id
            
            Param:
                * income_id : int
                * user_id : int
           Return:
                Income Persistence: Object        
        """
        return Income.query.filter_by(id=income_id, user_id=user_id).first()
    
    def get_all_income_by_user(self, user_id):
        """ 
            Returns list of all Income Objects by a user stored in database
            
            Param:
                * income_id : int
           Return:
                Income Persistence Objects: List
        """
        return Income.query.filter_by(user_id=user_id).all()
    
    def edit_income(self, income_id, user_id, data: dict) -> object:
        """ 
        Edit an Income Record with validated and cleaned data. 
            Param:  
                data: Dictionary
                    * user_id : Integer
                    * category_id : Integer
                    * source : String
                    * amount : Float
                    * payment_method : Enum("cash", "gcash", "bank", "card", "other")
                    * remarks : String
            Return:
                Income Persistence : Object
        """
        target_income = self.get_income_by_id_and_userid(income_id, user_id)        

        filtered_income_data = self.TRANSACTION_POLICY.validate_income_editing(data, target_income)

        category = self.get_category_by_id_and_userid(filtered_income_data["category_id"], user_id)

        self.CATEGORY_POLICY.validate_users_category_existence(category)

        for field, value in filtered_income_data.items():
            setattr(target_income, field, value)

        return self.safe_execute(lambda: self._save(filtered_income_data),
                                 error_message="Failed to update income")
    
    def delete_income(self, income_id, user_id):
        """ 
            Delete Income record by id
            Param:
                * income_id : Int
                * user_id: Int
            Return:
                Boolean
        """
        income = self.get_income_by_id_and_userid(income_id, user_id)
        debt_payment = self.get_debt_payment_by_income_id(income.income_id)
        saving_transaction = self.get_saving_transaction_by_income_id(income.income_id)
        self.TRANSACTION_POLICY.validate_income_deletion(income, debt_payment, saving_transaction)
        return self.safe_execute(
            lambda: self._delete(income),
            error_message="Failed to delete income"
        )

    def calculate_total_income_by_userid(self, user_id: int) -> float:
        """ 
            Returns sum of a user total Income
            Param:
                * user_id: Int
            Return:
                total: Float
        """
        total = (
            Income.query
            .with_entities(func.coalesce(func.sum(Income.amount), 0))
            .filter(Income.user_id == user_id)
            .scalar()
        )
        return float(total)

    def get_category_by_id_and_userid(self, category_id: int, user_id: int) -> object:
        """ 
            Get Category record by id and user id
            
            Param:
                * category_id : int
                * user_id : int
            Return:
                Categories Persistence: Object        
        """
        return Categories.query.filter_by(id=category_id, user_id=user_id).first()
    
    def get_debt_payment_by_income_id(self, income_id) -> object:
        """ 
            Get DebtPayments record income id
            
            Param:
                * income_id : int
            Return:
                DebtPayments Persistence: Object        
        """
        return DebtPayments.query.filter_by(income_id=income_id).first()
    
    def get_saving_transaction_by_income_id(self, income_id) -> object:
        """ 
            Get SavingTransactions record income id
            
            Param:
                * income_id : int
            Return:
                SavingTransactions Persistence: Object        
        """
        return SavingTransactions.query.filter_by(income_id=income_id).first()