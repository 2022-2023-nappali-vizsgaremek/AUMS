# Local imports
from utils.log import log
from utils.close import exit_app
import services.card_service as service

try:
    # External imports
    from flask_apispec import MethodResource, doc
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

active_parser = reqparse.RequestParser()
active_parser.add_argument("card_number", type=str)

unknown_parser = reqparse.RequestParser()
unknown_parser.add_argument("uk_card_number", type=str)

parser_activate = reqparse.RequestParser()
parser_activate.add_argument("uk_card_id", type=int)

validation_parser = reqparse.RequestParser()
validation_parser.add_argument("card_number", type=str)

class ActivateCard(MethodResource, Resource):
    @doc(description="Activate a card", tags=["Card"])
    def post(self, uk_card_id: int) -> dict:
        """
        Activate a card

        Args:
            uk_card_id (int): The id of the card

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Activating a card")
        return service.activate_card(uk_card_id)

class CardValidation(MethodResource, Resource):
    @doc(description="Validate a card", tags=["Card"])
    def post(self, card_number: str) -> dict:
        """
        Validate a card

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Registering a card")
        return service.validate_card(card_number)

class ActiveCards(MethodResource, Resource):
    @doc(description="Get all active cards", tags=["Card"])
    def get(self) -> dict:
        """
        Get all active cards

        Args:
            card_id (int, optional): The id of the card. Defaults to None.

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Getting all active cards")
        return service.get_all_cards()

class ActiveCardById(MethodResource, Resource):
    @doc(description="Get an active card by ID", tags=["Card"])
    def get(self, card_id=None) -> dict:
        """
        Get all active cards

        Args:
            card_id (int, optional): The id of the card. Defaults to None.

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info(f"Getting active card with ID: {card_id}")
        return service.get_card(card_id)

    @doc(description="Update an active card", tags=["Card"])
    def patch(self, card_id:int) -> dict:
        """
        Update an active card

        Args:
            card_id (int): The id of the card

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        args = active_parser.parse_args()
        log.info("Updating an active card")
        return service.update_card(args, card_id)

    @doc(description="Delete an active card", tags=["Card"])
    def delete(self, card_id:int) -> dict:
        """
        Delete an active card

        Args:
            card_id (int): The id of the card

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Deleting an active card")
        return service.delete_card(card_id)

class UnknownCards(MethodResource, Resource):
    @doc(description="Get all unknown cards", tags=["Card"])
    def get(self, uk_card_id=None) -> dict:
        """
        Get an unknown card or all unknown cards

        Args:
            card_id (int, optional): The id of the card. Defaults to None.

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Getting all unknown cards")
        return service.get_unknown_cards()

class UnknownCardById(MethodResource, Resource):
    @doc(description="Get an unknown card by ID", tags=["Card"])
    def get(self, uk_card_id=None) -> dict:
        """
        Get an unknown card or all unknown cards

        Args:
            card_id (int, optional): The id of the card. Defaults to None.

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info(f"Getting unknown card with ID: {uk_card_id}")
        return service.get_unknown_card(uk_card_id)

    @doc(description="Delete an unknown card", tags=["Card"])
    def delete(self, uk_card_id:int) -> dict:
        """
        Delete an unknown card

        Args:
            uk_card_id (int): The id of the card

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Deleting an unknown card")
        return service.delete_unknown_card(uk_card_id)