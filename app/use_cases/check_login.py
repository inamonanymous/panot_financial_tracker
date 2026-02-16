"""Check Login Use Case - Authenticates user credentials."""
from werkzeug.security import check_password_hash
from app.domain.policies.p_UserPolicy import UserPolicy
from app.domain.entities import User as DomainUser

class CheckLoginUseCase:
    """Authenticates user login with email and password."""

    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.user_policy = UserPolicy()

    def execute(self, email: str, password: str) -> DomainUser:
        """
        Authenticate user credentials.
        
        Args:
            email: User email
            password: User password (plaintext)
        
        Returns:
            DomainUser instance if authentication succeeds
        
        Raises:
            Exception: If email not found or password incorrect
        """
        # Get user by email using repository
        user_orm = self.uow.users.get_by_email(email)
        
        # Validate with policy
        self.user_policy.validate_login(email, password, user_orm)
        
        return user_orm
