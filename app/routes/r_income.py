from flask import Blueprint, render_template, redirect, session, url_for, request
from functools import wraps
from app.service import US_INS, IS_INS
from app.utils.exceptions.ServiceError import ServiceError
from app.routes.r_users import users as UserRoute
from app.routes.functions import require_user_session, get_current_user

income = Blueprint(
    'income',
    __name__,
    template_folder='templates',
    static_folder='statice'
)

@require_user_session
@income.route('/income')
def income_page():
    user = get_current_user()
    return render_template("auth/pages/income.html", user=user, all_income=IS_INS.get_all_income_by_user(user.id))