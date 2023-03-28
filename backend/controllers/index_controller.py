from utils.log import log
from utils.close import exit_app
import services.index_service as service

try:
    from flask_apispec import MethodResource
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

class Index(MethodResource, Resource):
    def get(self):
        log.info("Getting index message")
        return service.get_index_message()