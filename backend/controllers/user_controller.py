# Local imports
from utils.log import log
from utils.close import exit_app
import services.user_service as service
from services.index_service import auth_required

try:
    # External imports
    from flask_apispec import MethodResource, doc
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

parser = reqparse.RequestParser()
parser.add_argument("address", type=str)
parser.add_argument("username", type=str)
parser.add_argument("password", type=str)
parser.add_argument("last_name", type=str)
parser.add_argument("first_name", type=str)
parser.add_argument("birth_date", type=str)
parser.add_argument("phone_number", type=str)
parser.add_argument("company_email", type=str)
parser.add_argument("personal_email", type=str)

class Register(MethodResource, Resource):
    @doc(description="Register a new user", tags=["User"])
    @auth_required
    def post(self) -> dict:
        """
        Registers a new user

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        args = parser.parse_args()
        log.info("Registering new user")
        return service.register_new_user(args)

class Login(MethodResource, Resource):
    @doc(description="Login a user", tags=["User"])
    def post(self) -> dict:
        """
        Logs in a user

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        args = parser.parse_args()
        log.info("Logging in user")
        return service.login_user(args)