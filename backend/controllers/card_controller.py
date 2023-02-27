from flask import request
from flask_apispec import MethodResource
from flask_restful import Resource
from models.card import Card, db

class Cards(MethodResource, Resource):
    def get(self):
        cards = Card.query.all()
        if not cards:
            return {'message': 'No cards found'}, 404
        return [card.serialize() for card in cards], 200
    
    def post(self):
        card_number = request.form.get('card_number')
        if not card_number:
            return {'message': 'Card number is required'}, 400
        card = Card(card_number=card_number)
        db.session.add(card)
        try:
            db.session.commit()
        except:
            return {'message': 'This card already exists in the database'}, 409
        return card.serialize(), 200
    
    def patch(self, card_id):
        card_number = request.form.get('card_number')
        card = Card.query.filter_by(id=card_id).first()
        if not card:
            return {'message': 'Card not found'}, 404
        card.card_number = card_number
        try:
            db.session.commit()
        except:
            return {'message': 'Card number already exists in the database'}, 409
        return card.serialize(), 200
    
    def delete(self, card_id):
        card = Card.query.filter_by(id=card_id).first()
        if not card:
            return {'message': 'Card not found'}, 404
        db.session.delete(card)
        db.session.commit()
        return {'message': 'Card has been deleted'}, 200