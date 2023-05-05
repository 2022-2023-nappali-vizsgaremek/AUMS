from models import db

class User(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(100),
        unique=False,
        nullable=False)

    last_name = db.Column(
        db.String(100),
        unique=False,
        nullable=False)

    birth_date = db.Column(
        db.Date,
        unique=False,
        nullable=False)

    phone_number = db.Column(
        db.String(50),
        unique=False,
        nullable=True)

    address = db.Column(
        db.String(100),
        unique=False,
        nullable=True)

    company_email = db.Column(
        db.String(50),
        unique=True,
        nullable=False)

    personal_email = db.Column(
        db.String(50),
        unique=True,
        nullable=False)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False)

    password = db.Column(
        db.String(255),
        unique=False,
        nullable=False)

    access_token = db.Column(
        db.String(255),
        unique=True,
        nullable=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.first_name + " " + self.last_name,
            "company_email": self.company_email,
            "personal_email": self.personal_email,
            "phone": self.phone_number,
            "address": self.address,
        }
