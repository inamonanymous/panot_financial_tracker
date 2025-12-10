from app.ext import db, dt

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    type = db.Column(db.Enum("income", "expense"), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=dt.now())

    users = db.relationship("Users", foreign_keys=[user_id], backref=db.backref('categories', lazy=True, cascade='all, delete-orphan'))

