from app.model.m_Categories import Categories, db
from app.model.m_Income import Income
from app.model.m_Expenses import Expenses
from sqlalchemy.exc import SQLAlchemyError
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService
from sqlalchemy.sql import exists

class CategoriesService(BaseService):
    def insert_category(self, data: dict) -> object:
        """
        Creates a new category with validated and cleaned data.

        Param:
            data: Dictionary
                * user_id : String
                * type : Enum("income", "expense") 
                * name : String  
        Return: 
            Category Persistence: Object
        """
        clean = self.CATEGORY_POLICY.validate_insert_category(data)
        check_category_record = self.get_category_by_name_and_userid(clean["name"], clean["user_id"])
        self.CATEGORY_POLICY.validate_duplicate_category_name_entry(check_category_record)
        new_category = Categories(**clean)
        return self.safe_execute(lambda: self._save(new_category),
                                 error_message="Failed to create category")

    def get_category_by_id(self, category_id: int) -> object:
        """ 
            Get Category record by id
            
            Param:
                * category_id : int
           Return:
                Categories Persistence: Object        
        """
        return Categories.query.filter_by(id=category_id).first()
    
    def get_category_by_name_and_userid(self, name: str, user_id) -> object:
        """ 
            Get Category record by name and user id
            
            Param:
                * name : int
                * user_id : int
            Return:
                Categories Persistence: Object        
        """
        return Categories.query.filter_by(name=name, user_id=user_id).first()

    def get_category_by_id_and_userid(self, category_id: int, user_id: int) -> object:
        """ 
            Get Category record by id and user id
            
            Param:
                * category_id : int
                * user_id : int
            Return:
                Categories Persistence: Object        
        """
        return Categories.query.filter_by(id=category_id, user_id=user_id).first()

    def get_all_categories_by_user(self, user_id: int) -> list:
        """ 
            Returns list of all category objects by a user stored in database
            
            Return:
                Categories Persistence Objects: List        
        """
        return Categories.query.filter_by(user_id=user_id).all()
    
    def get_category_in_use(self, category_id) -> list:
        """
        Return the category object if it is in use (Income or Expenses)

        Param:
            None
        Return: 
            Categories Persistence: Object    
        """
        category_in_use = (
            db.session.query(Categories)
            .filter(Categories.id == category_id)
            .filter(
                exists().where(Income.category_id == Categories.id)
                | exists().where(Expenses.category_id == Categories.id)
            )
            .first()
        )
        return category_in_use

    def edit_category(self, category_id: int, data: dict, user_id) -> object:
        """
        Updates category record with validated and cleaned data.

        Param:
            category_id
            data: Dictionary
                * name : String  
        Return: 
            Categories Persistence: Object
        """
        target_category = self.get_category_by_id_and_userid(category_id, user_id)
        filtered_category_data = self.CATEGORY_POLICY.validate_category_editing(data, target_category)
        category = self.get_category_by_name_and_userid(filtered_category_data["name"], user_id)
        self.CATEGORY_POLICY.validate_duplicate_category_name_entry(category)

        for field, value in filtered_category_data.items():
            setattr(target_category, field, value)
        return self.safe_execute(lambda: self._save(target_category),
                                 error_message="Failed to update category")

    def delete_category(self, category_id: int, user_id: int) -> bool:
        """ 
            Delete category record by id
            Param:
                * id : Int
                * user_id: Int
            Return:
                Boolean
        """
        category = self.get_category_by_id_and_userid(category_id, user_id)
        category_in_use_checker = self.get_category_in_use(category_id)
        self.CATEGORY_POLICY.validate_category_deletion(category, user_id, category_in_use_checker)
        return self.safe_execute(
            lambda: self._delete(category),
            error_message="Failed to delete category"
        )
