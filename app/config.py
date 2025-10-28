import os
from dotenv import load_dotenv
from app.ext import db

load_dotenv()

class ApplicationConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret')
    SESSION_TYPE = os.getenv('SESSION_TYPE', 'sqlalchemy')
    SESSION_SQLALCHEMY = db
    SESSION_PERMANENT = os.getenv('SESSION_PERMANENT', 'False').lower() == 'true'
    SESSION_USE_SIGNER = os.getenv('SESSION_USE_SIGNER', 'True').lower() == 'true'