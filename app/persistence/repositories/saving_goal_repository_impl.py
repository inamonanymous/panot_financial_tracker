from typing import Optional, List
from app.repositories.saving_goal_repository import SavingGoalRepository
from app.model.m_SavingGoals import SavingGoals as SavingGoalORM
from app.ext import db
from app.domain.entities import SavingGoal as DomainSavingGoal
from app.repositories.exceptions import EntityNotFoundError


class SavingGoalRepositoryImpl(SavingGoalRepository):
    def save(self, entity: DomainSavingGoal) -> DomainSavingGoal:
        orm = SavingGoalORM(
            user_id=entity.user_id,
            name=entity.name,
            target_amount=entity.target_amount,
            target_date=entity.target_date,
            remarks=entity.remarks,
        )
        db.session.add(orm)
        db.session.flush()
        entity.id = orm.id
        return entity

    def get_by_id(self, goal_id: int) -> Optional[DomainSavingGoal]:
        orm = SavingGoalORM.query.filter_by(id=goal_id).first()
        if orm is None:
            return None
        goal = DomainSavingGoal(
            user_id=orm.user_id,
            name=orm.name,
            target_amount=orm.target_amount,
            target_date=orm.target_date,
            remarks=orm.remarks,
            id=orm.id,
        )
        goal.current_amount = getattr(orm, 'current_amount', 0.0)
        return goal

    def get_by_id_and_user_id(self, goal_id: int, user_id: int) -> Optional[DomainSavingGoal]:
        orm = SavingGoalORM.query.filter_by(id=goal_id, user_id=user_id).first()
        if orm is None:
            return None
        goal = DomainSavingGoal(
            user_id=orm.user_id,
            name=orm.name,
            target_amount=orm.target_amount,
            target_date=orm.target_date,
            remarks=orm.remarks,
            id=orm.id,
        )
        goal.current_amount = getattr(orm, 'current_amount', 0.0)
        return goal

    def get_all_by_user_id(self, user_id: int) -> List[DomainSavingGoal]:
        orms = SavingGoalORM.query.filter_by(user_id=user_id).all()
        goals = []
        for o in orms:
            g = DomainSavingGoal(
                user_id=o.user_id,
                name=o.name,
                target_amount=o.target_amount,
                target_date=o.target_date,
                remarks=o.remarks,
                id=o.id,
            )
            g.current_amount = getattr(o, 'current_amount', 0.0)
            goals.append(g)
        return goals

    def get_active_by_user_id(self, user_id: int) -> List[DomainSavingGoal]:
        orms = SavingGoalORM.query.filter_by(user_id=user_id).all()
        # active = not completed
        goals = []
        for o in orms:
            g = DomainSavingGoal(
                user_id=o.user_id,
                name=o.name,
                target_amount=o.target_amount,
                target_date=o.target_date,
                remarks=o.remarks,
                id=o.id,
            )
            g.current_amount = getattr(o, 'current_amount', 0.0)
            if not g.is_completed():
                goals.append(g)
        return goals

    def update(self, entity: DomainSavingGoal) -> DomainSavingGoal:
        orm = SavingGoalORM.query.filter_by(id=entity.id).first()
        if orm is None:
            raise EntityNotFoundError('Saving goal not found')
        orm.name = entity.name
        orm.target_amount = entity.target_amount
        orm.target_date = entity.target_date
        orm.remarks = entity.remarks
        db.session.flush()
        return entity

    def delete(self, entity_id: int) -> bool:
        orm = SavingGoalORM.query.filter_by(id=entity_id).first()
        if orm is None:
            return False
        db.session.delete(orm)
        return True

    def create(self, **kwargs) -> DomainSavingGoal:
        return DomainSavingGoal(**kwargs)

    def get_all(self):
        orms = SavingGoalORM.query.all()
        goals = []
        for o in orms:
            g = DomainSavingGoal(
                user_id=o.user_id,
                name=o.name,
                target_amount=o.target_amount,
                target_date=o.target_date,
                remarks=o.remarks,
                id=o.id,
            )
            g.current_amount = getattr(o, 'current_amount', 0.0)
            goals.append(g)
        return goals
