# Local imports
import random
from models import db
from datetime import date
from services.user_service import register_new_user, login_user
from tests.test_config import test_client, init_database, add_roles_to_db

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
        "role_level": random.choice([1, 5]),
        "phone_number": "12345678901",
        "personal_email": "john.doe@example.com",
    }

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

class TestRegisterUser:
    def test_register_user_success(self, test_client, init_database):
        """
        Test register user success

        Args:
            test_client (_type_): _description_
            init_database (_type_): _description_
        """

        with test_client.application.app_context():
            user_data = generate_valid_user_data()
            response, status_code = register_new_user(user_data)

            assert status_code == 201
            assert response["status"] == "success"
            assert response["message"] == "User successfully registered"

    def test_register_user_empty_field(self, test_client, init_database):
        """
        Test register user empty field

        Args:
            test_client (FlaskClient): The test client
            init_database (None): The database
        """

        with test_client.application.app_context():
            user_data = generate_valid_user_data()
            user_data["first_name"] = ""

            response, status_code = register_new_user(user_data)

            assert status_code == 400
            assert response["status"] == "failed"
            assert response["message"] == "One or more fields are empty"

    def test_register_user_invalid_email(self, test_client, init_database):
        """
        Test register user invalid email

        Args:
            test_client (FlaskClient): The test client
            init_database (None): The database
        """

        with test_client.application.app_context():
            user_data = generate_valid_user_data()
            user_data["personal_email"] = "invalid_email"

            response, status_code = register_new_user(user_data)

            assert status_code == 400
            assert response["status"] == "failed"
            assert response["message"] == "The personal email is invalid"

class TestLoginUser:
    def test_login_user_success(self, test_client, init_database) -> None:
        """
        Test login user success

        Args:
            test_client (FlaskClient): The test client
            init_database (None): The database
        """

        with test_client.application.app_context():
            user_data = generate_valid_user_data()
            _, _, password = register_new_user(user_data, return_password=True)

            fn = (user_data["first_name"]).lower()
            ln = (user_data["last_name"]).lower()

            company_email = fn + "." + ln + "@proj-aums.hu"
            login_args = {
                "company_email": company_email,
                "password": password
            }

            response, status_code = login_user(login_args)

            assert status_code == 200
            assert response["status"] == "success"
            assert response["message"] == "User successfully logged in"

    def test_login_user_invalid_password(self, test_client, init_database) -> None:
        """
        Test login user invalid password

        Args:
            test_client (FlaskClient): The test client
            init_database (None): The database
        """

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

    def test_login_user_invalid_company_email(self, test_client, init_database) -> None:
        """
        Test login user invalid company email

        Args:
            test_client (FlaskClient): The test client
            init_database (None): The database
        """

        with test_client.application.app_context():
            user_data = generate_valid_user_data()
            register_new_user(user_data)

            login_args = {
                "company_email": "shady.person@injection.com",
                "password": "password"
            }

            response, status_code = login_user(login_args)

            assert status_code == 401
            assert response["status"] == "failed"
            assert response["message"] == "Invalid company email or password"