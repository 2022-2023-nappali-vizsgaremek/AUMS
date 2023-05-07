# Local imports
from utils.log import log
from utils.close import exit_app
import services.schedule_service as service
from services.index_service import auth_required
from services.index_service import role_level_required

try:
    # External imports
    from flask_apispec import MethodResource, doc
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

class Schedule(MethodResource, Resource):
    @doc(description="Get all schedules", tags=["Schedule"])
    @auth_required
    @role_level_required(2)
    def get(self):
        """
        Get all schedules

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Getting schedule")
        return service.get_all_schedule()