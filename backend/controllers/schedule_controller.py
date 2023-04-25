from models.schedule import Schedule, db
from utils.log import log
from utils.close import exit_app
import services.schedule_service as service

try:
    from flask_apispec import MethodResource
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

class Schedule(MethodResource, Resource):
    def get(self):
        log.info("Getting schedule")
        return service.get_schedule()