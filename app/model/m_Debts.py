from app.ext import db, dt

class Debts(db.Model):
    __tablename__ = 'debts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    lender = db.Column(db.String(150), nullable=False)
    principal = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    status = db.Column(db.Enum("active", "closed"), default="active")
    created_at = db.Column(db.DateTime, default=dt.now())

    users = db.relationship("Users", foreign_keys=[user_id], backref=db.backref('debts', lazy=True, cascade='all, delete-orphan'))


