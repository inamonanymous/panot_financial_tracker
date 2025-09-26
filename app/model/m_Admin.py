from app.ext import db, dt

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=dt.now())

    users = db.relationship("Users", foreign_keys=[user_id], backref=db.backref('admin', lazy=True, cascade='all, delete-orphan'))