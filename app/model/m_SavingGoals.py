from app.ext import db, dt

class SavingGoals(db.Model):
    __tablename__ = 'saving_goals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(120), nullable=False, unique=True)
    target_amount = db.Column(db.Float, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    current_amount = db.Column(db.Float, nullable=False, default=1.0)
    created_at = db.Column(db.DateTime, default=dt.now())

    users = db.relationship("Users", foreign_keys=[user_id], backref=db.backref('saving_goals', lazy=True, cascade='all, delete-orphan'))
