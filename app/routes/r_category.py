from flask import Blueprint, render_template, redirect, session, url_for, request
from app.utils.exceptions.ServiceError import ServiceError
from app.routes.functions import require_user_session, get_current_user
from app.service import UOW

category = Blueprint(
    'category',
    __name__,
    template_folder='templates',
    static_folder='statice'
)

@require_user_session
@category.route('/insert_category', methods=['POST'])
def insert_category_route():
    pass