from app.model.m_Categories import Categories, db
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt

class CategoriesService:
    def insert_category(self, user_id: int, type: str, name: str) -> object:
        try:
            category_entry = Categories(
                user_id = user_id,
                type=type,
                name=name
            )
            db.session.add(category_entry)
            db.session.commit()
            return category_entry
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return None

    def get_category_by_id(self, id: int) -> object:
        return Categories.query.filter_by(id=id).first()
    
    def get_all_categories_by_user(self, user_id: int) -> list:
        return Categories.query.filter_by(user_id=user_id).all()
    
    def edit_category(self, id: int, name: str) -> object:
        try:
            target_category = Categories.query.filter_by(id=id).first()
            if not target_category:
                raise Exception(f"Category-{id} not found")
            target_category.name = name
            db.session.commit()
            return target_category
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return None
        
    def delete_category(self, id: int) -> bool:
        try:
            target_category = Categories.query.filter_by(id=id).first()
            if not target_category:
                raise Exception(f"Category-{id} not found")
            db.session.delete(target_category)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return False