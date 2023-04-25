from utils.log import log
from utils.close import exit_app
import services.card_service as service

try:
    from flask_apispec import MethodResource
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

active_parser = reqparse.RequestParser()
active_parser.add_argument('card_number', type=str)

unknown_parser = reqparse.RequestParser()
unknown_parser.add_argument('uk_card_number', type=str)

parser_activate = reqparse.RequestParser()
parser_activate.add_argument('uk_card_id', type=int)

validation_parser = reqparse.RequestParser()
validation_parser.add_argument('card_number', type=str)


class ActivateCard(MethodResource, Resource):
    def post(self, uk_card_id):
        log.info("Activating a card")
        return service.activate_card(uk_card_id)
    
class CardValidation(MethodResource, Resource):
    def post(self):
        args = validation_parser.parse_args()
        log.info("Registering a card")
        return service.validate_card(args)

class ActiveCards(MethodResource, Resource):
    def get(self, card_id=None):
        if card_id:
            log.info(f"Getting active card with ID: {card_id}")
            return service.get_card(card_id)
        else:
            log.info("Getting all active cards")
            return service.get_all_cards()

    def patch(self, card_id):
        args = active_parser.parse_args()
        log.info("Updating an active card")
        return service.update_card(args, card_id)

    def delete(self, card_id):
        log.info("Deleting an active card")
        return service.delete_card(card_id)
    
class UnknownCards(MethodResource, Resource):
    def get(self, card_id=None):
        if card_id:
            log.info(f"Getting unknown card with ID: {card_id}")
            return service.get_unknown_card(card_id)
        else:
            log.info("Getting all unknown cards")
            return service.get_unknown_cards()

    def delete(self, uk_card_id):
        log.info("Deleting an unknown card")
        return service.delete_unknown_card(uk_card_id)