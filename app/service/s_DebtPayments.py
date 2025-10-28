from app.service import db
from app.model.m_DebtPayments import DebtPayments
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt

class DebtPaymentsService:
    def insert_debt_payments(self, user_id: int, debt_payment_data: dict) -> object:
        try:
            required_fields = ['lender', 'principal', 'interest_rate', 'start_date', 'due_date']
            for field in required_fields:
                if field not in required_fields:
                    raise ValueError(f"Missing or empty field: {field}")
            debt_payment_entry = DebtPayments(
                lender=debt_payment_data['lender'],
                principal=debt_payment_data['principal'],
                intereset_rate=debt_payment_data['interest_rate'],
                start_date=debt_payment_data['start_date'],
                due_date=debt_payment_data['due_date'],
            )    
            db.session.add(debt_payment_data)
            db.session.commit()
            return debt_payment_entry
        except (SQLAlchemyError, ValueError) as e:
            db.session.rollback()
            print(f"Error inserting debt payments: {e}")
            return None
