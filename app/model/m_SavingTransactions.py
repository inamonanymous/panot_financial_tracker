from app.ext import db, dt

class SavingTransactions(db.Model):
    __tablename__ = 'saving_transactions'
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('saving_goals.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    txt_type = db.Column(db.Enum("deposit", "withdraw"), nullable=False, default='deposit')
    income_id = db.Column(db.Integer, db.ForeignKey('income.id', ondelete="CASCADE"), nullable=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id', ondelete="CASCADE"), nullable=True)

    income = db.relationship("Income", foreign_keys=[income_id], backref=db.backref('saving_transactions', lazy=True, cascade='all, delete-orphan'))
    expenses = db.relationship("Expenses", foreign_keys=[expense_id], backref=db.backref('saving_transactions', lazy=True, cascade='all, delete-orphan'))

    goals = db.relationship("SavingGoals", foreign_keys=[goal_id], backref=db.backref('saving_transactions', lazy=True, cascade='all, delete-orphan'))
    users = db.relationship("Users", foreign_keys=[user_id], backref=db.backref('saving_transactions', lazy=True, cascade='all, delete-orphan'))