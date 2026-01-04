from app.model.m_SavingGoals import db, SavingGoals
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService

class SavingGoalsService(BaseService):
    # -----------------------------------------------------
    # CREATE SAVING_GOALS 
    # -----------------------------------------------------            
    def insert_saving_goals(self, data: dict) -> object:
        """ 
        Creates a new saving_goals with validated and cleaned data.
        """
        clean = self.create_resource(
            data,
            required=[
                "name",
                "target_amount",
                "target_date",
                "remarks"
            ],
            allowed=[
                "name",
                "target_amount",
                "target_date",
                "remarks"
            ]
        )
        new_saving_goals = SavingGoals(**clean)
        
        return self.safe_execute(lambda: self._save(new_saving_goals),
                                 error_message="Failed to create new saving goals")
    
    # -----------------------------------------------------
    # GET SAVING_GOALS BY ID
    # -----------------------------------------------------        
    def get_saving_goals_by_id(self, saving_goals_id: int) -> object:
        return SavingGoals.query.filter_by(id=saving_goals_id).first()
    
    # -----------------------------------------------------
    # CREATE SAVING_GOALS BY ID AND USER ID
    # -----------------------------------------------------        
    def get_saving_goals_by_user_and_id(self, saving_goals_id: int, user_id: int) -> object:
        return SavingGoals.query.filter_by(id=saving_goals_id, user_id=user_id).first()
    
