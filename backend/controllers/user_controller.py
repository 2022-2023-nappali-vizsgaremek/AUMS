from utils.log import log
from utils.close import exit_app
import services.index_service as service

try:
    from flask_apispec import MethodResource
    from flask_restful import Resource, reqparse
except ImportError as ex: exit_app(f"Module not found: {ex}")

parser = reqparse.RequestParser()
parser.add_argument('address', type=str, location='form')
parser.add_argument('username', type=str, location='form')
parser.add_argument('password', type=str, location='form')
parser.add_argument('last_name', type=str, location='form')
parser.add_argument('first_name', type=str, location='form')
parser.add_argument('birth_date', type=str, location='form')
parser.add_argument('phone_number', type=str, location='form')
parser.add_argument('company_email', type=str, location='form')
parser.add_argument('personal_email', type=str, location='form')

class Register(MethodResource, Resource):
    def post(self):
        args = parser.parse_args()
        log.info("Registering new user")
        return service.register_new_user(args)