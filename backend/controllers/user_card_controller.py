# Local imports
from utils.log import log
from utils.close import exit_app
import services.user_card_service as service
from services.index_service import auth_required

try:
    # External imports
    from flask_apispec import MethodResource, doc
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

parser = reqparse.RequestParser()
parser.add_argument("card_id", type=int)
parser.add_argument("user_id", type=int)

class UserCard(MethodResource, Resource):
    @doc(description="Connect card to user", tags=["UserCard"])
    @auth_required
    def post(self) -> dict:
        """
        Connect card to user

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        args = parser.parse_args()
        card_id = args["card_id"]
        user_id = args["user_id"]
        log.info("Connecting card to user")
        return service.connect_card_to_user(card_id, user_id)

    @doc(description="Get all user cards", tags=["UserCard"])
    @auth_required
    def get(self) -> dict:
        """
        Get all user cards

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Getting all user cards")
        return service.get_all_user_cards()

    @doc(description="Delete user-card connection", tags=["UserCard"])
    @auth_required
    def delete(self, id: int) -> dict:
        """
        Delete user-card connection

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Deleting user-card connection")
        return service.delete_user_card(id)

class Users(MethodResource, Resource):
    @doc(description="Get users", tags=["Users"])
    @auth_required
    def get(self) -> dict:
        """
        Get users

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Getting users")
        return service.get_users()