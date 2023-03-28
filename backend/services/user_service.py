import datetime as dt
from random import Random
from models.user import User, db

def register_new_user(args):
    username = args['username']
    password = args['password']
    first_name = args['first_name']
    last_name = args['last_name']
    birth_date = args['birth_date']
    phone_number = args['phone_number']
    personal_email = args['personal_email']
    address = args['address']
    
    

    if not username or not password or not first_name or not birth_date or not phone_number or not personal_email or not address:
        return {
            'status': 'failed',
            'message': 'All fields are required'}, 400
    if not last_name:
        return{
            'status': 'failed',
            'message': 'The name field should consist of at least two words'
        }, 400

    company_email = f'{first_name.lower()}.{last_name.lower()}@aums.com'
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