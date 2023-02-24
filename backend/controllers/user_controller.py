from models.user import User, db
from flask_restful import Resource, reqparse
from flask_apispec.views import MethodResource

parser = reqparse.RequestParser()
parser.add_argument('address')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('last_name')
parser.add_argument('first_name')
parser.add_argument('birth_date')
parser.add_argument('phone_number')
parser.add_argument('company_email')
parser.add_argument('personal_email')

class Register(MethodResource, Resource):
    def post(self):
        args = parser.parse_args()

        return {
            'status': 'failed',
            'message': 'Not Implemented Yet'}, 200