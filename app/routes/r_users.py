from flask import Blueprint, render_template, redirect, session, url_for, request
from functools import wraps
from app.service import US_INS, IS_INS, ES_INS, DS_INS, DPS_INS, STS_INS
from app.utils.exceptions.ServiceError import ServiceError
from app.routes.functions import require_user_session, get_current_user
users = Blueprint(
    'users',
    __name__,
    template_folder='templates',
    static_folder='static'
)


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
    user = get_current_user()
    US_INS.edit_user(user.id, {
        "firstname": "Stephen",
        "lastname": "Joaquin"
    })
    return render_template('auth/pages/dashboard.html', 
                           user=get_current_user(), 
                           total_income=IS_INS.calculate_total_income_by_userid(int(user.id)),
                           total_expense=ES_INS.calculate_total_expense_by_userid(int(user.id)),
                           total_saving_transactions=STS_INS.calculate_total_saving_deposits_by_userid(int(user.id)),
                           user_total_value=US_INS.calculate_current_amount_by_userid(int(user.id))
                           )

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
    
