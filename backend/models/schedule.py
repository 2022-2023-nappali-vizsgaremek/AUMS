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
        db.ForeignKey('user.id'),
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

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start': self.enter_date,
            'end': self.leave_date}