from models import db
from utils.log import log
from create import create_app
from utils.close import exit_app
import controllers.role_controller
import controllers.schedule_controller
import controllers.user_role_controller
import controllers.user_card_controller
from config import MainConfig, LocalhostConfig
from flask_apispec.extension import FlaskApiSpec

try:
    from waitress import serve
    from sqlalchemy_utils import database_exists
    from sqlalchemy_utils import create_database
except ImportError as import_error:
    exit_app(f"Module not found: {import_error}")

import controllers.user_controller as user_ctrl
import controllers.card_controller as card_ctrl
import controllers.index_controller as index_ctrl

# Change the parameter to LocalhostConfig if you want to run locally or MainConfig if you want to run in docker
app, api = create_app(LocalhostConfig)

api.add_resource(user_ctrl.Register, '/register')
api.add_resource(index_ctrl.Index, '/')
api.add_resource(user_ctrl.Login, '/login')
api.add_resource(card_ctrl.ActiveCards, '/cards', '/cards/<int:card_id>')
api.add_resource(card_ctrl.UnknownCards, '/unknown_cards', '/unknown_cards/<int:uk_card_id>')
api.add_resource(card_ctrl.ActivateCard, '/activate_card/<int:uk_card_id>')

docs = FlaskApiSpec(app)
docs.register(user_ctrl.Register)
docs.register(index_ctrl.Index)
docs.register(user_ctrl.Login)
docs.register(card_ctrl.ActiveCards)
docs.register(card_ctrl.UnknownCards)
docs.register(card_ctrl.ActivateCard)

with app.app_context():
    db.init_app(app)
    engine = db.engine.url

    if not database_exists(db.engine.url):
        create_database(db.engine.url)

    try:
        if not database_exists(engine):
            create_database(engine)
        db.create_all()
        log.info("Db created")
    except Exception as db_error:
        exit_app(f"Db error: {db_error}")

if __name__ == '__main__':
    log.debug("Starting app")
    #serve(app, host='0.0.0.0', port=5000)
    app.run(debug=True, port=5000, host="0.0.0.0")