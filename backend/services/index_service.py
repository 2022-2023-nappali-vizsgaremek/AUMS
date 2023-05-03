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
    user = User.query.filter_by(access_token=access_token).first()

    if not user:
        return {
            "status": "failed",
            "message": "Invalid access token" }, 401

    return {
        "status": "success",
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
    