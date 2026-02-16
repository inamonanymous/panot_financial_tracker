from typing import Optional, List
from app.repositories.expense_repository import ExpenseRepository
from app.model.m_Expenses import Expenses as ExpenseORM
from app.ext import db
from app.domain.entities import Expense as DomainExpense
from app.repositories.exceptions import EntityNotFoundError
from sqlalchemy import func


class ExpenseRepositoryImpl(ExpenseRepository):
    def save(self, entity: DomainExpense) -> DomainExpense:
        orm = ExpenseORM(
            user_id=entity.user_id,
            category_id=entity.category_id,
            payee=entity.payee,
            amount=entity.amount,
            expense_date=entity.expense_date,
            payment_method=entity.payment_method,
            remarks=entity.remarks,
        )
        db.session.add(orm)
        db.session.flush()
        entity.id = orm.id
        return entity

    def get_by_id(self, expense_id: int) -> Optional[DomainExpense]:
        orm = ExpenseORM.query.filter_by(id=expense_id).first()
        if orm is None:
            return None
        return DomainExpense(
            user_id=orm.user_id,
            category_id=orm.category_id,
            payee=orm.payee,
            amount=orm.amount,
            expense_date=orm.expense_date,
            payment_method=orm.payment_method,
            remarks=orm.remarks,
            id=orm.id,
        )

    def get_by_id_and_user_id(self, expense_id: int, user_id: int) -> Optional[DomainExpense]:
        orm = ExpenseORM.query.filter_by(id=expense_id, user_id=user_id).first()
        if orm is None:
            return None
        return DomainExpense(
            user_id=orm.user_id,
            category_id=orm.category_id,
            payee=orm.payee,
            amount=orm.amount,
            expense_date=orm.expense_date,
            payment_method=orm.payment_method,
            remarks=orm.remarks,
            id=orm.id,
        )

    def get_all_by_user_id(self, user_id: int) -> List[DomainExpense]:
        orms = ExpenseORM.query.filter_by(user_id=user_id).all()
        return [
            DomainExpense(
                user_id=o.user_id,
                category_id=o.category_id,
                payee=o.payee,
                amount=o.amount,
                expense_date=o.expense_date,
                payment_method=o.payment_method,
                remarks=o.remarks,
                id=o.id,
            )
            for o in orms
        ]

    def calculate_total_by_user_id(self, user_id: int) -> float:
        total = (
            ExpenseORM.query
            .with_entities(func.coalesce(func.sum(ExpenseORM.amount), 0))
            .filter(ExpenseORM.user_id == user_id)
            .scalar()
        )
        return float(total)

    def get_by_category_id(self, category_id: int) -> List[DomainExpense]:
        orms = ExpenseORM.query.filter_by(category_id=category_id).all()
        return [
            DomainExpense(
                user_id=o.user_id,
                category_id=o.category_id,
                payee=o.payee,
                amount=o.amount,
                expense_date=o.expense_date,
                payment_method=o.payment_method,
                remarks=o.remarks,
                id=o.id,
            )
            for o in orms
        ]

    def update(self, entity: DomainExpense) -> DomainExpense:
        orm = ExpenseORM.query.filter_by(id=entity.id).first()
        if orm is None:
            raise EntityNotFoundError('Expense not found')
        orm.payee = entity.payee
        orm.amount = entity.amount
        orm.payment_method = entity.payment_method
        orm.remarks = entity.remarks
        orm.category_id = entity.category_id
        orm.expense_date = entity.expense_date
        db.session.flush()
        return entity

    def create(self, **kwargs) -> DomainExpense:
        return DomainExpense(**kwargs)

    def delete(self, entity_id: int) -> bool:
        orm = ExpenseORM.query.filter_by(id=entity_id).first()
        if orm is None:
            return False
        db.session.delete(orm)
        return True

    def get_all(self):
        orms = ExpenseORM.query.all()
        return [
            DomainExpense(
                user_id=o.user_id,
                category_id=o.category_id,
                payee=o.payee,
                amount=o.amount,
                expense_date=o.expense_date,
                payment_method=o.payment_method,
                remarks=o.remarks,
                id=o.id,
            )
            for o in orms
        ]
