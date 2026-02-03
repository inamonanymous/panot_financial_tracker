from flask import Blueprint, render_template, redirect, session, url_for, request
from functools import wraps
from app.utils.exceptions.ServiceError import ServiceError
from app.routes.functions import require_user_session, get_current_user
from app.service import UOW
from app.use_cases.create_debt_payment import CreateDebtPaymentUseCase
from app.use_cases.dashboard_reporting import DashboardReportingUseCase
from app.use_cases.create_user import CreateUserUseCase
from app.use_cases.check_login import CheckLoginUseCase
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
        user = CheckLoginUseCase(UOW).execute(
            args['email'],
            args['password']
        )
        session['user_email'] = user.email
        return redirect(url_for('users.dashboard'))
    except Exception as e:
        return redirect(url_for('users.login', error_message=str(e)))

import datetime
@users.route('/dashboard')
@require_user_session
def dashboard():
    user = get_current_user()
    user_id = int(user.id)
    
    # Use new DashboardReportingUseCase with repositories
    reporting_use_case = DashboardReportingUseCase(UOW)
    dashboard_data = reporting_use_case.execute(user_id)
    
    return render_template('auth/pages/dashboard.html', 
                           user=user,
                           total_income=dashboard_data["total_income"],
                           total_expense=dashboard_data["total_expense"],
                           total_saving_transactions=dashboard_data["total_saving_deposits"],
                           user_total_value=dashboard_data["user_total_value"]
                           )


@users.route('/debt_payment', methods=['POST'])
@require_user_session
def create_debt_payment():
    user = get_current_user()
    args = request.form
    debt_data = {
        "user_id": int(user.id),
        "debt_id": int(args.get('debt_id')),
    }

    expense_data = {
        "user_id": int(user.id),
        "amount": float(args.get('amount')),
        "expense_date": args.get('expense_date'),
        "payment_method": args.get('payment_method'),
        "remarks": args.get('remarks', ""),
    }

    use_case = CreateDebtPaymentUseCase(UOW)
    try:
        dp = use_case.execute(debt_data, expense_data)
        return redirect(url_for('users.dashboard'))
    except Exception as e:
        return redirect(url_for('users.dashboard', error_message=str(e)))

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
    
    # Use new CreateUserUseCase with repositories
    use_case = CreateUserUseCase(UOW)
    try:
        new_user = use_case.execute(user_data)
        return redirect(url_for('users.index', email = new_user.email))
    except Exception as e:
        return render_template('public/register.html', error_message=str(e))
    
