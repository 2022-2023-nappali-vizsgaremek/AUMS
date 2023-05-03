# Local imports
from utils.log import log
from utils.close import exit_app
import services.index_service as service

try:
    # External imports
    from flask_restful import Resource, reqparse
    from flask_apispec import MethodResource, doc
except ImportError as ex: exit_app(f"Module not found: {ex}")

parser = reqparse.RequestParser()

class Index(MethodResource, Resource):
    @doc(description="Get index message", tags=["Index"])
    def get(self) -> dict:
        """
        Get index message

        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Getting index message")
        return service.get_index_message()

class IsAuthenticated(MethodResource, Resource):
    def post(self, access_token: str) -> dict:
        """
        Check if user is authenticated
        Returns:
            dict: A dictionary containing the response and the status code of the request
        """

        log.info("Checking if user is authenticated")
        return service.is_authenticated(access_token)