from app.service import check_password_hash, generate_password_hash, db
from app.model.m_Users import Users
from sqlalchemy.exc import SQLAlchemyError
from app.ext import dt

class UserService:
    def check_login(self, email, password):
        user = Users.query.filter_by(
            email=email.strip()
        ).first()
        if not (user and check_password_hash(user.password_hash, password.strip())):
            return None
        return user
    
    def insert_user(user_data: dict) -> object:
        try:
            # Basic validation
            required_fields = ['firstname', 'lastname', 'email', 'password']
            for field in required_fields:
                if field not in user_data or not str(user_data[field]).strip():
                    raise ValueError(f"Missing or empty field: {field}")

            # Hash the password securely
            hashed_password = generate_password_hash(user_data['password'].strip())

            # Create user object
            user_entry = Users(
                firstname=user_data['firstname'].strip(),
                lastname=user_data['lastname'].strip(),
                email=user_data['email'].strip().lower(),
                password_hash=hashed_password
            )

            # Add and commit
            db.session.add(user_entry)
            db.session.commit()
            return user_entry
        except (SQLAlchemyError, ValueError) as e:
            db.session.rollback()
            print(f"Error inserting user: {e}")
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

            # Allowed fields with expected data types
            allowed_fields = {
                'firstname': str,
                'lastname': str,
            }

            for field, expected_type in allowed_fields.items():
                if field in user_data and user_data[field] is not None:
                    value = user_data[field]

                    # Make sure value is a string (and not empty)
                    if isinstance(value, expected_type) and str(value).strip():
                        setattr(target_user, field, value)

            target_user.updated_at = dt.now()
            db.session.commit()
            return target_user

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error: {e}")
            return None

        except Exception as e:
            db.session.rollback()
            print(f"Error editing user: {e}")
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