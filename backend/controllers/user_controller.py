import datetime as dt
from random import Random
from models.user import User, db
from flask_restful import Resource, reqparse
from flask_apispec.views import MethodResource

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

        username = args['username']
        password = args['password']
        first_name = args['first_name']
        last_name = args['last_name']
        birth_date = dt.datetime.strptime(args['birth_date'], '%Y-%m-%d')
        phone_number = args['phone_number']
        personal_email = args['personal_email']
        address = args['address']

        company_email = f'{first_name.lower()}.{last_name.lower()}@aums.com'

        if not username or not password or not first_name or not last_name or not birth_date or not phone_number or not personal_email or not address:
            return {
                'status': 'failed',
                'message': 'All fields are required'}, 400
        
        user_exists = User.query.filter_by(username=username).first()
        company_email_exists = User.query.filter_by(company_email=company_email).first()
        personal_email_exists = User.query.filter_by(personal_email=personal_email).first()

        if user_exists:
            return {
                'status': 'failed',
                'message': 'Username already exists in the database'}, 409
        
        if company_email_exists:
            company_email = f'{first_name.lower()}.{last_name.lower()}{(Random().randint(0, 100))}@aums.com'

        if personal_email_exists:
            return {
                'status': 'failed',
                'message': 'Personal email already exists in the database'}, 409
        
        user = User(first_name=first_name, last_name=last_name, birth_date=birth_date, phone_number=phone_number, address=address, company_email=company_email, personal_email=personal_email, username=username, password=password)
        db.session.add(user)

        try:
            db.session.commit()
        except Exception as e:
            return {
                'status': 'failed',
                'message': str(e)}, 500
        return {
            'status': 'success',
            'message': 'User successfully registered'}, 201