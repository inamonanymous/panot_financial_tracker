from app.ext import db, dt

class DebtPayments(db.Model):
    __tablename__ = 'debt_payments'
    id = db.Column(db.Integer, primary_key=True)
    debt_id = db.Column(db.Integer, db.ForeignKey('debts.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, default=dt.now().date)
    remarks = db.Column(db.String(255))

    users = db.relationship("Users", foreign_keys=[user_id], backref=db.backref('debt_payments', lazy=True, cascade='all, delete-orphan'))
    debts = db.relationship("Debts", foreign_keys=[debt_id], backref=db.backref('debt_payments', lazy=True, cascade='all, delete-orphan'))