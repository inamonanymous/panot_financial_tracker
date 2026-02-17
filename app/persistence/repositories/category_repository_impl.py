from typing import Optional, List
from app.repositories.category_repository import CategoryRepository
from app.model.m_Categories import Categories as CategoryORM
from app.ext import db
from app.domain.entities import Category as DomainCategory
from app.repositories.exceptions import EntityNotFoundError
from sqlalchemy.sql import exists


class CategoryRepositoryImpl(CategoryRepository):
    def save(self, entity: DomainCategory) -> DomainCategory:
        orm = CategoryORM(
            user_id=entity.user_id,
            type=entity.type,
            name=entity.name,
            description=entity.description,
        )
        db.session.add(orm)
        db.session.flush()
        entity.id = orm.id
        return entity

    def get_by_id(self, category_id: int) -> Optional[DomainCategory]:
        orm = CategoryORM.query.filter_by(id=category_id).first()
        if orm is None:
            return None
        return DomainCategory(
            user_id=orm.user_id,
            type=orm.type,
            name=orm.name,
            description=orm.description,
            id=orm.id,
        )

    def get_by_id_and_user_id(self, category_id: int, user_id: int) -> Optional[DomainCategory]:
        orm = CategoryORM.query.filter_by(id=category_id, user_id=user_id).first()
        if orm is None:
            return None
        return DomainCategory(
            user_id=orm.user_id,
            type=orm.type,
            name=orm.name,
            description=orm.description,
            id=orm.id,
        )

    def get_by_name_and_user_id(self, name: str, user_id: int) -> Optional[DomainCategory]:
        orm = CategoryORM.query.filter_by(name=name, user_id=user_id).first()
        if orm is None:
            return None
        return DomainCategory(
            user_id=orm.user_id,
            type=orm.type,
            name=orm.name,
            description=orm.description,
            id=orm.id,
        )

    def get_all_by_user_id(self, user_id: int) -> List[DomainCategory]:
        orms = CategoryORM.query.filter_by(user_id=user_id).all()
        return [
            DomainCategory(
                user_id=o.user_id,
                type=o.type,
                name=o.name,
                description=o.description,
                id=o.id,
            )
            for o in orms
        ]

    def get_all_by_user_and_type(self, user_id: int, category_type: str) -> List[DomainCategory]:
        orms = CategoryORM.query.filter_by(user_id=user_id, type=category_type).all()
        return [
            DomainCategory(
                user_id=o.user_id,
                type=o.type,
                name=o.name,
                description=o.description,
                id=o.id,
            )
            for o in orms
        ]

    def exists_with_name_and_user(self, name: str, user_id: int) -> bool:
        return CategoryORM.query.filter_by(name=name, user_id=user_id).first() is not None

    def is_in_use(self, category_id: int) -> bool:
        # Check if any income or expense references this category
        from app.model.m_Income import Income as IncomeORM
        from app.model.m_Expenses import Expenses as ExpenseORM

        income_exists = db.session.query(exists().where(IncomeORM.category_id == category_id)).scalar()
        expense_exists = db.session.query(exists().where(ExpenseORM.category_id == category_id)).scalar()
        return bool(income_exists or expense_exists)

    def update(self, entity: DomainCategory) -> DomainCategory:
        orm = CategoryORM.query.filter_by(id=entity.id).first()
        if orm is None:
            raise EntityNotFoundError('Category not found')
        orm.name = entity.name
        orm.description = entity.description
        db.session.flush()
        return entity

    def delete(self, entity_id: int) -> bool:
        orm = CategoryORM.query.filter_by(id=entity_id).first()
        if orm is None:
            return False
        db.session.delete(orm)
        return True

    def create(self, **kwargs) -> DomainCategory:
        return DomainCategory(**kwargs)

    def get_all(self):
        orms = CategoryORM.query.all()
        return [
            DomainCategory(
                user_id=o.user_id,
                type=o.type,
                name=o.name,
                description=o.description,
                id=o.id,
            )
            for o in orms
        ]
