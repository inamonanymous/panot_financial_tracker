from app.service import check_password_hash, generate_password_hash
from app.domain.policies.BasePolicy import BasePolicy
from app.utils.exceptions.PolicyError import PolicyError
import re

class UserPolicy(BasePolicy):
    def validate_login(self, email: str, password: str, user) -> None:
        email = self.validate_email_string(email)

        password = self.validate_password_string(
            password,
            confirm=None,
            min_len=8
        )

        if not user:
            raise PolicyError("Incorrect credentials")

        if not check_password_hash(user.password_hash, password):
            raise PolicyError("Invalid Password")

    def validate_user_registration(self, user_data: dict) -> dict:
        user_data['firstname'] = self.validate_user_name(
            user_data['firstname'], 
            field_name="Firstname"
        )
        user_data['lastname']  = self.validate_user_name(
            user_data['lastname'], 
            field_name="Lastname"
        )
        user_data['email']     = self.validate_email_string(user_data['email'])
        user_data['password_hash']  = self.validate_password_string(
                        user_data['password_hash'],
                        confirm=user_data.get('password2'),
                        min_len=8
                    )
        
        hashed_password = generate_password_hash(user_data['password_hash'].strip())
        user_data['password_hash'] = hashed_password

        filtered_user_data = self.create_resource(
            user_data,
            required=['firstname', 'lastname', 'email', 'password_hash'],
            allowed=['firstname', 'lastname', 'email', 'password_hash']
        )

        return filtered_user_data
    
    def validate_user_editing(self, user_data: dict, user: object) -> dict:
        if user is None:
            raise PolicyError(f"User not found")

        clean = self.update_resource(
            user_data,
            allowed=["firstname", "lastname"]
        )

        if "firstname" in clean:
            clean["firstname"] = self.validate_user_name(
                value=clean["firstname"], 
                field_name="Firstname"
            )

        if "lastname" in clean:
            clean["lastname"] = self.validate_user_name(
                value=clean["lastname"], 
                field_name="Lastname"
            )
        
        return clean
    
    def validate_user_name(self, value: str, *, field_name: str) -> str:
        value = self.validate_string(value, field_name, min_len=2)

        if not re.fullmatch(r"^[A-Za-z]+(?: [A-Za-z]+)*$", value):
            raise PolicyError(
                f"{field_name} must contain letters only, with single spaces between words"
            )

        return value
