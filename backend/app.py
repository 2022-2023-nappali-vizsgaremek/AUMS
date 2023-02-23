from models import db
from flask import Flask
from apispec import APISpec
from flask_cors import CORS
from flask_restful import Api
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from sqlalchemy_utils import database_exists, create_database

import controllers.role_controller
import controllers.card_controller
import controllers.schedule_controller
import controllers.user_role_controller
import controllers.user_card_controller

from controllers.index_controller import Index
from controllers.user_controller import Register

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/aums"
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@mysql_aums:3306/aums"

CORS(app)
api = Api(app)
api.add_resource(Index, '/')
api.add_resource(Register, '/register')

with app.app_context():
    db.init_app(app)
    if not database_exists(db.engine.url):
        create_database(db.engine.url)
    db.create_all()

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='AUMS', version='v1',
        plugins=[MarshmallowPlugin()], openapi_version='2.0.0'),
    'APISPEC_SWAGGER_URL': '/swagger/', 'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'})

docs = FlaskApiSpec(app)
docs.register(Register)
docs.register(Index)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")