from app.service import check_password_hash, generate_password_hash, db
from app.model.m_Users import Users
from app.model.m_Income import Income
from app.model.m_Expenses import Expenses
from app.model.m_SavingTransactions import SavingTransactions
from app.model.m_DebtPayments import DebtPayments
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.utils.exceptions.ServiceError import ServiceError
from app.service.BaseService import BaseService
from app.ext import dt
from sqlalchemy import func

class UserService(BaseService):
    def check_login(self, email, password):
        """ 
            Checks user login authentication
            
            Param:
                * email: String
                * password: String
            Return:
                User Persistence: Object    
        """
        user = Users.query.filter_by(
            email=email
        ).first()
        
        self.USER_POLICY.validate_login(email, password, user)

        return user
    
    def insert_user(self, user_data: dict) -> object:
        """ 
            Insert User record
            
            Param:
                data: Dictionary
                    * firstname: String
                    * lastname: String
                    * email: String
                    * password_hash: String
            Return:
                User Persistence: Object        
        """
        filtered_user_data = self.USER_POLICY.validate_user_registration(user_data)

        new_user = Users(**filtered_user_data)

        return self.safe_execute(lambda: self._save(new_user),
                                    error_message="Failed to create User")

    def get_user_by_id(self, id: int) -> object:
        """ 
            Get User record
            
            Param:
                * id : int
            Return:
                User Persistence: Object        
        """
        return Users.query.filter_by(id=id).first()
    
    def get_user_by_email(self, email: str) -> object:
        return Users.query.filter_by(email=email).first()
    
    def get_all_users() -> list:
        """ 
            Get all user records in database
            
            Return:
                User Persistence Objects: List        
        """
        return Users.query.all()
   
    def edit_user(self, id: int, user_data: dict) -> object:
        """ 
            Updates user record by id
            
            Param:
                data: Dictionary
                    * firstname : String
                    * lastname : String
            Return:
                User Persistence: Object        
        """
        target_user = self.get_user_by_id(id)
        filtered_user_data = self.USER_POLICY.validate_user_editing(user_data, target_user)

        for field, value in filtered_user_data.items():
            setattr(target_user, field, value)

        return self.safe_execute(lambda: self._save(target_user),
                                 error_message="Failed to update user")
           
    def delete_user(self, id: int) -> bool:
        """ 
            Delete user record by id
            
            Param:
                * id : Int
            Return:
                Boolean
        """

        target_user = self.get_user_by_id(id)

        return self.safe_execute(
            lambda: self._delete(target_user),
            error_message="Failed to delete user"
        )
        
    def calculate_current_amount_by_userid(self, user_id: int) -> float:
        """ 
            Calculates current amount of a user in the record and returns difference of expense, debt payments, and saving deposits from income
            
            Param:
                * user_id : Int
            Return:
                User Persistence Objects: List        
        """
        total_income = (
            Income.query
            .with_entities(func.coalesce(func.sum(Income.amount), 0))
            .filter(Income.user_id == user_id)
            .scalar()
        )
        
        total_expense = (
            Expenses.query
            .with_entities(func.coalesce(func.sum(Expenses.amount), 0))
            .filter(Expenses.user_id == user_id)
            .scalar()
        )
        
        """ total_debt_payments = (
            DebtPayments.query
            .with_entities(func.coalesce(func.sum(DebtPayments.amount), 0))
            .filter(DebtPayments.user_id == user_id)
            .scalar()
        ) """

        total_debt_payments = (
            db.session.query(func.coalesce(func.sum(Income.amount), 0))
            .join(
                DebtPayments,
                DebtPayments.income_id == Income.id
            )
            .filter(DebtPayments.user_id == user_id)
            .filter(DebtPayments.pymt_type == "deposit")
            .scalar()
        )
        
        """ total_saving_deposits = (
            SavingTransactions.query
            .with_entities(func.coalesce(func.sum(SavingTransactions.amount), 0))
            .filter(SavingTransactions.user_id == user_id)
            .filter(SavingTransactions.txt_type == "deposit")
            .scalar()
        ) """

        total_saving_deposits = (
            db.session.query(func.coalesce(func.sum(Income.amount), 0))
            .join(
                SavingTransactions,
                SavingTransactions.income_id == Income.id
            )
            .filter(SavingTransactions.user_id == user_id)
            .filter(SavingTransactions.txt_type == "deposit")
            .scalar()
        )

        current_value = self.FINANCIALCALCULATIONS_POLICY.caculate_current_amount_of_user(
            total_income, 
            total_expense, 
            total_debt_payments, 
            total_saving_deposits
        )

        return current_value

    def _save(self, instance):
        try:
            db.session.add(instance)
            db.session.commit()
            return instance

        except IntegrityError as e:
            db.session.rollback()
            message = str(e.orig)

            if "email" in message:
                raise ServiceError("Email already exists. Please use another one")
            print(message)
            raise ServiceError("User database constraint error")

        except Exception:
            db.session.rollback()
            raise ServiceError("Unexpected database error in UserService")