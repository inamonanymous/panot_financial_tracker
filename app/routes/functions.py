from flask import redirect, session, url_for
from functools import wraps
from typing import Callable, Any, Optional
from app.service import UOW
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
        # Use UserRepository from UoW to fetch user by email
        user = UOW.users.get_by_email(session.get('user_email'))
        if not user:
            raise ServiceError('User not found')
        return user
    else:
        raise ServiceError('No user in session')


def run_action_redirect(
    action: Callable[[], Any],
    success_endpoint: str,
    error_endpoint: Optional[str] = None,
):
    """
    Execute an action and map result to redirect responses.

    Args:
        action: callable containing route action logic
        success_endpoint: endpoint used for successful redirect
        error_endpoint: endpoint used for error redirect (defaults to success_endpoint)
    """
    target_error_endpoint = error_endpoint or success_endpoint

    try:
        action()
        return redirect(url_for(success_endpoint))
    except Exception as exc:
        return redirect(url_for(target_error_endpoint, error_message=str(exc)))


def redirect_on_action(
    success_endpoint: str,
    error_endpoint: Optional[str] = None,
):
    """
    Decorator to standardize action route success/error redirects.

    The wrapped function should run business action logic and does not need
    to return a response; redirect responses are handled here.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return run_action_redirect(
                lambda: fn(*args, **kwargs),
                success_endpoint=success_endpoint,
                error_endpoint=error_endpoint,
            )

        return wrapper

    return decorator