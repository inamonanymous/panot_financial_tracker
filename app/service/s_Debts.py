from app.model.m_Debts import db, Debts
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt

class DebtsService:
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
                status = 'active',
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
    
    def get_all_debts_by_user(self, user_id: int):
        return Debts.query.filter_by(user_id=user_id).all()
    
    def edit_debt(self, id: int, debt_data: dict) -> object:
        try:
            target_debt = Debts.query.filter_by(id=id).first()
            if not target_debt:
                raise Exception(f"Debt-{id} not found")

            # Safe update mapping
            allowed_fields = {
                'lender': str,
                'principal': (int, float),
                'interest_rate': (int, float)
            }

            for field, expected_type in allowed_fields.items():
                if field in debt_data and debt_data[field] is not None:
                    value = debt_data[field]

                    # Optional: try to cast numeric strings to float
                    if isinstance(expected_type, tuple) and isinstance(value, str):
                        try:
                            value = float(value)
                        except ValueError:
                            continue  # skip invalid numeric strings

                    # Only assign if the value matches the expected type
                    if isinstance(value, expected_type):
                        setattr(target_debt, field, value)

            db.session.commit()
            return target_debt

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to edit debt: {str(e)}")


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