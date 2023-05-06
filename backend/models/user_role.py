from models import db

class UserRole(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=True,
        nullable=False,
        primary_key=False,
        autoincrement=False)

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("role.id"),
        unique=False,
        nullable=False,
        primary_key=False,
        autoincrement=False)