from models import db
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

import controllers.role_controller
import controllers.card_controller
import controllers.schedule_controller
import controllers.user_role_controller
import controllers.user_card_controller

from controllers.index_controller import Index
from controllers.user_controller import Register

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/aums"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@mysql_aums:3306/aums"

CORS(app)
api = Api(app)
api.add_resource(Index, '/')
api.add_resource(Register, '/register')

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")