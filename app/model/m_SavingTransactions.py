from app.ext import db, dt

class SavingTransactions(db.Model):
    __tablename__ = 'saving_transactions'
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('saving_goals.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    txt_type = db.Column(db.Enum("deposit", "withdraw"), nullable=False, default='deposit')
    amount = db.Column(db.Float, nullable=False, default=1.0)
    txt_date = db.Column(db.Date, default=dt.now().date, nullable=False)
    remarks = db.Column(db.String(255))

    goals = db.relationship("SavingGoals", foreign_keys=[goal_id], backref=db.backref('saving_transactions', lazy=True, cascade='all, delete-orphan'))
    users = db.relationship("Users", foreign_keys=[user_id], backref=db.backref('saving_transactions', lazy=True, cascade='all, delete-orphan'))