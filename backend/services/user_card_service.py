from models.card import Card, db
from models.user import User
from models.user_card import UserCard

def get_all_user_cards() -> dict:
    """
    Get all user cards from the database

    Returns:
        tuple: A list of user cards and a status code
    """

    return _get_all(UserCard)

def get_users() -> dict:
    """
    Get all users from the database

    Returns:
        tuple: A list of users and a status code
    """

    return _get_all(User)

def connect_card_to_user(card_id:int, user_id:int) -> dict:
    """
    Connect card to user

    Args:
        card_id (int): The id of the card
        user_id (int): The id of the user

    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    card = Card.query.filter_by(id=card_id).first()
    if not card: return _error_response("failed", "Card not found", 404)

    user = User.query.filter_by(id=user_id).first()
    if not user: return _error_response("failed", "User not found", 404)

    user_card = UserCard.query.filter_by(card_id=card_id).first()
    if user_card: return _error_response("failed", "Card already connected to a user", 400)

    new_user_card = UserCard(card_id=card_id, user_id=user_id)
    db.session.add(new_user_card)

    try: db.session.commit()
    except: return _error_response("failed", "Internal server error", 500)

    return _error_response("success", "Card has been connected to user", 200)


def delete_user_card(conn_id:int) -> dict:
    """
    Delete user-card connection

    Args:
        id (int): The id of the user-card connection

    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    user_card = UserCard.query.filter_by(id=conn_id).first()
    if not user_card: return _error_response("failed", "User card not found", 404)

    db.session.delete(user_card)

    try: db.session.commit()
    except: return _error_response("failed", "Internal server error", 500)

    return _error_response("success", "User card has been deleted", 200)

def _get_all(model) -> tuple:
    """
    Get all user cards

    Args:
        model (Any): The model of the user cards

    Returns:
        tuple: A list of user cards and a status code if exist, otherwise an error response
    """

    items = model.query.all()
    if not items: return _error_response("failed", "No user cards found", 404)

    return [item.serialize() for item in items], 200


def _error_response(status: str, message: str, code: int) -> dict:
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