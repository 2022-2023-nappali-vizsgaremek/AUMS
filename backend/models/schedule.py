from models import db

class Schedule(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=False,
        nullable=False,
        primary_key=False,
        autoincrement=False)

    enter_date = db.Column(
        db.Date,
        unique=False,
        nullable=False)

    leave_date = db.Column(
        db.Date,
        unique=False,
        nullable=True)