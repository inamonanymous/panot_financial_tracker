from app.service import check_password_hash, generate_password_hash, db
from app.model.m_Users import Users
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt

class UserService:

    def insert_user(user_data: dict) -> object:
        try:
            user_entry = Users(
                firstname=user_data['firstname'].strip(),
                lastname=user_data['lastname'].strip(),
                email=user_data['email'].strip(),
                password_hash=user_data['password'].strip(),
            )
            db.session.add(user_data)
            db.session.commit()
            return user_entry
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return None
        
    def get_user_by_id(id: int) -> object:
        return Users.query.filter_by(id=id).first()
    
    def get_all_users():
        return Users.query.all()
    
    def edit_user(id: int, user_data: dict) -> object:
        try:
            target_user = Users.query.filter_by(id=id).first()
            if not target_user:
                raise Exception(f"User-{id} not found")
            target_user.firstname = user_data['firstname']
            target_user.lastname = user_data['lastname']
            target_user.updated_at = dt.now()
            db.session.commit()
            return target_user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return None
        
    def delete_user(id: int) -> bool:
        try:
            target_user = Users.query.filter_by(id=id).first()
            if not target_user:
                raise Exception(f"User-{id} not found")
            db.session.delete(target_user)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            print(e)
            return False