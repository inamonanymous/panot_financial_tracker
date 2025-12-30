from app.ext import db, dt

class Expenses(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
    payee = db.Column(db.String(32), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expense_date = db.Column(db.DateTime, default=dt.now())
    payment_method = db.Column(db.Enum("cash", "gcash", "bank", "card", "other"), nullable=True, default="cash")
    remarks = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=dt.now())

    users = db.relationship("Users", foreign_keys=[user_id], backref=db.backref('expenses', lazy=True, cascade='all, delete-orphan'))
    categories = db.relationship("Categories", foreign_keys=[category_id], backref=db.backref('expenses', lazy=True, cascade='all, delete-orphan'))                               