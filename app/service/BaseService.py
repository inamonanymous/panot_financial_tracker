from abc import ABC
from app.utils.exceptions.ServiceError import ServiceError
from app.utils.exceptions.PolicyError import PolicyError
from app.ext import db
import re
from app.policies.p_UserPolicy import UserPolicy
from app.policies.p_FinancialCalculations import FinancialCalculationsPolicy
from app.policies.p_CategoryPolicy import CategoryPolicy
from app.policies.p_TransactionPolicy import TransactionPolicy

class BaseService(ABC):
    """
    BaseService gives you reusable tools for:
    - safe error handling
    - safe execution for database operations

    Every Service class in your app should inherit from BaseService.
    """

    def __init__(self):
        self.USER_POLICY = UserPolicy()
        self.FINANCIALCALCULATIONS_POLICY = FinancialCalculationsPolicy()
        self.CATEGORY_POLICY = CategoryPolicy()
        self.TRANSACTION_POLICY = TransactionPolicy()

    # ==============================================================
    # 1. SAFE EXECUTION WRAPPER
    # ==============================================================

    def safe_execute(self, func, error_message="Service failed"):
        """
        Runs any function in a safe try/except block.

        Why you need this:
        - It prevents your API from crashing
        - It converts unknown errors into clean ServiceError messages
        - It keeps your code DRY (no need to write try/except everywhere)

        Usage Example:
            return self.safe_execute(lambda: self._save_to_db(obj))
        """
        try:
            return func()
        except ServiceError as e:
            # If Use case error, raise it normally
            raise e
            db.session.rollback()
        except PolicyError as e:
            # If validation error, raise it normally
            raise e
            db.session.rollback()
        except Exception as e:
            # Any unknown error triggers ServiceError
            print(e)  # optional logging
            db.session.rollback()
            raise ServiceError(error_message)

    def _save(self, instance):
        db.session.add(instance)
        db.session.commit()
        return instance

    def _delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
        return True
