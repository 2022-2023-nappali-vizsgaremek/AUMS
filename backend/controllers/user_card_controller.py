# Local imports
from utils.log import log
from utils.close import exit_app
import services.user_card_service as service

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
    def post(self, card_id:int, user_id:int) -> dict:
        """
        Connect card to user

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Connecting card to user")
        return service.connect_card_to_user(card_id, user_id)
    
    @doc(description="Get all user cards", tags=["UserCard"])
    def get(self) -> dict:
        """
        Get all user cards

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Getting all user cards")
        return service.get_all_user_cards()