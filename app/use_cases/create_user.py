"""Create User Use Case - Orchestrates user registration using UOW and policies."""
from app.model.m_Users import Users
from app.domain.policies.p_UserPolicy import UserPolicy
from app.ext import db
from sqlalchemy.exc import IntegrityError


class CreateUserUseCase:
    """Orchestrates user registration with validation and atomic transaction."""

    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.user_policy = UserPolicy()

    def execute(self, user_data: dict) -> Users:
        """
        Register a new user with validated data.
        
        Args:
            user_data: dict with keys:
                - firstname: str
                - lastname: str
                - email: str
                - password_hash: str (plaintext, will be hashed)
                - password2: str (confirmation)
        
        Returns:
            Users ORM instance (persisted)
        
        Raises:
            Exception: If validation fails or user already exists
        """
        # Validate and clean user data
        filtered_user_data = self.user_policy.validate_user_registration(user_data)

        # Create ORM instance
        new_user = Users(**filtered_user_data)

        # Save within transaction
        try:
            with self.uow.transaction():
                saved_user = self.uow.users.save(new_user)
            return saved_user
        except IntegrityError as e:
            db.session.rollback()
            if "email" in str(e.orig):
                raise Exception("Email already exists. Please use another one")
            raise Exception("User database constraint error")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to register user: {str(e)}")
