from flask import Blueprint, render_template, redirect, session, url_for, request
from functools import wraps
from app.service import US_INS
from app.utils.exceptions.ServiceError import ServiceError

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
    return render_template('public/login.html')

@users.route('/login', methods=['POST', 'GET'])
def login():
    return redirect(url_for('users.dashboard'))

@users.route('/dashboard')
def dashboard():
    return render_template('auth/dashboard.html')

@users.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method != 'POST':
        return render_template('public/register.html')
    
    args = request.form
    """ 
        if args['password'] != args['password2']:
            return render_template('public/register.html', error_message="Passwords doesn't match")
 """
    user_data = {
        'firstname': args['firstname'],
        'lastname': args['lastname'],
        'email': args['email'],
        'password_hash': args['password'],
        'password2': args['password2']
    }
    
    try:
        new_user = US_INS.insert_user(user_data)
        return redirect(url_for('users.index'))
    except ServiceError as e:
        print(type(e))

        return render_template('public/register.html', error_message=str(e))
    

    
