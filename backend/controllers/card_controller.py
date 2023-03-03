from flask_apispec import MethodResource
from flask_restful import Resource, reqparse
from models.card import Card, db

parser = reqparse.RequestParser()
parser.add_argument('card_number', type=str, location='form')

class Cards(MethodResource, Resource):
    def get(self):
        cards = Card.query.all()
        if not cards:
            return {
                'status': 'failed',
                'message': 'No cards found'}, 404
        return {
            'status': 'success',
            'data': [card.serialize() for card in cards]}, 200

    def post(self):
        args = parser.parse_args()
        card_number = args['card_number']
        print(card_number)
        if not card_number:
            return {
                'status': 'failed',
                'message': 'Card number is required'}, 400
        card = Card.query.filter_by(card_number=card_number).first()

        if card:
            return {
                'status': 'failed',
                'message': 'Card number already exists in the database'}, 409
        card = Card(card_number=card_number)
        db.session.add(card)
        db.session.commit()
        return {
            'status': 'success',
            'data': card.card_number}, 201

    def patch(self, card_id):
        args = parser.parse_args()
        card_number = args['card_number']
        if not card_number:
            return {
                'status': 'failed',
                'message': 'Card number is required'}, 400
        card = Card.query.filter_by(id=card_id).first()

        if not card:
            return {
                'status': 'failed',
                'message': 'Card not found'}, 404
        card.card_number = card_number

        try:
            db.session.commit()
        except:
            return {
                'status': 'failed',
                'message': 'Card number already exists in the database'}, 409
        return card.serialize(), 200

    def delete(self, card_id):
        card = Card.query.filter_by(id=card_id).first()

        if not card:
            return {
                'status': 'failed',
                'message': 'Card not found'}, 404
        db.session.delete(card)

        try:
            db.session.commit()
        except:
            return {
                'status': 'failed',
                'message': 'Internal server error'}, 500

        return {
            'status': 'success',
            'message': 'Card has been deleted'}, 200
