# Local imports
from models.user import User
from utils.close import exit_app

# External imports
try: import pytest
except ImportError as import_error: exit_app(f"Module not found: {import_error}")

@pytest.fixture(scope="module")
def valid_user():
    """
    Creates a valid user object for testing

    Returns:
        User: A valid user object
    """

    user = User(
        first_name="John",
        last_name="Doe",
        birth_date="1990-01-01",
        phone_number="123456789",
        address="1234 Main St",
        company_email="john.doe@proj-aums.hu",
        personal_email="john.john@gmail.com",
        username="johnny",
        password="password")

    return user

def test_user_creation(valid_user):
    """
    Test user creation with valid data

    Args:
        valid_user (User): A valid user object
    """

    assert valid_user.first_name == "John"
    assert valid_user.last_name == "Doe"
    assert valid_user.birth_date == "1990-01-01"
    assert valid_user.phone_number == "123456789"
    assert valid_user.address == "1234 Main St"
    assert valid_user.company_email == "john.doe@proj-aums.hu"
    assert valid_user.personal_email == "john.john@gmail.com"
    assert valid_user.username == "johnny"
    assert valid_user.password == "password"