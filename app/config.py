from app.ext import db
class ApplicationConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/finance_tracker'
    SECRET_KEY = 'happynation'
    SESSION_TYPE = 'sqlalchemy'

