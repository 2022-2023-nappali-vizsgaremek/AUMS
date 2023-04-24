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

class Localhost(Base):
    """
    Localhost app configurations

    Args:
        Base (object): Base configurations
    """

    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost:3306/aums"

class Production(Base):
    """
    Production app configurations

    Args:
        Base (object): Base configurations
    """

    SQLALCHEMY_DATABASE_URI = "mysql://root:root@mysql_aums:3306/aums"