from models.card import Card, db
from models.unknown_card import UnknownCard

def get_all_cards():
    return _get_all(Card)

def get_unknown_cards():
    return _get_all(UnknownCard)

def get_card_by_number(card_number):
    return _get_by_attribute(Card, 'card_number', card_number)

def get_card(card_id):
    return _get_by_attribute(Card, 'id', card_id)

def get_unknown_card(uk_card_id):
    return _get_by_attribute(UnknownCard, 'id', uk_card_id)

def create_new_unknown_card(args):
    uk_card_number = args['uk_card_number']

    if not uk_card_number:
        return _error_response('failed', 'Card number is required', 400)

    card = _get_by_attribute(Card, 'card_number', uk_card_number, serialize=False)

    if card:
        return _error_response('failed', 'Card number already exists in the active cards', 409)

    uk_card = _get_by_attribute(UnknownCard, 'uk_card_number', uk_card_number, serialize=False)

    if uk_card:
        return _error_response('failed', 'Card number already exists in the unknown cards', 409)

    uk_card = UnknownCard(uk_card_number=uk_card_number)
    db.session.add(uk_card)
    db.session.commit()

    return _error_response('success', 'Card has been added to the database', 201)

def update_card(args, card_id):
    return _update_card(Card, 'id', card_id, args)

def update_unknown_card(args, uk_card_id):
    return _update_card(UnknownCard, 'id', uk_card_id, args)

def delete_card(card_id):
    return _delete_card(Card, 'id', card_id)

def delete_unknown_card(uk_card_id):
    return _delete_card(UnknownCard, 'id', uk_card_id)

def activate_card(uk_card_id):
    uk_card = _get_by_attribute(UnknownCard, 'id', uk_card_id, serialize=False)
    if not uk_card:
        return _error_response('failed', 'Card not found', 404)

    new_card = Card(card_number=uk_card.uk_card_number)
    db.session.add(new_card)
    db.session.delete(uk_card)

    try:
        db.session.commit()
    except:
        return _error_response('failed', 'Internal server error', 500)

    return _error_response('success', 'Card has been activated', 200)

def validate_card(args):
    card_number = args['card_number']
    card = _get_by_attribute(Card, 'card_number', card_number, serialize=False)

    if card:
        return _error_response('success', 'Card is valid', 200)

    unknown_card = _get_by_attribute(UnknownCard, 'uk_card_number', card_number, serialize=False)

    if unknown_card:
        return _error_response('failed', 'Unknown card with this card number already exists', 409)

    return create_new_unknown_card({'uk_card_number': card_number})

def _get_all(model):
    items = model.query.all()

    if not items:
        return _error_response('failed', 'No cards found', 404)

    return [item.serialize() for item in items], 200

def _get_by_attribute(model, attribute, value, serialize=True):
    item = model.query.filter_by(**{attribute: value}).first()

    if not item:
        return None if not serialize else _error_response('failed', 'Card not found', 404)

    return (item.serialize(), 200) if serialize else item

def _update_card(model, attribute, value, args):
    card_number = args['card_number']

    if not card_number:
        return _error_response('failed', 'Card number is required', 400)

    card = model.query.filter_by(**{attribute: value}).first()

    if not card:
        return _error_response('failed', 'Card not found', 404)
    
    card.card_number = card_number
    db.session.commit()

    return _error_response('success', 'Card has been updated', 200)

def _delete_card(model, attribute, value):
    card = model.query.filter_by(**{attribute: value}).first()

    if not card:
        return _error_response('failed', 'Card not found', 404)

    db.session.delete(card)
    db.session.commit()

    return _error_response('success', 'Card has been deleted', 200)

def _error_response(status, message, code):
    return {
        'status': status,
        'message': message
    }, code