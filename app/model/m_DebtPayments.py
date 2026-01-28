from app.ext import db, dt

class DebtPayments(db.Model):
    __tablename__ = 'debt_payments'
    id = db.Column(db.Integer, primary_key=True)
    debt_id = db.Column(db.Integer, db.ForeignKey('debts.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    income_id = db.Column(db.Integer, db.ForeignKey('income.id', ondelete="CASCADE"), nullable=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id', ondelete="CASCADE"), nullable=True)
    pymt_type = db.Column(db.Enum("deposit", "withdraw"), nullable=False, default='deposit')
    
    income = db.relationship("Income", foreign_keys=[income_id], backref=db.backref('debt_payments', lazy=True, cascade='all, delete-orphan'))
    expenses = db.relationship("Expenses", foreign_keys=[expense_id], backref=db.backref('debt_payments', lazy=True, cascade='all, delete-orphan'))
    users = db.relationship("Users", foreign_keys=[user_id], backref=db.backref('debt_payments', lazy=True, cascade='all, delete-orphan'))
    debts = db.relationship("Debts", foreign_keys=[debt_id], backref=db.backref('debt_payments', lazy=True, cascade='all, delete-orphan'))