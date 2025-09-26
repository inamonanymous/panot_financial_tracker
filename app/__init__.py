from flask import Flask
from flask_migrate import Migrate
from app.ext import db
from app.config import ApplicationConfig
from app.model.m_Admin import Admin
from app.model.m_Categories import Categories
from app.model.m_DebtPayments import DebtPayments
from app.model.m_Debts import Debts
from app.model.m_Expenses import Expenses
from app.model.m_Income import Income
from app.model.m_SavingGoals import SavingGoals
from app.model.m_SavingTransactions import SavingTransactions
from app.model.m_Users import Users


def generate_tables(app):
    with app.app_context():
        Admin, Categories, DebtPayments, Debts, Expenses, Income, SavingGoals, SavingTransactions
        db.create_all()

def create_app():
    app = Flask(__name__)
    app.config.from_object(ApplicationConfig)
    db.init_app(app)
    migrate = Migrate(app, db)

    generate_tables(app)

    return app
    