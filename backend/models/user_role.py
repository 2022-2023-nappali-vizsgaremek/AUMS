from models import db

class UserRole(db.Model):
    user_id = db.Column(db.SmallInteger,
        db.ForeignKey('user.id'),
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=False)
    
    role_id = db.Column(db.SmallInteger,
        db.ForeignKey('role.id'),
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=False)