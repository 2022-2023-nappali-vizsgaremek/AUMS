from models.card import Card, db
from models.unknown_card import UnknownCard

def get_all_cards():
    cards = Card.query.all()

    if not cards:
        return {
            'status': 'failed',
            'message': 'No cards found'}, 404
    return [card.serialize() for card in cards], 200

def get_unknown_cards():
    uk_cards = UnknownCard.query.all()

    if not uk_cards:
        return {
            'status': 'failed',
            'message': 'No unknown cards found'}, 404
    return [uk_card.serialize() for uk_card in uk_cards], 200

def get_card(card_id):
    card = Card.query.filter_by(id=card_id).first()

    if not card:
        return {
            'status': 'failed',
            'message': 'Card not found'}, 404
    return card.serialize(), 200

def get_unknown_card(uk_card_id):
    uk_card = UnknownCard.query.filter_by(id=uk_card_id).first()

    if not uk_card:
        return {
            'status': 'failed',
            'message': 'Unknown card not found'}, 404
    return uk_card.serialize(), 200

def create_new_card(args):
    card_number = args['card_number']

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
        'message': 'Card has been added to the database',
        'data': card.card_number}, 201
    
def create_new_unknown_card(args):
    uk_card_number = args['uk_card_number']

    if not uk_card_number:
        return {
            'status': 'failed',
            'message': 'Card number is required'}, 400
    uk_card = UnknownCard.query.filter_by(uk_card_number=uk_card_number).first()

    if uk_card:
        return {
            'status': 'failed',
            'message': 'Card number already exists in the database'}, 409
    uk_card = UnknownCard(uk_card_number=uk_card_number)
    db.session.add(uk_card)
    db.session.commit()
    return {
        'status': 'success',
        'message': 'Card has been added to the database',
        'data': uk_card.uk_card_number}, 201

def update_card(args, card_id):
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
    
    return {
        'status': 'success',
        'message': 'This card has been updated'}, 200
    
def update_unknown_card(args, uk_card_id):
    uk_card_number = args['uk_card_number']
    if not uk_card_number:
        return {
            'status': 'failed',
            'message': 'Card number is required'}, 400
    uk_card = UnknownCard.query.filter_by(id=uk_card_id).first()

    if not uk_card:
        return {
            'status': 'failed',
            'message': 'Card not found'}, 404
    uk_card.uk_card_number = uk_card_number

    try:
        db.session.commit()
    except:
        return {
            'status': 'failed',
            'message': 'Card number already exists in the database'}, 409
    
    return {
        'status': 'success',
        'message': 'This card has been updated'}, 200

def delete_card(card_id):
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
    
def delete_unknown_card(uk_card_id):
    uk_card = UnknownCard.query.filter_by(id=uk_card_id).first()
    
    if not uk_card:
        return {
            'status': 'failed',
            'message': 'Card not found'}, 404
    db.session.delete(uk_card)
        
    try:
        db.session.commit()
    except:
        return {
            'status': 'failed',
            'message': 'Internal server error'}, 500

    return {
        'status': 'success',
        'message': 'Card has been deleted'}, 200