from functools import wraps
from flask import jsonify, request, make_response

def auth_required(f):
    """
    Decorator for authentication

    Args:
        f (any): The function to be decorated

    Returns:
        any: The decorated function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("Authorization")

        if not access_token or is_authenticated(access_token.split(" ")[1])[0]["status"] != "success":
            return make_response(jsonify({"message": "Invalid or missing access token" + str(access_token)}), 401)
        return f(*args, **kwargs)
    return decorated_function

def role_level_required(required_role):
    """
    Decorator for role level authentication

    Args:
        required_role (int): The required role level
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            header_data = request.headers.get("Authorization")
            access_token = header_data.split(" ")[1]

            if access_token and is_authenticated(access_token)[0]["status"] == "success":
                from models.user import User
                from models.role import Role
                from models.user_role import UserRole

                user = User.query.filter_by(access_token=access_token).first()
                user_role_id = UserRole.query.filter_by(user_id=user.id).first().role_id
                user_role_level = Role.query.filter_by(id=user_role_id).first().level

                if user_role_level < required_role:
                    return make_response(jsonify({"message": "Insufficient role level"}), 401)
            else: return make_response(jsonify({"message": "Invalid or missing access token"}), 401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_index_message() -> dict:
    """
    Returns the message of the index page

    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    return {
        "status": "success",
        "message": "AUMS Rest API" }, 200

def is_authenticated(access_token: str) -> dict:
    """
    Checks if user is authenticated
    Args:
        access_token (str): The access token of the user
    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    from models.user import User
    from models.role import Role
    from models.user_role import UserRole

    user = User.query.filter_by(access_token=access_token).first()

    user_role = UserRole.query.filter_by(user_id=user.id).first()
    role = Role.query.filter_by(id=user_role.role_id).first()

    if not user:
        return {
            "status": "failed",
            "message": "Invalid access token" }, 401

    return {
        "status": "success",
        "role_level": role.level,
        "message": "User is authenticated" }, 200

def get_log_dump() -> dict:
    """
    Returns the log dump

    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    from utils.log import log
    log.info("Getting log dump")

    log_dump = ""
    with open("app.log", "r") as file:
        log_dump = file.read()

    return {
        "status": "success",
        "message": "Log dump",
        "log_dump": log_dump }, 200