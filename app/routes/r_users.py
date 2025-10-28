from flask import Blueprint, render_template, redirect, session, url_for
from functools import wraps

users = Blueprint(
    'users',
    __name__,
    template_folder='templates',
    static_folder='static'
)

def require_user_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_username' not in session:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs) 
    return wrapper

@users.route('/')
def index():
    return render_template('login.html')

@users.route('/login')
def login():
    pass
