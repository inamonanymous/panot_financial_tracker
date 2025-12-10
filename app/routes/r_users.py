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
        if 'user_email' not in session:
            return redirect(url_for('users.index'))
        return f(*args, **kwargs) 
    return wrapper

def get_current_user():
    x = session.get('user_email')
    print(x)
    print(type(x))
    if 'user_email' in session:
        return US_INS.get_user_by_email(session.get('user_email'))
    else:
        raise ServiceError('No user in session')


@users.route('/', methods=['GET'])
def index():
    return redirect(url_for('users.login'))

@users.route('/login', methods=['POST', 'GET'])
def login():
    if request.method != 'POST':
        email = request.args.get('email') if request.args.get('email') else None
        error_message = request.args.get('error_message') if request.args.get('error_message') else None
        return render_template('public/login.html', email=email, error_message=error_message)
    
    try:
        args = request.form
        user = US_INS.check_login(
            args['email'],
            args['password']
        )
        session['user_email'] = user.email
        return redirect(url_for('users.dashboard'))
    except ServiceError as e:
        return redirect(url_for('users.login', error_message=str(e)))

@users.route('/dashboard')
@require_user_session
def dashboard():
    
    return render_template('auth/pages/dashboard.html', user=get_current_user())

@users.route('/logout')
@require_user_session
def logout():
    session.pop('user_email')
    return redirect(url_for('users.index'))

@users.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method != 'POST':
        return render_template('public/register.html')
    
    args = request.form

    user_data = {
        'firstname': args['firstname'],
        'lastname': args['lastname'],
        'email': args['email'],
        'password_hash': args['password'],
        'password2': args['password2']
    }
    
    try:
        new_user = US_INS.insert_user(user_data)
        return redirect(url_for('users.index', email = new_user.email))
    except ServiceError as e:
        return render_template('public/register.html', error_message=str(e))
    
