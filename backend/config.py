class MainConfig:
    CORS_HEADERS = 'Content-Type'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@mysql_aums:3306/aums"

class LocalhostConfig(MainConfig):
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost:3306/aums"

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory SQLite database for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False