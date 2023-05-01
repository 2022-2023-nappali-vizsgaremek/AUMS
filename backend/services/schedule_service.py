from models.schedule import Schedule, db

def get_schedule_by_userid(userid: int) -> dict:
    """
    Get schedule by userid

    Args:
        userid (int): The id of the user

    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    schedules = Schedule.query.filter_by(user_id=userid)

    if not schedules:
        return error_response("No schedule found", 404)

    return schedules.serialize(), 200


def get_all_schedule() -> dict:
    """
    Get all schedules

    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    all_schedules = Schedule.query.all()

    if not all_schedules:
        return error_response("No schedule found", 404)
    return [schedule.serialize() for schedule in all_schedules], 200


def error_response(message, status_code):
    return {"status": "failed", "message": message}, status_code