from models import db

class UnknownCard(db.Model):
    id = db.Column(
        db.SmallInteger,
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=True)

    uk_card_number = db.Column(
        db.String(100),
        unique=True,
        nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "card_number": self.uk_card_number}