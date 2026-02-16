from typing import Optional, List
from app.repositories.income_repository import IncomeRepository
from app.model.m_Income import Income as IncomeORM
from app.ext import db
from app.domain.entities import Income as DomainIncome
from app.repositories.exceptions import EntityNotFoundError
from sqlalchemy import func


class IncomeRepositoryImpl(IncomeRepository):
    def save(self, entity: DomainIncome) -> DomainIncome:
        orm = IncomeORM(
            user_id=entity.user_id,
            category_id=entity.category_id,
            source=entity.source,
            amount=entity.amount,
            received_date=entity.received_date,
            payment_method=entity.payment_method,
            remarks=entity.remarks,
        )
        db.session.add(orm)
        db.session.flush()
        entity.id = orm.id
        return entity

    def get_by_id(self, income_id: int) -> Optional[DomainIncome]:
        orm = IncomeORM.query.filter_by(id=income_id).first()
        if orm is None:
            return None
        return DomainIncome(
            user_id=orm.user_id,
            category_id=orm.category_id,
            source=orm.source,
            amount=orm.amount,
            received_date=orm.received_date,
            payment_method=orm.payment_method,
            remarks=orm.remarks,
            id=orm.id,
        )

    def get_by_id_and_user_id(self, income_id: int, user_id: int) -> Optional[DomainIncome]:
        orm = IncomeORM.query.filter_by(id=income_id, user_id=user_id).first()
        if orm is None:
            return None
        return DomainIncome(
            user_id=orm.user_id,
            category_id=orm.category_id,
            source=orm.source,
            amount=orm.amount,
            received_date=orm.received_date,
            payment_method=orm.payment_method,
            remarks=orm.remarks,
            id=orm.id,
        )

    def get_all_by_user_id(self, user_id: int) -> List[DomainIncome]:
        orms = IncomeORM.query.filter_by(user_id=user_id).all()
        return [
            DomainIncome(
                user_id=o.user_id,
                category_id=o.category_id,
                source=o.source,
                amount=o.amount,
                received_date=o.received_date,
                payment_method=o.payment_method,
                remarks=o.remarks or "",
                id=o.id,
            )
            for o in orms
        ]

    def calculate_total_by_user_id(self, user_id: int) -> float:
        total = (
            IncomeORM.query
            .with_entities(func.coalesce(func.sum(IncomeORM.amount), 0))
            .filter(IncomeORM.user_id == user_id)
            .scalar()
        )
        return float(total)

    def get_by_category_id(self, category_id: int) -> List[DomainIncome]:
        orms = IncomeORM.query.filter_by(category_id=category_id).all()
        return [
            DomainIncome(
                user_id=o.user_id,
                category_id=o.category_id,
                source=o.source,
                amount=o.amount,
                received_date=o.received_date,
                payment_method=o.payment_method,
                remarks=o.remarks,
                id=o.id,
            )
            for o in orms
        ]

    def update(self, entity: DomainIncome) -> DomainIncome:
        orm = IncomeORM.query.filter_by(id=entity.id).first()
        if orm is None:
            raise EntityNotFoundError('Income not found')
        orm.source = entity.source
        orm.amount = entity.amount
        orm.payment_method = entity.payment_method
        orm.remarks = entity.remarks
        orm.category_id = entity.category_id
        orm.received_date = entity.received_date
        db.session.flush()
        return entity

    def create(self, **kwargs) -> DomainIncome:
        return DomainIncome(**kwargs)

    def delete(self, entity_id: int) -> bool:
        orm = IncomeORM.query.filter_by(id=entity_id).first()
        if orm is None:
            return False
        db.session.delete(orm)
        return True

    def get_all(self):
        orms = IncomeORM.query.all()
        return [
            DomainIncome(
                user_id=o.user_id,
                category_id=o.category_id,
                source=o.source,
                amount=o.amount,
                received_date=o.received_date,
                payment_method=o.payment_method,
                remarks=o.remarks,
                id=o.id,
            )
            for o in orms
        ]
