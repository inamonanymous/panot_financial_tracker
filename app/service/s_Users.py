from app.service import check_password_hash, generate_password_hash, db
from app.model.m_Users import Users
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.utils.exceptions.ServiceError import ServiceError
from app.service.BaseService import BaseService
from app.ext import dt

class UserService(BaseService):
    def check_login(self, email, password):
        email = self.validate_email_string(email)
        password = self.validate_password_string(
                        password,
                        confirm=None,
                        min_len=8
                    )
        user = Users.query.filter_by(
            email=email
        ).first()
        if not (user and check_password_hash(user.password_hash, password)):
            raise ServiceError("Incorrect Credentials!")


        return user
    
    """     def insert_user(user_data: dict) -> object:
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
    """        

    def insert_user(self, user_data: dict) -> object:
        """ 
        Creates a new user with validated and clean data

        Param: user_data: dict
        Return: User object instance
        """

        user_data['firstname'] = self.validate_string(user_data['firstname'], "Firstname", min_len=2)
        user_data['lastname']  = self.validate_string(user_data['lastname'], "Lastname",  min_len=2)
        user_data['email']     = self.validate_email_string(user_data['email'])
        user_data['password_hash']  = self.validate_password_string(
                        user_data['password_hash'],
                        confirm=user_data.get('password2'),
                        min_len=8
                    )
        
        hashed_password = generate_password_hash(user_data['password_hash'].strip())
        user_data['password_hash'] = hashed_password

        clean = self.create_resource(
            user_data,
            required=['firstname', 'lastname', 'email', 'password_hash'],
            allowed=['firstname', 'lastname', 'email', 'password_hash']
        )


        new_user = Users(**clean)

        return self.safe_execute(lambda: self._save(new_user),
                                    error_message="Failed to create Userw")

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
        

    def _save(self, instance):
        try:
            db.session.add(instance)
            db.session.commit()
            return instance

        except IntegrityError as e:
            db.session.rollback()
            message = str(e.orig)

            if "email" in message:
                raise ServiceError("Email already exists. Please use another one")
            print(message)
            raise ServiceError("User database constraint error")

        except Exception:
            db.session.rollback()
            raise ServiceError("Unexpected database error in UserService")