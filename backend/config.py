# Local imports
from utils.env import get_env

class Base:
    """
    Base app configurations
    """

    CORS_HEADERS = "Content-Type"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Test(Base):
    """
    Pytest app configurations

    Args:
        Base (object): Base configurations
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SEND_EMAILS = False

class Localhost(Base):
    """
    Localhost app configurations

    Args:
        Base (object): Base configurations
    """

    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost:3306/aums"
    SEND_EMAILS = False

class Production(Base):
    """
    Production app configurations

    Args:
        Base (object): Base configurations
    """

    try:
        SQLALCHEMY_DATABASE_URI = get_env("PRODUCTION_DATABASE_URI")
    except SystemExit:
        SQLALCHEMY_DATABASE_URI = None