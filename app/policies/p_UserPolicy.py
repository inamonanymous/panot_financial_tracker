from app.service import check_password_hash, generate_password_hash
from app.policies.BasePolicy import BasePolicy

class UserPolicy(BasePolicy):


    def validate_registration(self, user_data: dict) -> dict:
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

        return clean