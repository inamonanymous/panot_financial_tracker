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
        email = self.validate_email_string(email)
        password = self.validate_password_string(
                        password,
                        confirm=None,
                        min_len=8
                    )
        user = Users.query.filter_by(
            email=email
        ).first()
        if not (user and check_password_hash(user.password_hash, password)):
            raise ServiceError("Incorrect Credentials!")


        return user
    

    def insert_user(self, user_data: dict) -> object:
        """ 
        Creates a new user with validated and clean data

        Param: user_data: dict
        Return: User object instance
        """

        user_data['firstname'] = self.validate_string(user_data['firstname'], "Firstname", min_len=2)
        user_data['lastname']  = self.validate_string(user_data['lastname'], "Lastname",  min_len=2)
        user_data['email']     = self.validate_email_string(user_data['email'])
        user_data['password_hash']  = self.validate_password_string(
                        user_data['password_hash'],
                        confirm=user_data.get('password2'),
                        min_len=8
                    )
        
        hashed_password = generate_password_hash(user_data['password_hash'].strip())
        user_data['password_hash'] = hashed_password

        clean = self.create_resource(
            user_data,
            required=['firstname', 'lastname', 'email', 'password_hash'],
            allowed=['firstname', 'lastname', 'email', 'password_hash']
        )


        new_user = Users(**clean)

        return self.safe_execute(lambda: self._save(new_user),
                                    error_message="Failed to create Userw")

    def get_user_by_id(id: int) -> object:
        return Users.query.filter_by(id=id).first()
    
    def get_user_by_email(self, email: str) -> object:
        return Users.query.filter_by(email=email).first()
    
    def get_all_users():
        return Users.query.all()
    
    def edit_user(id: int, user_data: dict) -> object:
        try:
            target_user = Users.query.filter_by(id=id).first()
            if not target_user:
                raise Exception(f"User-{id} not found")

            # Allowed fields with expected data types
            allowed_fields = {
                'firstname': str,
                'lastname': str,
            }

            for field, expected_type in allowed_fields.items():
                if field in user_data and user_data[field] is not None:
                    value = user_data[field]

                    # Make sure value is a string (and not empty)
                    if isinstance(value, expected_type) and str(value).strip():
                        setattr(target_user, field, value)

            target_user.updated_at = dt.now()
            db.session.commit()
            return target_user

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error: {e}")
            return None

        except Exception as e:
            db.session.rollback()
            print(f"Error editing user: {e}")
            return None
        
    def delete_user(id: int) -> bool:
        try:
            target_user = Users.query.filter_by(id=id).first()
            if not target_user:
                raise Exception(f"User-{id} not found")
            db.session.delete(target_user)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(e)
            return False
        

    def calculate_current_amount_by_userid(self, user_id: int) -> float:
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
        
        total_debt_payments = (
            DebtPayments.query
            .with_entities(func.coalesce(func.sum(DebtPayments.amount), 0))
            .filter(DebtPayments.user_id == user_id)
            .scalar()
        )
        
        total_saving_deposits = (
            SavingTransactions.query
            .with_entities(func.coalesce(func.sum(SavingTransactions.amount), 0))
            .filter(SavingTransactions.user_id == user_id)
            .filter(SavingTransactions.txt_type == "deposit")
            .scalar()
        )

        current_value = (
            total_income
            - total_expense
            - total_debt_payments
            - total_saving_deposits
        )

        return float(current_value)


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