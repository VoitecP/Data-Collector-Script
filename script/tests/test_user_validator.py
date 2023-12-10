import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from script_files.db_manager import Base, User
from script_files.user_validator import LoginFormat, UserValidator


@pytest.fixture(scope='session')
def engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine, tables):
    ''' Returns an sqlalchemy session, 
    and after the test tears down everything properly.'''
    connection = engine.connect()
    # this metod uses nested transaction, and already started transaction
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    connection.close()


@pytest.fixture
def valid_phone():
    phone = '123456789'
    return phone

@pytest.fixture
def valid_email():
    email = 'test@example.com'
    return email

@pytest.fixture
def valid_password():
    return 'password12'

@pytest.fixture
def invalid_password():
    return 'pass'


def test_phone_format(valid_phone):
    login_format = LoginFormat(login=valid_phone, password='')
    assert login_format.phone_format() == True

def test_email_format(valid_email):
    login_format = LoginFormat(login=valid_email, password='')
    assert login_format.email_format() == True

def test_invalid_email_format(valid_phone):
    login_format = LoginFormat(login=valid_phone, password='')
    assert login_format.email_format() == False

def test_password_format(valid_password):
    login_format = LoginFormat(login='', password=valid_password)
    assert login_format.password_format() == True

def test_invalid_password_format(invalid_password):
    login_format = LoginFormat(login='', password=invalid_password)
    assert login_format.password_format() == False



def test_user_authentication(valid_email, valid_password, session):
    
    user_data = {
        'firstname': 'Test',
        'telephone_number': '123456789',
        'email': valid_email,
        'password': valid_password,
        'role': 'admin',
        'created_at': '2023',
        'children' : []
    }

    session.add(User(user_data))
    session.commit()

    user_validator = UserValidator(login=user_data['email'], password=user_data['password'], session=session)
    
    print(f'\n{user_data}')
    assert user_validator.authenticate() == True
    assert user_validator.is_admin() == True

    session.query(User).delete()
    session.commit()
    session.close()
