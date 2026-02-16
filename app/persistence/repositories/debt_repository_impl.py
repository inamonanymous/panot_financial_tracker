from typing import Optional, List
from app.repositories.debt_repository import DebtRepository
from app.model.m_Debts import Debts as DebtORM
from app.ext import db
from app.domain.entities import Debt as DomainDebt
from app.repositories.exceptions import EntityNotFoundError
from sqlalchemy import func


class DebtRepositoryImpl(DebtRepository):
    def save(self, entity: DomainDebt) -> DomainDebt:
        orm = DebtORM(
            user_id=entity.user_id,
            lender=entity.lender,
            principal=entity.principal,
            name=entity.name,
            interest_rate=entity.interest_rate,
            start_date=entity.start_date,
            due_date=entity.due_date,
            status=entity.status,
        )
        db.session.add(orm)
        db.session.flush()
        entity.id = orm.id
        return entity

    def get_by_id(self, debt_id: int) -> Optional[DomainDebt]:
        orm = DebtORM.query.filter_by(id=debt_id).first()
        if orm is None:
            return None
        return DomainDebt(
            user_id=orm.user_id,
            lender=orm.lender,
            principal=orm.principal,
            interest_rate=orm.interest_rate,
            start_date=orm.start_date,
            due_date=orm.due_date,
            name=orm.name,
            status=orm.status,
            id=orm.id,
        )

    def get_by_id_and_user_id(self, debt_id: int, user_id: int) -> Optional[DomainDebt]:
        orm = DebtORM.query.filter_by(id=debt_id, user_id=user_id).first()
        if orm is None:
            return None
        return DomainDebt(
            user_id=orm.user_id,
            lender=orm.lender,
            principal=orm.principal,
            interest_rate=orm.interest_rate,
            start_date=orm.start_date,
            due_date=orm.due_date,
            name=orm.name,
            status=orm.status,
            id=orm.id,
        )

    def get_all_by_user_id(self, user_id: int) -> List[DomainDebt]:
        orms = DebtORM.query.filter_by(user_id=user_id).all()
        return [
            DomainDebt(
                user_id=o.user_id,
                lender=o.lender,
                principal=o.principal,
                interest_rate=o.interest_rate,
                start_date=o.start_date,
                due_date=o.due_date,
                name=o.name,
                status=o.status,
                id=o.id,
            )
            for o in orms
        ]

    def get_active_by_user_id(self, user_id: int) -> List[DomainDebt]:
        orms = DebtORM.query.filter_by(user_id=user_id, status='active').all()
        return [
            DomainDebt(
                user_id=o.user_id,
                lender=o.lender,
                principal=o.principal,
                interest_rate=o.interest_rate,
                start_date=o.start_date,
                due_date=o.due_date,
                name=o.name,
                status=o.status,
                id=o.id,
            )
            for o in orms
        ]

    def calculate_total_principal_by_user_id(self, user_id: int) -> float:
        total = (
            DebtORM.query
            .with_entities(func.coalesce(func.sum(DebtORM.principal), 0))
            .filter(DebtORM.user_id == user_id)
            .filter(DebtORM.status == 'active')
            .scalar()
        )
        return float(total)

    def update(self, entity: DomainDebt) -> DomainDebt:
        orm = DebtORM.query.filter_by(id=entity.id).first()
        if orm is None:
            raise EntityNotFoundError('Debt not found')
        orm.lender = entity.lender
        orm.principal = entity.principal
        orm.interest_rate = entity.interest_rate
        orm.start_date = entity.start_date
        orm.due_date = entity.due_date
        orm.name = entity.name
        orm.status = entity.status
        db.session.flush()
        return entity

    def delete(self, entity_id: int) -> bool:
        orm = DebtORM.query.filter_by(id=entity_id).first()
        if orm is None:
            return False
        db.session.delete(orm)
        return True

    def create(self, **kwargs) -> DomainDebt:
        return DomainDebt(**kwargs)

    def get_all(self):
        orms = DebtORM.query.all()
        return [
            DomainDebt(
                user_id=o.user_id,
                lender=o.lender,
                principal=o.principal,
                interest_rate=o.interest_rate,
                start_date=o.start_date,
                due_date=o.due_date,
                name=o.name,
                status=o.status,
                id=o.id,
            )
            for o in orms
        ]
