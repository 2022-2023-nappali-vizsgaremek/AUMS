# Local imports
from datetime import date
from tests.test_config import test_client, init_database
from services.user_service import register_new_user, login_user

def register_user_args() -> dict:
    """
    Creates an argument dictionary for testing user registration

    Returns:
        dict: A dictionary containing the arguments for testing user registration
    """

    args = {
        "first_name": "Test",
        "last_name": "User",
        "birth_date": date(1999, 1, 1),
        "phone_number": "12345678",
        "address": "123 Test St.",
        "personal_email": "user.email@gmail.com",
        "username": "test_user",
        "password": "password"
    }

    return args

def login_user_args() -> dict:
    """
    Creates an argument dictionary for testing user login

    Returns:
        dict: A dictionary containing the arguments for testing user login
    """

    args = {
        "company_email": "test.user@proj-aums.hu",
        "password": "password"
    }

    return args

def test_register_user(test_client, init_database) -> None:
    """
    Test user registration with valid data

    Args:
        test_client (FlaskClient): A test client
        init_database (Database): A database instance
    """

    with test_client.application.app_context():
        response, status_code = register_new_user(register_user_args())

        assert status_code == 201
        assert response["status"] == "success"
        assert response["message"] == "User successfully registered"

def test_register_user_wrong_fields(test_client, init_database) -> None:
    """
    Test user registration with wrong fields

    Args:
        test_client (FlaskClient): A test client
        init_database (Database): A database instance
    """

    modified_args = register_user_args()
    modified_args["username"] = ""

    response, status_code = register_new_user(modified_args)

    assert status_code == 400
    assert response["status"] == "failed"
    assert response["message"] == "All fields are required"

def test_login_user(test_client, init_database) -> None:
    """
    Test user login with valid data

    Args:
        test_client (FlaskClient): A test client
        init_database (Database): A database instance
    """

    with test_client.application.app_context():
        register_new_user(register_user_args())
        response, status_code = login_user(login_user_args())

        assert status_code == 200
        assert response["status"] == "success"
        assert response["message"] == "User successfully logged in"

def test_login_user_invalid_password(test_client, init_database) -> None:
    """
    Test user login with invalid password

    Args:
        test_client (FlaskClient): A test client
        init_database (Database): A database instance
    """

    with test_client.application.app_context():
        register_new_user(register_user_args())

        modified_args = login_user_args()
        modified_args["password"] = "wrong_password"
        response, status_code = login_user(modified_args)

        assert status_code == 401
        assert response["status"] == "failed"
        assert response["message"] == "Invalid company email or password"

def test_login_user_invalid_company_email(test_client, init_database) -> None:
    """
    Test user login with invalid company email

    Args:
        test_client (FlaskClient): A test client
        init_database (Database): A database instance
    """

    with test_client.application.app_context():
        register_new_user(register_user_args())

        modified_args = login_user_args()
        modified_args["company_email"] = "shady.person@injection.com"
        response, status_code = login_user(modified_args)

        assert status_code == 401
        assert response["status"] == "failed"
        assert response["message"] == "Invalid company email or password"