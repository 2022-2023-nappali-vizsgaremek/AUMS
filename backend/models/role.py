from models import db

class Role(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=True)

    name = db.Column(
        db.String(50),
        unique=True,
        nullable=False)

    level = db.Column(
        db.Integer,
        unique=True,
        nullable=False)