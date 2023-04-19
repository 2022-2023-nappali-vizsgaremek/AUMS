from datetime import date
from tests.test_config import test_client, init_database
from services.user_service import register_new_user, loginuser

def register_user_args():
    args = {
        'first_name': 'Test',
        'last_name': 'User',
        'birth_date': date(1999, 1, 1),
        'phone_number': '12345678',
        'address': '123 Test St.',
        'personal_email': 'user.email@gmail.com',
        'username': 'test_user',
        'password': 'password'
    }
    
    return args

def login_user_args():
    args = {
        'company_email': 'test.user@aums.com',
        'password': 'password'
    }
    
    return args

def test_register_user(test_client, init_database):
    with test_client.application.app_context():
        
        response, status_code = register_new_user(register_user_args())
        
        assert status_code == 201
        assert response['status'] == 'success'
        assert response['message'] == 'User successfully registered'

def test_register_user_wrong_fields(test_client, init_database):
    modified_args = register_user_args()
    modified_args['username'] = ''
    
    response, status_code = register_new_user(modified_args)
    
    assert status_code == 400
    assert response['status'] == 'failed'
    assert response['message'] == 'All fields are required'

def test_loginuser(test_client, init_database):
    with test_client.application.app_context():
    
        register_new_user(register_user_args())
        response, status_code = loginuser(login_user_args())

        assert status_code == 200
        assert response['status'] == 'success'
        assert response['message'] == 'User successfully logged in'
        
def test_loginuser_invalid_password(test_client, init_database):
    with test_client.application.app_context():
    
        register_new_user(register_user_args())
        modified_args = login_user_args()
        modified_args['password'] = 'wrong_password'
        response, status_code = loginuser(modified_args)
        
        assert status_code == 401
        assert response['status'] == 'failed'
        assert response['message'] == 'Invalid company email or password'
        
def test_loginuser_invalid_company_email(test_client, init_database):
    with test_client.application.app_context():
    
        register_new_user(register_user_args())
        modified_args = login_user_args()
        modified_args['company_email'] = 'shady.person@injection.com'
        response, status_code = loginuser(modified_args)
        
        assert status_code == 401
        assert response['status'] == 'failed'
        assert response['message'] == 'Invalid company email or password'