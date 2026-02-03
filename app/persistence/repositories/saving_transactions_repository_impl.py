from typing import Optional, List
from app.repositories.saving_transactions_repository import SavingTransactionsRepository
from app.model.m_SavingTransactions import SavingTransactions as SavingTransactionsORM
from app.ext import db
from sqlalchemy import func


class SavingTransactionsRepositoryImpl(SavingTransactionsRepository):
    """SQLAlchemy-backed repository for SavingTransactions model."""

    def save(self, entity: SavingTransactionsORM) -> SavingTransactionsORM:
        db.session.add(entity)
        db.session.flush()
        return entity

    def get_by_id(self, entity_id: int) -> Optional[SavingTransactionsORM]:
        return SavingTransactionsORM.query.filter_by(id=entity_id).first()

    def get_by_id_and_userid(self, entity_id: int, user_id: int) -> Optional[SavingTransactionsORM]:
        return SavingTransactionsORM.query.filter_by(id=entity_id, user_id=user_id).first()

    def get_all(self) -> List[SavingTransactionsORM]:
        return SavingTransactionsORM.query.all()

    def get_all_by_user(self, user_id: int) -> List[SavingTransactionsORM]:
        return SavingTransactionsORM.query.filter_by(user_id=user_id).all()

    def get_all_by_user_and_type(self, user_id: int, txt_type: str) -> List[SavingTransactionsORM]:
        return SavingTransactionsORM.query.filter_by(user_id=user_id, txt_type=txt_type).all()

    def update(self, entity: SavingTransactionsORM) -> SavingTransactionsORM:
        db.session.flush()
        return entity

    def delete(self, entity_id: int) -> bool:
        obj = self.get_by_id(entity_id)
        if obj is None:
            return False
        db.session.delete(obj)
        return True

    def calculate_total_deposits_by_user(self, user_id: int) -> float:
        """Calculate total deposits (income) for a user's saving transactions."""
        from app.model.m_Income import Income
        
        total = (
            db.session.query(func.coalesce(func.sum(Income.amount), 0))
            .join(
                SavingTransactionsORM,
                SavingTransactionsORM.income_id == Income.id
            )
            .filter(SavingTransactionsORM.user_id == user_id)
            .filter(SavingTransactionsORM.txt_type == "deposit")
            .scalar()
        )
        return float(total)
