# Local imports
from utils.log import log
from utils.close import exit_app

try:
    # External imports
    from flask import Flask
    from flask_cors import CORS
    from apispec import APISpec
    from flask_restful import Api
    from apispec.ext.marshmallow import MarshmallowPlugin
except ImportError as import_error: exit_app(f"Module not found: {import_error}")

def create_app(config: object) -> tuple:
    """
    Creates the app and api objects with basic configuration

    Args:
        config (object): The selected configuration object

    Returns:
        tuple: The created app and api objects
    """

    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)
    api = Api(app)
    log.info("App created with basic cfg")

    # Swagger
    app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="AUMS", version="v1",
            plugins=[MarshmallowPlugin()], openapi_version="2.0.0"),
        "APISPEC_SWAGGER_URL": "/swagger/", "APISPEC_SWAGGER_UI_URL": "/swagger-ui/"
    })

    return app, api