import pytest
from models.user import User

@pytest.fixture(scope='module')
def valid_user():
    user = User(
        first_name='John',
        last_name='Doe',
        birth_date='1990-01-01',
        phone_number='123456789',
        address='1234 Main St',
        company_email='john.doe@aums.com',
        personal_email='john.john@gmail.com',
        username='johnny',
        password='password')
        
    return user

def test_user_creation(valid_user):
    assert valid_user.first_name == 'John'
    assert valid_user.last_name == 'Doe'
    assert valid_user.birth_date == '1990-01-01'
    assert valid_user.phone_number == '123456789'
    assert valid_user.address == '1234 Main St'
    assert valid_user.company_email == 'john.doe@aums.com'
    assert valid_user.personal_email == 'john.john@gmail.com'
    assert valid_user.username == 'johnny'
    assert valid_user.password == 'password'