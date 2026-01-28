from app.model.m_Expenses import db, Expenses
from app.model.m_Categories import Categories
from app.model.m_DebtPayments import DebtPayments
from app.model.m_SavingTransactions import SavingTransactions
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService
from sqlalchemy import func

class ExpenseService(BaseService):
    def insert_expense(self, data: dict) -> object:
        """ 
            Creates a new Expense with validated and cleaned data.

            Param:  
                data: Dictionary
                    * user_id : Integer
                    * category_id : Integer
                    * payee : String
                    * amount : Float
                    * expense_date : String
                    * payment_method : Enum("cash", "gcash", "bank", "card", "other")
                    * remarks : String
            Return:
                clean : Dictionary
        """
        filtered_expense_data = self.TRANSACTION_POLICY.validate_insert_expense(data)
        new_expense = Expenses(**filtered_expense_data)
        return self.safe_execute(lambda: self._save(new_expense),
                                 error_message="Failed to create expense")
    
    def get_expense_by_id(self, expense_id) -> object:
        """ 
            Get Expense record by id
            
            Param:
                * expense_id : int
           Return:
                Expense Persistence: Object        
        """
        return Expenses.query.filter_by(id=expense_id).first()
    
    def get_expenses_by_id_and_userid(self, expense_id, user_id) -> object:
        """ 
            Get Expense record by id and user id
            
            Param:
                * expense_id : int
                * user_id : int
           Return:
                Expense Persistence: Object        
        """
        return Expenses.query.filter_by(id=expense_id, user_id=user_id).first()

    def get_all_expense_by_user(self, user_id):
        """ 
            Returns list of all Expense Objects by a user stored in database
            
            Param:
                * expense_id : int
           Return:
                Expense Persistence: Object        
        """
        return Expenses.query.filter_by(user_id=user_id).all()
    
    def edit_expense(self, user_id, expense_id, data: dict) -> object:
        """ 
            Edit an expense Record with validated and cleaned data. 
            Param:  
                data: Dictionary
                    * user_id : Integer
                    * category_id : Integer
                    * payee : String
                    * expense_date : String
                    * payment_method : Enum("cash", "gcash", "bank", "card", "other")
                    * remarks : String
           Return:
                Expense Persistence: Object        
        """
        target_expense = self.get_expenses_by_id_and_userid(expense_id, user_id)
        filtered_expenses_data = self.TRANSACTION_POLICY.validate_insert_expense(data, target_expense)
        category = self.get_category_by_id_and_userid(filtered_expenses_data["category_id"], user_id)
        self.CATEGORY_POLICY.validate_users_category_existence(category)
        
        for field, value in filtered_expenses_data.items():
            setattr(target_expense, field, value)
        return self.safe_execute(lambda: self._save(target_expense),
                                 error_message="Failed to update expense")
    
    def delete_expense(self, expense_id, user_id):
        """ 
            Delete Expense record by id
            Param:
                * expense_id : Int
                * user_id: Int
            Return:
                Boolean
        """
        expense = self.get_expenses_by_id_and_userid(expense_id, user_id)
        debt_payment = self.get_debt_payment_by_expense_id(expense.id)
        saving_transaction = self.get_saving_transaction_by_expense_id(expense.id)
        self.TRANSACTION_POLICY.validate_expense_deletion(expense, debt_payment, saving_transaction)
        return self.safe_execute(
            lambda: self._delete(expense),
            error_message="Failed to delete expense"
        )
    
    def calculate_total_expense_by_userid(self, user_id: int) -> float:
        """ 
            Returns sum of a user total Expense
            Param:
                * user_id: Int
            Return:
                total: Float
        """
        total = (
            Expenses.query
            .with_entities(func.coalesce(func.sum(Expenses.amount), 0))
            .filter(Expenses.user_id == user_id)
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
    
    def get_debt_payment_by_expense_id(self, expense_id) -> object:
        """ 
            Get DebtPayments record expense id
            
            Param:
                * expense_id : int
            Return:
                DebtPayments Persistence: Object        
        """
        return DebtPayments.query.filter_by(expense_id=expense_id).first()
    
    def get_saving_transaction_by_expense_id(self, expense_id) -> object:
        """ 
            Get SavingTransactions record expense id
            
            Param:
                * expense_id : int
            Return:
                SavingTransactions Persistence: Object        
        """
        return SavingTransactions.query.filter_by(expense_id=expense_id).first()