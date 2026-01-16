from app.service import db
from app.model.m_DebtPayments import DebtPayments
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService

class DebtPaymentsService(BaseService):
    # -----------------------------------------------------
    # CREATE DEBT PAYMENTS
    # -----------------------------------------------------   
    def insert_debt_payments(self, data: dict) -> object:
        """ 
        Creates a new debt payment with validated and cleaned data.
        """
        clean = self.create_resource(
            data,
            required=[
                "lender"
                "principal",
                "interest_rate",
                "start_date",
                "due_date"
            ],
            allowed=[
                "lender"
                "principal",
                "interest_rate",
                "start_date",
                "due_date"
            ]
        )

        new_debt_payment = DebtPayments(**clean)

        return self.safe_execute(
            lambda: self._save(new_debt_payment),
            error_message="Failed to create debt"
        )
        
    # -----------------------------------------------------
    # GET DEBT_PAYMENT BY ID
    # -----------------------------------------------------
    def get_debt_payment_by_id(self, id: int) -> object:
        return DebtPayments.query.filter_by(id=id).first()

    # -----------------------------------------------------
    # GET DEBT_PAYMENT BY ID AND USER ID
    # -----------------------------------------------------
    def get_debt_payment_by_id_and_userid(self, id: int, user_id: int) -> object:
        return DebtPayments.query.filter_by(id=id, user_id=user_id).first()
    
    # -----------------------------------------------------
    # GET ALL DEBT_PAYMENTS BY USER
    # -----------------------------------------------------
    def get_all_debt_payments_by_user(self, user_id: int) -> object:
        return DebtPayments.query.filter_by(user_id=user_id).all()
    
    
    # -----------------------------------------------------
    # UPDATE DEBT_PAYMENT
    # -----------------------------------------------------
    """ 
        payment_date:
        remarks
    """
    def edit_debt_payment(self, id: int, user_id: int, data: dict) -> object:
        target_debt_payment = self.get_debt_payment_by_id_and_userid(id, user_id)

        if target_debt_payment is None: 
            raise ServiceError("No debt payment record is found")
        
        clean = self.update_resource(
            data,
            allowed=["payment_date", "remarks"]
        )

        if clean["payment_date"]:
            target_debt_payment.payment_date = clean["payment_date"]
        if clean["remarks"]:
            target_debt_payment.remarks = clean["remarks"]
        
        return self.safe_execute(lambda: self._save(target_debt_payment),
                                 error_message="Failed to update debt payment")


    # -----------------------------------------------------
    # DELETE DEBT PAYMENT
    # -----------------------------------------------------
    def delete_debt_payment(self, id: int, user_id: int) -> bool:
        debt_payment = self.get_debt_payment_by_id_and_userid(id, user_id)

        return self.safe_execute(
            lambda: self._delete(debt_payment),
            error_message="Failed to delete debt payment"
        )