from app.ext import db
from app.model.m_DebtPayments import DebtPayments
from typing import Optional, List


class DebtPaymentsRepositoryImpl:
    """SQLAlchemy-backed repository for DebtPayments model."""

    def save(self, entity: DebtPayments) -> DebtPayments:
        db.session.add(entity)
        db.session.flush()
        return entity

    def get_by_id(self, entity_id: int) -> Optional[DebtPayments]:
        return DebtPayments.query.filter_by(id=entity_id).first()

    def get_by_id_and_userid(self, entity_id: int, user_id: int) -> Optional[DebtPayments]:
        return DebtPayments.query.filter_by(id=entity_id, user_id=user_id).first()

    def get_all(self) -> List[DebtPayments]:
        return DebtPayments.query.all()

    def get_all_by_user(self, user_id: int) -> List[DebtPayments]:
        return DebtPayments.query.filter_by(user_id=user_id).all()

    def update(self, entity: DebtPayments) -> DebtPayments:
        db.session.flush()
        return entity

    def delete(self, entity_id: int) -> bool:
        obj = self.get_by_id(entity_id)
        if obj is None:
            return False
        db.session.delete(obj)
        return True

    def create(self, **kwargs) -> DebtPayments:
        return DebtPayments(**kwargs)
