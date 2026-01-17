import os
from dotenv import load_dotenv
from app.ext import db
from datetime import timedelta

load_dotenv()

class ApplicationConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_TYPE = os.getenv('SESSION_TYPE')
    SESSION_SQLALCHEMY = db
    SESSION_PERMANENT = os.getenv('SESSION_PERMANENT').lower() == 'false'
    SESSION_USE_SIGNER = os.getenv('SESSION_USE_SIGNER').lower() == 'true'
    PERMANENT_SESSION_LIFETIME = timedelta(int(os.getenv('PERMANENT_SESSION_LIFETIME')))