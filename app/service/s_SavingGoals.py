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
    def get_saving_goals_by_id_and_userid(self, saving_goals_id: int, user_id: int) -> object:
        return SavingGoals.query.filter_by(id=saving_goals_id, user_id=user_id).first()
    
    # -----------------------------------------------------
    # GET ALL SAVING_GOALS BY USER
    # -----------------------------------------------------  
    def get_all_saving_goals_by_user(self, user_id: int):
        return SavingGoals.query.filter_by(user_id=user_id).all()
    

    # -----------------------------------------------------
    # UPDATE SAVING_GOALS
    # -----------------------------------------------------  
    def edit_saving_goals(self, saving_goals_id: int, user_id: int, data: dict) -> object:
        target_saving_goal = self.get_saving_goals_by_id_and_userid(saving_goals_id, user_id)
        
        if target_saving_goal is None:
            raise ServiceError("No debt record found")
        
        clean = self.update_resource(
            data,
            allowed=['name', 'target_date', 'remarks']
        )

        if clean['name']:
            target_saving_goal.name = clean['name'],
        if clean['target_date']:
            target_saving_goal.target_date = clean['target_date']
        if clean['remarks']:
            target_saving_goal.remarks = clean['remarks']
        
        return self.safe_execute(lambda: self._save(target_saving_goal),
                                 error_message="Failed to update saving goals")
    
    
    # -----------------------------------------------------
    # DELETE SAVING_GOALS
    # -----------------------------------------------------  
    def delete_saving_goals(self, id: int, user_id: int) -> bool:
        saving_goal = self.get_saving_goals_by_id_and_userid(id, user_id)

        return self.safe_execute(
            lambda: self._delete(saving_goal),
            error_message="Failed to delete saving_goal"
        )
