from app.ext import db, dt

class Income(db.Model):
    __tablenam__ = 'income'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
    source = db.Column(db.String(55), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    received_date = db.Column(db.Date, default=dt.now().date)
    remarks = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=dt.now())

    users = db.relationship("Users", foreign_keys=[user_id], backref=db.backref('income', lazy=True, cascade='all, delete-orphan'))
    users = db.relationship("Categories", foreign_keys=[category_id], backref=db.backref('income', lazy=True, cascade='all, delete-orphan'))