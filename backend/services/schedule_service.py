from models.schedule import Schedule, db

def get_schedule_by_userid(userid):
    schedules = Schedule.query.filter_by(user_id=userid)

    if not schedules:
        return error_response('Failed, no schedule found', 404)
    print(schedules.serialize())
    return schedules.serialize(), 200


def get_all_schedule():
    all_schedules = Schedule.query.all()

    if not all_schedules:
        return error_response('Failed, no schedule found', 404)
    return [schedule.serialize() for schedule in all_schedules], 200


def error_response(status, message, status_code):
    return {'status': status, 'message': message}, status_code
    