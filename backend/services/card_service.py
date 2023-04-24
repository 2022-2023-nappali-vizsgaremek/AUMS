from models.card import Card, db
from models.unknown_card import UnknownCard

def get_all_cards():
    cards = Card.query.all()

    if not cards:
        return error_response('failed', 'No cards found', 404)
    return [card.serialize() for card in cards], 200

def get_unknown_cards():
    uk_cards = UnknownCard.query.all()

    if not uk_cards:
        return error_response('failed', 'No cards found', 404)
    return [uk_card.serialize() for uk_card in uk_cards], 200

def get_card(card_id):
    card = Card.query.filter_by(id=card_id).first()

    if not card:
        return error_response('failed', 'Card not found', 404)
    return card.serialize(), 200

def get_unknown_card(uk_card_id):
    uk_card = UnknownCard.query.filter_by(id=uk_card_id).first()

    if not uk_card:
        return error_response('failed', 'Card not found', 404)
    return uk_card.serialize(), 200

'''def create_new_card(args):
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
   ''' 
def create_new_unknown_card(args):
    uk_card_number = args['uk_card_number']

    if not uk_card_number:
        return error_response('failed', 'Card number is required', 400)
    uk_card = UnknownCard.query.filter_by(uk_card_number=uk_card_number).first()

    if uk_card:
        return error_response('failed', 'Card number already exists in the database', 409)
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
        return error_response('failed', 'Card number is required', 400)
    card = Card.query.filter_by(id=card_id).first()

    if not card:
        return error_response('failed', 'Card not found', 404)
    card.card_number = card_number

    try:
        db.session.commit()
    except:
        return error_response('failed', 'Card number already exists in the database', 409)
    
    return error_response('success', 'This card has been updated', 200)
    
def update_unknown_card(args, uk_card_id):
    uk_card_number = args['uk_card_number']
    if not uk_card_number:
        return error_response('failed', 'Card number is required', 400)
    uk_card = UnknownCard.query.filter_by(id=uk_card_id).first()

    if not uk_card:
        return error_response('failed', 'Card not found', 404)
    uk_card.uk_card_number = uk_card_number

    try:
        db.session.commit()
    except:
        return error_response('failed', 'Card number already exists in the database', 409)
    
    return error_response('success', 'This card has been updated', 200)

def delete_card(card_id):
    card = Card.query.filter_by(id=card_id).first()

    if not card:
        return error_response('failed', 'Card not found', 404)
    db.session.delete(card)

    try:
        db.session.commit()
    except:
        return error_response('failed', 'Internal server error', 500)

    return error_response('success', 'Card has been deleted', 200)
    
def delete_unknown_card(uk_card_id):
    uk_card = UnknownCard.query.filter_by(id=uk_card_id).first()
    
    if not uk_card:
        return error_response('failed', 'Card not found', 404)
    db.session.delete(uk_card)
        
    try:
        db.session.commit()
    except:
        return error_response('failed', 'Internal server error', 500)

    return error_response('success', 'Card has been deleted', 200)

def activate_card(uk_card_id):
    uk_card = UnknownCard.query.filter_by(id=uk_card_id).first()
    
    if not uk_card:
        return error_response('failed', 'Card not found', 404)
    new_card = Card(card_number=uk_card.uk_card_number)
    db.session.add(new_card)
    db.session.delete(uk_card)
        
    try:
        db.session.commit()
    except:
        return error_response('failed', 'Internal server error', 500)

    return error_response('success', 'Card has been activated', 200)

def error_response(status, message, status_code):
    return {'status': status, 'message': message}, status_code