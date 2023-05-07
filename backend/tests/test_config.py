# Local imports
import config
from models import db
from models.role import Role
from models.user import User
from models.card import Card
from datetime import datetime
from utils.close import exit_app
from models.schedule import Schedule
from models.user_card import UserCard
from models.user_role import UserRole

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

    role1 = Role(name="Base User", level=1)
    role2 = Role(name="Authenticated User", level=2)
    #role3 = Role(id=3, name="Secretary", level=3)
    #role4 = Role(id=4, name="Manager", level=4)
    role5 = Role(name="Admin", level=5)

    db.session.add(role1)
    db.session.add(role2)
    #db.session.add(role3)
    #db.session.add(role4)
    db.session.add(role5)

class TestConfig:
    def test_app_config(self, test_client):
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

    def test_database(self, test_client):
        """
        Test valid database creation

        Args:
            test_client (Flask): A test client
        """

        expected_tables = ["card", "role", "schedule", "user", "user_card", "user_role"]

        with test_client.application.app_context():
            actual_tables = sorted(str(t) for t in db.metadata.sorted_tables)
            assert actual_tables == expected_tables

    def test_wrong_database(self, test_client):
        """
        Test invalid database creation

        Args:
            test_client (Flask): A test client
        """

        expected_tables = ["card", "role", "user", "user_card"]

        with test_client.application.app_context():
            actual_tables = sorted(str(t) for t in db.metadata.sorted_tables)
            assert actual_tables != expected_tables

class TestRole:
    def test_add_role(self, test_client, init_database):
        """
        Test role creation

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            role = Role(name="Super Admin", level=6)
            db.session.add(role)
            db.session.commit()

            assert role.id is not None

    def test_update_role(self, test_client, init_database):
        """
        Test role updation

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            initial_role_count = Role.query.count()
            self.test_add_role(test_client, init_database)

            roles = Role.query.all()
            assert len(roles) == initial_role_count + 1

            role = roles[-1]
            role.name = "Super Duper Admin"
            db.session.commit()

            updated_role = Role.query.get(role.id)
            assert updated_role.name == "Super Duper Admin"

    def test_delete_role(self, test_client, init_database):
        """
        Test role deletion

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            initial_role_count = Role.query.count()
            self.test_add_role(test_client, init_database)

            roles = Role.query.all()
            assert len(roles) == initial_role_count + 1

            role = roles[-1]
            db.session.delete(role)
            db.session.commit()

            deleted_role = Role.query.get(role.id)
            assert deleted_role is None

class TestCard:
    def test_add_card(self, test_client, init_database):
        """
        Test card creation

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            card = Card(card_number="1234567890")
            db.session.add(card)
            db.session.commit()

            assert card.id is not None

    def test_update_card(self, test_client, init_database):
        """
        Test card updation

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            self.test_add_card(test_client, init_database)
            cards = Card.query.all()
            assert len(cards) == 1

            card = cards[0]
            card.card_number = "0987654321"
            db.session.commit()

            updated_card = Card.query.get(card.id)
            assert updated_card.card_number == "0987654321"

    def test_delete_card(self, test_client, init_database):
        """
        Test card deletion

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            self.test_add_card(test_client, init_database)
            cards = Card.query.all()
            assert len(cards) == 1

            card = cards[0]
            db.session.delete(card)
            db.session.commit()

            deleted_card = Card.query.get(card.id)
            assert deleted_card is None

class TestUserRole:
    def test_add_user_role(self, test_client, init_database):
        """
        Test user role creation
        
        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            user_role = UserRole(id=1, user_id=1, role_id=1)
            db.session.add(user_role)
            db.session.commit()

            assert user_role.id is not None

    def test_update_user_role(self, test_client, init_database):
        """
        Test user role updation

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            self.test_add_user_role(test_client, init_database)
            user_roles = UserRole.query.all()
            assert len(user_roles) == 1

            user_role = user_roles[0]
            user_role.role_id = 2
            db.session.commit()

            updated_user_role = UserRole.query.get(user_role.id)
            assert updated_user_role.role_id == 2

    def test_delete_user_role(self, test_client, init_database):
        """
        Test user role deletion

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            self.test_add_user_role(test_client, init_database)
            user_roles = UserRole.query.all()
            assert len(user_roles) == 1

            user_role = user_roles[0]
            db.session.delete(user_role)
            db.session.commit()

            deleted_user_role = UserRole.query.get(user_role.id)
            assert deleted_user_role is None

class TestUserCard:
    def test_add_user_card(self, test_client, init_database):
        """
        Test user card creation

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            user_card = UserCard(user_id=1, card_id=1)
            db.session.add(user_card)
            db.session.commit()

            assert user_card.id is not None

    def test_update_user_card(self, test_client, init_database):
        """
        Test user card updation

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            self.test_add_user_card(test_client, init_database)
            user_cards = UserCard.query.all()

            assert len(user_cards) == 1

            user_card = user_cards[0]
            user_card.card_id = 2
            db.session.commit()

            updated_user_card = UserCard.query.get(user_card.id)
            assert updated_user_card.card_id == 2

    def test_delete_user_card(self, test_client, init_database):
        """
        Test user card deletion

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            self.test_add_user_card(test_client, init_database)
            user_cards = UserCard.query.all()
            assert len(user_cards) == 1

            user_card = user_cards[0]
            db.session.delete(user_card)
            db.session.commit()

            deleted_user_card = UserCard.query.get(user_card.id)
            assert deleted_user_card is None

class TestSchedule:
    def test_add_schedule(self, test_client, init_database):
        """
        Test schedule creation

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            enter_date = datetime(2020, 1, 1, 8, 0, 0)
            leave_date = datetime(2020, 1, 1, 16, 0, 0)
            schedule = Schedule(user_id=1, enter_date=enter_date, leave_date=leave_date)
            db.session.add(schedule)
            db.session.commit()

            assert schedule.id is not None

    def test_add_schedule_enter_date(self, test_client, init_database):
        """
        Test schedule creation

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            enter_date = datetime(2020, 1, 1, 8, 0, 0)
            leave_date = None

            schedule = Schedule(user_id=1, enter_date=enter_date, leave_date=leave_date)
            db.session.add(schedule)
            db.session.commit()

            assert schedule.enter_date == enter_date

    def test_delete_schedule(self, test_client, init_database):
        """
        Test schedule deletion

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            self.test_add_schedule(test_client, init_database)
            schedules = Schedule.query.all()
            assert len(schedules) == 1

            schedule = schedules[0]
            db.session.delete(schedule)
            db.session.commit()

            deleted_schedule = Schedule.query.get(schedule.id)
            assert deleted_schedule is None

class TestUserRoleConnection:
    def test_connect_role_to_user(self, test_client, init_database):
        """
        Test user role connection

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            user_role = UserRole(user_id=1, role_id=1)
            db.session.add(user_role)
            db.session.commit()

            assert user_role.id is not None

    def test_disconnect_role_from_user(self, test_client, init_database):
        """
        Test user role disconnection

        Args:
            test_client (Flask): A test client
            init_database (function): Initialize database
        """

        with test_client.application.app_context():
            self.test_connect_role_to_user(test_client, init_database)
            user_roles = UserRole.query.all()
            assert len(user_roles) == 1

            user_role = user_roles[0]
            db.session.delete(user_role)
            db.session.commit()

            deleted_user_role = UserRole.query.get(user_role.id)
            assert deleted_user_role is None