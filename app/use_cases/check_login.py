"""Check Login Use Case - Authenticates user credentials."""
from werkzeug.security import check_password_hash
from app.model.m_Users import Users
from app.domain.policies.p_UserPolicy import UserPolicy


class CheckLoginUseCase:
    """Authenticates user login with email and password."""

    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.user_policy = UserPolicy()

    def execute(self, email: str, password: str) -> Users:
        """
        Authenticate user credentials.
        
        Args:
            email: User email
            password: User password (plaintext)
        
        Returns:
            Users ORM instance if authentication succeeds
        
        Raises:
            Exception: If email not found or password incorrect
        """
        # Get user by email using repository
        user_orm = Users.query.filter_by(email=email).first()
        
        # Validate with policy
        self.user_policy.validate_login(email, password, user_orm)
        
        return user_orm
