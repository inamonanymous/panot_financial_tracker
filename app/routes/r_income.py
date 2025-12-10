from flask import Blueprint, render_template, redirect, session, url_for, request
from functools import wraps
from app.service import US_INS
from app.utils.exceptions.ServiceError import ServiceError
from app.routes.r_users import users as UserRoute

income = Blueprint(
    'income',
    __name__,
    template_folder='templates',
    static_folder='statice'
)

