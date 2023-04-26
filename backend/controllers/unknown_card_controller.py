from utils.log import log
from utils.close import exit_app
import services.card_service as service

try:
    from flask_apispec import MethodResource
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

parser = reqparse.RequestParser()
parser.add_argument("uk_card_number", type=str)

class Cards(MethodResource, Resource):
    def get(self, card_id=None) -> dict:
        """
        Get a card or all cards

        Args:
            card_id (int, optional): The id of the card. Defaults to None.

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        if card_id:
            log.info(f"Getting card with ID: {card_id}")
            return service.get_unknown_card(card_id)
        else:
            log.info("Getting all cards")
            return service.get_unknown_cards()

    def post(self) -> dict:
        """
        Create a new card

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        args = parser.parse_args()
        log.info("Creating a new card")
        return service.create_new_unknown_card(args)

    def patch(self, card_id) -> dict:
        """
        Update a card

        Args:
            card_id (int): The id of the card

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        args = parser.parse_args()
        log.info("Updating a card")
        return service.update_unknown_card(args, card_id)

    def delete(self, card_id) -> dict:
        """
        Delete a card

        Args:
            card_id (int): The id of the card

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Deleting a card")
        return service.delete_unknown_card(card_id)