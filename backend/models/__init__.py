from create import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

db = SQLAlchemy()

with app.app_context():
    db.init_app(app)

    if not database_exists(db.engine.url):
        create_database(db.engine.url)

    db.create_all()