import pytest
from models import db
from flask import Flask
from config import TestingConfig
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture(scope='module')
def test_client():
    app = Flask(__name__)
    app.config.from_object(TestingConfig)

    from models import card, role, schedule, user, user_card, user_role

    db.init_app(app)

    with app.app_context():
        db.create_all()
        testing_client = app.test_client()
        yield testing_client
        db.session.remove()
        db.drop_all()

def test_app_config(test_client):
    assert test_client.application.config['TESTING'] == True
    assert test_client.application.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'

def test_database(test_client):
    expected_tables = ['card', 'role', 'schedule', 'user', 'user_card', 'user_role']

    with test_client.application.app_context():
        actual_tables = sorted(str(t) for t in db.metadata.sorted_tables)
        assert actual_tables == expected_tables