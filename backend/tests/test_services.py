# Local imports
import random
from datetime import date
from tests.test_config import test_client, init_database
from services.user_service import register_new_user, login_user

def generate_valid_user_data():
    """
    Generate valid user data

    Returns:
        dict: A dictionary containing valid user data
    """

    return {
        "address": "123 Example St.",
        "last_name": "Doe",
        "first_name": "John",
        "birth_date": date(1990, 1, 1),
        "role_level": random.randint(1, 5),
        "phone_number": "12345678901",
        "personal_email": "john.doe@example.com",
    }

def test_register_user_success(test_client, init_database):
    with test_client.application.app_context():
        user_data = generate_valid_user_data()
        response, status_code = register_new_user(user_data)

        assert status_code == 201
        assert response["status"] == "success"
        assert response["message"] == "User successfully registered"

def test_register_user_empty_field(test_client, init_database):
    with test_client.application.app_context():
        user_data = generate_valid_user_data()
        user_data["first_name"] = ""

        response, status_code = register_new_user(user_data)

        assert status_code == 400
        assert response["status"] == "failed"
        assert response["message"] == "One or more fields are empty"

def test_register_user_invalid_email(test_client, init_database):
    with test_client.application.app_context():
        user_data = generate_valid_user_data()
        user_data["personal_email"] = "invalid_email"

        response, status_code = register_new_user(user_data)

        assert status_code == 400
        assert response["status"] == "failed"
        assert response["message"] == "The personal email is invalid"


def test_login_user_success(test_client, init_database) -> None:
    with test_client.application.app_context():
        user_data = generate_valid_user_data()
        password = "password"  # The password we want to use for testing
        register_new_user(user_data, password)

        login_args = {
            "company_email": user_data["personal_email"],
            "password": password
        }

        print(login_args)

        response, status_code = login_user(login_args)

        assert status_code == 200
        assert response["status"] == "success"
        assert response["message"] == "User successfully logged in"

def test_login_user_invalid_password(test_client, init_database) -> None:
    with test_client.application.app_context():
        user_data = generate_valid_user_data()
        register_new_user(user_data)

        login_args = {
            "company_email": user_data["personal_email"],
            "password": "wrong_password"
        }

        response, status_code = login_user(login_args)

        assert status_code == 401
        assert response["status"] == "failed"
        assert response["message"] == "Invalid company email or password"

def test_login_user_invalid_company_email(test_client, init_database) -> None:
    with test_client.application.app_context():
        user_data = generate_valid_user_data()
        print(user_data)
        register_new_user(user_data)

        login_args = {
            "company_email": "shady.person@injection.com",
            "password": "password"
        }

        response, status_code = login_user(login_args)

        assert status_code == 401
        assert response["status"] == "failed"
        assert response["message"] == "Invalid company email or password"