from flask import Flask
from flask_cors import CORS
from apispec import APISpec
from flask_restful import Api
from apispec.ext.marshmallow import MarshmallowPlugin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)
api = Api(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='AUMS', version='v1',
        plugins=[MarshmallowPlugin()], openapi_version='2.0.0'),
    'APISPEC_SWAGGER_URL': '/swagger/', 'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'})