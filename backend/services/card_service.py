# Local imports
from datetime import datetime
from models.card import Card, db
from models.unknown_card import UnknownCard

def get_all_cards() -> dict:
    """
    Get all cards from the database

    Returns:
        tuple: A list of cards and a status code
    """

    return _get_all(Card)

def get_unknown_cards() -> dict:
    """
    Get all unknown cards from the database

    Returns:
        tuple: A list of unknown cards and a status code
    """

    return _get_all(UnknownCard)

def get_card_by_number(card_number: str):
    """
    Get a card by card number

    Args:
        card_number (string): The card number

    Returns:
        tuple: A card and a status code if exist, otherwise an error response
    """

    return _get_by_attribute(Card, "card_number", card_number)

def get_card(card_id: int) -> dict:
    """
    Get a card by id

    Args:
        card_id (int): The id of the card

    Returns:
        tuple: A card and a status code if exist, otherwise an error response
    """

    return _get_by_attribute(Card, "id", card_id)

def get_unknown_card(uk_card_id: int) -> dict:
    """
    Get an unknown card by id

    Args:
        uk_card_id (int): The id of the unknown card

    Returns:
        tuple: An unknown card and a status code if exist, otherwise an error response
    """

    return _get_by_attribute(UnknownCard, "id", uk_card_id)

def create_new_unknown_card(args: dict) -> dict:
    """
    Create a new unknown card

    Args:
        args (dict): A dictionary containing the arguments for unknown card creation

    Returns:
        tuple: The response and the status code of the request
    """

    uk_card_number = args["uk_card_number"]

    if not uk_card_number:
        return _response("failed", "Card number is required", 400)

    card = _get_by_attribute(Card, "card_number", uk_card_number, serialize=False)

    if card:
        return _response("failed", "Card number already exists in the active cards", 409)

    uk_card = _get_by_attribute(UnknownCard, "uk_card_number", uk_card_number, serialize=False)

    if uk_card:
        return _response("failed", "Card number already exists in the unknown cards", 409)

    uk_card = UnknownCard(uk_card_number=uk_card_number)
    db.session.add(uk_card)
    db.session.commit()

    return _response("success", "Card has been added to the database", 201)

def update_card(args: dict, card_id: int) -> dict:
    """
    Update a card

    Args:
        args (dict): A dictionary containing the arguments for card update
        card_id (int): The id of the card

    Returns:
        tuple: The response and the status code of the request
    """

    return _update_card(Card, "id", card_id, args)

def update_unknown_card(args: dict, uk_card_id: int) -> dict:
    """
    Update an unknown card

    Args:
        args (dict): A dictionary containing the arguments for unknown card update
        uk_card_id (int): The id of the unknown card

    Returns:
        tuple: The response and the status code of the request
    """

    return _update_card(UnknownCard, "id", uk_card_id, args)

def delete_card(card_id: int) -> dict:
    """
    Delete a card

    Args:
        card_id (int): The id of the card

    Returns:
        tuple: The response and the status code of the request
    """

    return _delete_card(Card, "id", card_id)

def delete_unknown_card(uk_card_id: int) -> dict:
    """
    Delete an unknown card

    Args:
        uk_card_id (int): The id of the unknown card

    Returns:
        tuple: The response and the status code of the request
    """
    return _delete_card(UnknownCard, "id", uk_card_id)

def activate_card(uk_card_id: int) -> dict:
    """
    Activate an unknown card

    Args:
        uk_card_id (int): The id of the unknown card

    Returns:
        tuple: The response and the status code of the request
    """

    uk_card = _get_by_attribute(UnknownCard, "id", uk_card_id, serialize=False)
    if not uk_card: return _response("failed", "Card not found", 404)

    new_card = Card(card_number=uk_card.uk_card_number)
    db.session.add(new_card)
    db.session.delete(uk_card)

    try: db.session.commit()
    except: return _response("failed", "Internal server error", 500)

    return _response("success", "Card has been activated", 200)

def validate_card(card_number: str) -> dict:
    """
    Validate a card

    Args:
        args (dict): A dictionary containing the arguments for card validation

    Returns:
        tuple: The response and the status code of the request
    """

    card = _get_by_attribute(Card, "card_number", card_number, serialize=False)

    if card:
        from models.schedule import Schedule
        from models.user_card import UserCard
        user_card = UserCard.query.filter_by(card_id=card.id).first()

        if user_card:
            last_schedule = Schedule.query.filter_by(user_id=user_card.user_id).order_by(Schedule.id.desc()).first()

            if last_schedule and not last_schedule.leave_date:
                last_schedule.leave_date = datetime.now()
            else:
                new_schedule = Schedule(user_id=user_card.user_id, enter_date=datetime.now())
                db.session.add(new_schedule)

            try: db.session.commit()
            except: return _response("failed", "Internal server error", 500)

            return _response("success", "Card is valid", 200)
        else: return _response("failed", "Card is valid but not connected to any user", 401)

    unknown_card = _get_by_attribute(UnknownCard, "uk_card_number", card_number, serialize=False)

    if unknown_card:
        return _response("failed", "Unknown card with this card number already exists", 409)

    return create_new_unknown_card({"uk_card_number": card_number})

def _get_all(model) -> tuple:
    """
    Get all cards

    Args:
        model (Any): The model of the cards

    Returns:
        tuple: A list of cards and a status code if exist, otherwise an error response
    """

    items = model.query.all()

    if not items:
        return _response("failed", "No cards found", 404)

    return [item.serialize() for item in items], 200

def _get_by_attribute(model, attribute, value, serialize=True) -> tuple:
    """
    Get a card by an attribute

    Args:
        model (Any): The model of the card
        attribute (Any): The attribute of the card
        value (Any): The value of the attribute
        serialize (bool, optional): Whether to serialize the card or not. Defaults to True.

    Returns:
        tuple: A card and a status code if exist, otherwise an error response
    """

    item = model.query.filter_by(**{attribute: value}).first()

    if not item:
        return None if not serialize else _response("failed", "Card not found", 404)

    return (item.serialize(), 200) if serialize else item

def _update_card(model, attribute, value, args) -> tuple:
    """
    Update a card

    Args:
        model (Any): The model of the card
        attribute (Any): The attribute of the card
        value (Any): The value of the attribute
        args (dict): A dictionary containing the arguments for card update

    Returns:
        tuple: The response and the status code of the request
    """

    card_number = args["card_number"]

    if not card_number:
        return _response("failed", "Card number is required", 400)

    card = model.query.filter_by(**{attribute: value}).first()

    if not card:
        return _response("failed", "Card not found", 404)

    card.card_number = card_number
    db.session.commit()

    return _response("success", "Card has been updated", 200)

def _delete_card(model, attribute, value) -> tuple:
    """
    Delete a card

    Args:
        model (Any): The model of the card
        attribute (Any): The attribute of the card
        value (Any): The value of the attribute

    Returns:
        tuple: The response and the status code of the request
    """

    card = model.query.filter_by(**{attribute: value}).first()

    if not card:
        return _response("failed", "Card not found", 404)

    db.session.delete(card)
    db.session.commit()

    return _response("success", "Card has been deleted", 200)

def _response(status: str, message: str, code: int) -> dict:
    """
    Create an error response

    Args:
        status (str): The status of the response
        message (str): The message of the response
        code (int): The status code of the response

    Returns:
        dict: The response and the status code of the request
    """

    return {
        "status": status,
        "message": message }, code