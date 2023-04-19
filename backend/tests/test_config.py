import pytest
from models import db
from flask import Flask
from config import TestingConfig
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database

@pytest.fixture(scope='function')
def test_client():
    app = Flask(__name__)
    app.config.from_object(TestingConfig)

    from models import card, role, schedule, user, user_card, user_role
    db.init_app(app)
    
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()
    
@pytest.fixture(scope='function')
def init_database(test_client):
    with test_client.application.app_context():
        engine = db.engine.url

        if not database_exists(engine):
            create_database(engine)

        db.create_all()
        db.session.commit()

        yield

        db.drop_all()
    
def test_app_config(test_client):
    expected_config = {
        test_client.application.config['TESTING'] == True,
        test_client.application.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    }
    
    assert expected_config == {
        test_client.application.config['TESTING'] == True,
        test_client.application.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    }
    
def test_wrong_app_config(test_client):
    expected_config = {
        test_client.application.config['TESTING'] == False,
        test_client.application.config['SQLALCHEMY_DATABASE_URI'] == 'mysql://root:root@mysql_aums:3306/aums'
    }
    
    assert expected_config != {
        test_client.application.config['TESTING'] == True,
        test_client.application.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    }

def test_database(test_client):
    expected_tables = ['card', 'role', 'schedule', 'user', 'user_card', 'user_role']

    with test_client.application.app_context():
        actual_tables = sorted(str(t) for t in db.metadata.sorted_tables)
        assert actual_tables == expected_tables
        
def test_wrong_database(test_client):
    expected_tables = ['card', 'role', 'user', 'user_card']

    with test_client.application.app_context():
        actual_tables = sorted(str(t) for t in db.metadata.sorted_tables)
        assert actual_tables != expected_tables