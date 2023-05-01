# Local imports
from utils.log import log
from utils.close import exit_app
import services.schedule_service as service

try:
    # External imports
    from flask_apispec import MethodResource, doc
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

class Schedule(MethodResource, Resource):
    @doc(description="Get all schedules", tags=["Schedule"])
    def get(self):
        """
        Get all schedules

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Getting schedule")
        return service.get_all_schedule()