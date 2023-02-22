from models import db
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

import controllers.user_controller
import controllers.schedule_controller
from controllers.index_controller import Index

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/aums"

CORS(app)
api = Api(app)

api.add_resource(Index, '/')

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")