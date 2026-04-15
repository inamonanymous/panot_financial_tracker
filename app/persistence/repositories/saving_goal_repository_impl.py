from typing import Optional, List
from app.repositories.saving_goal_repository import SavingGoalRepository
from app.model.m_SavingGoals import SavingGoals as SavingGoalORM
from app.model.m_SavingTransactions import SavingTransactions as SavingTransactionsORM
from app.model.m_Income import Income
from app.model.m_Expenses import Expenses
from app.ext import db
from app.domain.entities import SavingGoal as DomainSavingGoal
from app.repositories.exceptions import EntityNotFoundError
from sqlalchemy import func


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
            created_at=orm.created_at,
            id=orm.id,
        )
        goal.current_amount = self.calculate_current_amount(goal_id)
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
            created_at=orm.created_at,
            id=orm.id,
        )
        goal.current_amount = self.calculate_current_amount(goal_id)
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
                created_at=o.created_at,
                id=o.id,
            )
            g.current_amount = self.calculate_current_amount(o.id)
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
                created_at=o.created_at,
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
            g.current_amount = self.calculate_current_amount(o.id)
            goals.append(g)
        return goals

    def calculate_current_amount(self, goal_id: int) -> float:
        """Calculate current amount for a saving goal (deposits - withdrawals)."""
        # Sum deposits from income
        deposits = (
            db.session.query(func.coalesce(func.sum(Income.amount), 0))
            .join(
                SavingTransactionsORM,
                SavingTransactionsORM.income_id == Income.id
            )
            .filter(SavingTransactionsORM.goal_id == goal_id)
            .filter(SavingTransactionsORM.txt_type == "deposit")
            .scalar()
        )
        
        # Sum withdrawals from expenses
        withdrawals = (
            db.session.query(func.coalesce(func.sum(Expenses.amount), 0))
            .join(
                SavingTransactionsORM,
                SavingTransactionsORM.expense_id == Expenses.id
            )
            .filter(SavingTransactionsORM.goal_id == goal_id)
            .filter(SavingTransactionsORM.txt_type == "withdraw")
            .scalar()
        )
        
        return float(deposits - withdrawals)
