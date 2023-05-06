# Local imports
import config
from models import db
from utils.close import exit_app

try:
    # External imports
    import pytest
    from flask import Flask
    from sqlalchemy_utils import database_exists
    from sqlalchemy_utils import create_database
except ImportError as import_error: exit_app(f"Module not found: {import_error}")

@pytest.fixture(scope="function")
def test_client():
    """
    Test client creation with test configuration

    Yields:
        FlaskClient: A test client
    """

    app = Flask(__name__)
    app.config.from_object(config.Test)
    from models import card, role, schedule, user, user_card, user_role

    db.init_app(app)

    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client
    ctx.pop()

@pytest.fixture(scope="function")
def init_database(test_client):
    """
    Initialize database with test configuration

    Args:
        test_client (Flask): A test client
    """

    with test_client.application.app_context():
        engine = db.engine.url

        if not database_exists(engine):
            create_database(engine)

        db.create_all()
        add_roles_to_db()
        db.session.commit()

        yield
        db.drop_all()

def add_roles_to_db():
    """
    Add roles to database
    """

    from models.role import Role

    role1 = Role(id=1, name="Admin", level=5)
    role2 = Role(id=2, name="User", level=1)

    db.session.add(role1)
    db.session.add(role2)

def connect_role_to_user(user_id: int, role_id: int):
    """
    Connect role to user

    Args:
        user_id (int): The id of the user
        role_id (int): The id of the role
    """

    from models.user_role import UserRole

    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.session.add(user_role)
    db.session.commit()

def test_app_config(test_client):
    """
    Test app configuration

    Args:
        test_client (Flask): A test client
    """

    expected_config = {
        test_client.application.config["TESTING"] == True,
        test_client.application.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
    }

    assert expected_config == {
        test_client.application.config["TESTING"] == True,
        test_client.application.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
    }

    expected_config = {
        test_client.application.config["TESTING"] == False,
        test_client.application.config["SQLALCHEMY_DATABASE_URI"] == "mysql://root:root@mysql_aums:3306/aums"
    }

    assert expected_config != {
        test_client.application.config["TESTING"] == True,
        test_client.application.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
    }

def test_database(test_client):
    """
    Test valid database creation

    Args:
        test_client (Flask): A test client
    """

    expected_tables = ["card", "role", "schedule", "user", "user_card", "user_role"]

    with test_client.application.app_context():
        actual_tables = sorted(str(t) for t in db.metadata.sorted_tables)
        assert actual_tables == expected_tables

def test_wrong_database(test_client):
    """
    Test invalid database creation

    Args:
        test_client (Flask): A test client
    """

    expected_tables = ["card", "role", "user", "user_card"]

    with test_client.application.app_context():
        actual_tables = sorted(str(t) for t in db.metadata.sorted_tables)
        assert actual_tables != expected_tables