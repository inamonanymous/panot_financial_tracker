from flask import Flask
from app.ext import db
from app.config import ApplicationConfig


def generate_tables(app):
    """Create DB tables if missing. Models are imported lazily to avoid
    executing heavy imports at module import time.
    """
    with app.app_context():
        # Import models lazily
        from app.model.m_Admin import Admin
        from app.model.m_Categories import Categories
        from app.model.m_DebtPayments import DebtPayments
        from app.model.m_Debts import Debts
        from app.model.m_Expenses import Expenses
        from app.model.m_Income import Income
        from app.model.m_SavingGoals import SavingGoals
        from app.model.m_SavingTransactions import SavingTransactions
        from app.model.m_Users import Users

        db.create_all()


def create_app():
    app = Flask(__name__)
    app.config.from_object(ApplicationConfig)

    # Register blueprints and extensions lazily
    from app.routes.r_users import users
    from app.routes.r_income import income
    from app.routes.r_expense import expense
    from flask_migrate import Migrate
    from flask_session import Session

    app.register_blueprint(users)
    app.register_blueprint(income)
    app.register_blueprint(expense)

    db.init_app(app)
    migrate = Migrate(app, db)
    session = Session(app)

    generate_tables(app)

    return app
    