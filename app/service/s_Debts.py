from app.model.m_Debts import db, Debts
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt

class Debts:
    def insert_debt(self, debt_data: dict) -> object:
        try:
            debt_entry = Debts(
                user_id = debt_data['user_id'],
                lender = debt_data['lender'],
                principal = debt_data['principal'],
                interest_rate = debt_data['interest_rate'],
                start_date = debt_data['start_date'],
                due_date = debt_data['due_date'],
                min_payment = debt_data['min_payment'],
                status = debt_data['status'],
            )

            db.session.add(debt_entry)
            db.sessin.commit()
            return debt_entry
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return None
        
    def get_debt_by_id(self, id:int) -> object: 
        return Debts.query.filter_by(id=id).first()
    
    def get_all_debts(self):
        return Debts.query.all()
    
    """ def edit_debt() """

    def delete_debt(self, id: int) -> bool:
        try:
            target_debt = Debts.query.filter_by(id=id).first()
            if not target_debt:
                raise Exception(f"Debt-{id} not found")
            db.session.delete(target_debt)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return False