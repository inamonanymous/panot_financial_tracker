from flask import redirect, session, url_for
from functools import wraps
from app.service import US_INS
from app.utils.exceptions.ServiceError import ServiceError

def require_user_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('users.index'))
        return f(*args, **kwargs) 
    return wrapper

def get_current_user():
    x = session.get('user_email')
    if 'user_email' in session:
        return US_INS.get_user_by_email(session.get('user_email'))
    else:
        raise ServiceError('No user in session')