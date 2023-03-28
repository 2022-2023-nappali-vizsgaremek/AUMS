from utils.log import log
from utils.close import exit_app
import services.card_service as service

try:
    from flask_apispec import MethodResource
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

parser = reqparse.RequestParser()
parser.add_argument('card_number', type=str, location='form')

class Cards(MethodResource, Resource):
    def get(self):
        log.info("Getting all cards")
        return service.get_all_cards()

    def post(self):
        args = parser.parse_args()
        log.info("Creating a new card")
        return service.create_new_card(args)

    def patch(self, card_id):
        args = parser.parse_args()
        log.info("Updating a card")
        return service.update_card(args, card_id)

    def delete(self, card_id):
        log.info("Deleting a card")
        return service.delete_card(card_id)
