from utils.log import log

def exit_app(msg: str) -> None:
    """
    Log and exit app with error message

    Args:
        msg (str): The given error message
    """

    log.error(msg); exit()