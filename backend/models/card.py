from models import db

class Card(db.Model):
    id = db.Column(db.SmallInteger,
                   unique=True,
                   nullable=False,
                   primary_key=True,
                   autoincrement=True)
    
    card_number = db.Column(db.String(100), unique=True, nullable=False)