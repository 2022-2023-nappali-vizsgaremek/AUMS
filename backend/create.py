from utils.log import log
from utils.close import exit_app
from config import MainConfig, LocalhostConfig

try:
    from flask import Flask
    from flask_cors import CORS
    from apispec import APISpec
    from flask_restful import Api
    from apispec.ext.marshmallow import MarshmallowPlugin
except ImportError as import_error:
    exit_app(f"Module not found: {import_error}")

def create_app(MainConfig):
    app = Flask(__name__)
    app.config.from_object(MainConfig)

    CORS(app)
    api = Api(app)
    log.info("App created with basic cfg")

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='AUMS', version='v1',
            plugins=[MarshmallowPlugin()], openapi_version='2.0.0'),
        'APISPEC_SWAGGER_URL': '/swagger/', 'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'
    })

    return app, api