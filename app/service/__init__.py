from werkzeug.security import check_password_hash, generate_password_hash
from app.ext import db
from app.service.s_Users import UserService 
from app.service.s_Admin import AdminService
from app.service.s_Income import IncomeService

US_INS = UserService()
IN_INS = IncomeService()