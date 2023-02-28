
from models import db
import imports_app as imp
from create import api, app
from sqlalchemy_utils import database_exists, create_database

from controllers.index_controller import Index
from controllers.user_controller import Register
from controllers.card_controller import Cards

api.add_resource(Index, '/')
api.add_resource(Register, '/register')
api.add_resource(Cards, '/cards', '/cards/<int:card_id>')

docs = imp.FlaskApiSpec(app)
docs.register(Index)
docs.register(Register)
docs.register(Cards)

with app.app_context():
    db.init_app(app)

    if not database_exists(db.engine.url):
        create_database(db.engine.url)

    db.create_all()

if __name__ == '__main__':
    #imp.serve(app, host='0.0.0.0', port=5000)
    app.run(debug=True, port=5000, host="0.0.0.0")