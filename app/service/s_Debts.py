from app.model.m_Debts import db, Debts
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService


class DebtsService(BaseService):
    """ def insert_debtx(self, debt_data: dict) -> object:
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
            return None """

    # -----------------------------------------------------
    # CREATE DEBT
    # -----------------------------------------------------        
    def insert_debt(self, data: dict) -> object:
        """
        Creates a new debt with validated and cleaned data.
        """
        clean = self.create_resource(
            data,
            required=[
                "user_id",
                "lender", 
                "principal", 
                "interest_rate", 
                "start_date", 
                "due_date", 
                "min_payment"
                ],
            allowed=[
                "user_id", 
                "lender", 
                "principal", 
                "interest_rate", 
                "start_date", 
                "due_date", 
                "min_payment"
                ]
        )
        
        new_debt = Debts(**clean)

        return self.safe_execute(lambda: self._save(new_debt), 
                                 error_message="Failed to create debt")


    # -----------------------------------------------------
    # GET DEBT
    # -----------------------------------------------------
    def get_debt_by_id(self, debt_id:int) -> object: 
        debt = Debts.query.filter_by(id=debt_id).first()
        if not debt:
            raise ServiceError(f"Debt-{debt_id} not found")
        return debt
    
    def get_all_debts_by_user(self, user_id: int):
        return Debts.query.filter_by(user_id=user_id).all()
    
    """ def edit_debt(self, id: int, debt_data: dict) -> object:
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
            raise Exception(f"Failed to edit debt: {str(e)}") """

    # -----------------------------------------------------
    # UPDATE DEBT[]
    # -----------------------------------------------------
    def edit_debt(self, debt_id, data: dict) -> object:
        target_debt = self.get_debt_by_id(debt_id)

        clean = self.create_resource(
            data,
            required=["lender", "principal", "interest_rate"],
            allowed=["lender", "principal", "interest_rate"]
        )
        target_debt.lender = clean['lender']
        target_debt.lender = clean['principal']
        target_debt.lender = clean['interest_rate']
        
        return self.safe_execute(lambda: self._save(target_debt),
                                 error_message="Failed to update debt")

    """ def delete_debt(self, id: int) -> bool:
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
            return False """
    
    # -----------------------------------------------------
    # DELETE DEBT
    # -----------------------------------------------------

    def delete_debt(self, id: int) -> bool:
        debt = self.get_debt_by_id(id)

        return self.safe_execute(
            lambda: self._delete(debt),
            error_message="Failed to delete debt"
        )