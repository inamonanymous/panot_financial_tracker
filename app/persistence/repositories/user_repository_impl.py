from app.repositories.user_repository import UserRepository
from app.model.m_Users import Users as UserORM
from app.ext import db
from app.domain.entities import User as DomainUser
from app.repositories.exceptions import EntityNotFoundError
from typing import Optional


class UserRepositoryImpl(UserRepository):
    def save(self, entity: DomainUser) -> DomainUser:
        orm = UserORM(
            firstname=entity.firstname,
            lastname=entity.lastname,
            email=entity.email,
            password_hash=entity.password_hash,
            current_value=getattr(entity, 'current_value', 0.0)
        )
        db.session.add(orm)
        db.session.flush()
        entity.id = orm.id
        return entity

    def get_by_email(self, email: str) -> Optional[DomainUser]:
        orm = UserORM.query.filter_by(email=email).first()
        if orm is None:
            return None
        return DomainUser(
            firstname=orm.firstname,
            lastname=orm.lastname,
            email=orm.email,
            password_hash=orm.password_hash,
            id=orm.id,
        )

    def get_by_id(self, user_id: int) -> Optional[DomainUser]:
        orm = UserORM.query.filter_by(id=user_id).first()
        if orm is None:
            return None
        return DomainUser(
            firstname=orm.firstname,
            lastname=orm.lastname,
            email=orm.email,
            password_hash=orm.password_hash,
            id=orm.id,
        )

    def update(self, entity: DomainUser) -> DomainUser:
        orm = UserORM.query.filter_by(id=entity.id).first()
        if orm is None:
            raise EntityNotFoundError("User not found")
        orm.firstname = entity.firstname
        orm.lastname = entity.lastname
        if entity.password_hash:
            orm.password_hash = entity.password_hash
        orm.current_value = getattr(entity, 'current_value', orm.current_value)
        db.session.flush()
        return entity

    def delete(self, entity_id: int) -> bool:
        orm = UserORM.query.filter_by(id=entity_id).first()
        if orm is None:
            return False
        db.session.delete(orm)
        return True

    def get_all(self):
        orms = UserORM.query.all()
        return [
            DomainUser(
                firstname=o.firstname,
                lastname=o.lastname,
                email=o.email,
                password_hash=o.password_hash,
                id=o.id,
            )
            for o in orms
        ]
