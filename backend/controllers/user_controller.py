from models.user import User, db
from flask_restful import Resource, reqparse
from flask_apispec.views import MethodResource

parser = reqparse.RequestParser()
parser.add_argument('address', type=str, help='User Address')
parser.add_argument('username', type=str, help='User Username')
parser.add_argument('password', type=str, help='User Password')
parser.add_argument('last_name', type=str, help='User Last Name')
parser.add_argument('first_name', type=str, help='User First Name')
parser.add_argument('birth_date', type=str, help='User Birth Date')
parser.add_argument('phone_number', type=str, help='User Phone Number')
parser.add_argument('company_email', type=str, help='User Company Email')
parser.add_argument('personal_email', type=str, help='User Personal Email')

class Register(MethodResource, Resource):
    def post(self):
        args = parser.parse_args()

        return {
            'status': 'failed',
            'message': 'Not Implemented Yet'}, 200