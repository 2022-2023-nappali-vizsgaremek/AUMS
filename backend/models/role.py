from models import db

class Role(db.Model):
    id = db.Column(
        db.SmallInteger,
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=True)

    name = db.Column(db.String(50), unique=True, nullable=False)
    level = db.Column(db.SmallInteger, unique=True, nullable=False)