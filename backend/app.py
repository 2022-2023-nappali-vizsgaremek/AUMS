# Local imports
import config
from models import db
from utils.log import log
from create import create_app
from utils.close import exit_app
from utils.mail.mail_settings import configure_mail

# Local empty controllers
import controllers.role_controller
import controllers.user_role_controller
import controllers.user_card_controller

# Local used controllers
import controllers.user_controller as user_ctrl
import controllers.index_controller as index_ctrl
import controllers.card_controller as card_ctrl
import controllers.schedule_controller as schedule_ctrl

try:
    # External imports
    import bcrypt
    from waitress import serve
    from sqlalchemy_utils import database_exists
    from sqlalchemy_utils import create_database
    from flask_apispec.extension import FlaskApiSpec
except ImportError as import_error: exit_app(f"Module not found: {import_error}")

# Config type to run app
selected_config = "Localhost"
if selected_config == "Localhost": app, api = create_app(config.Localhost)
elif selected_config == "Production": app, api = create_app(config.Production)

configure_mail(app)

# Index routes
api.add_resource(index_ctrl.Index, "/")
api.add_resource(index_ctrl.LogDump, "/log_dump")
api.add_resource(index_ctrl.IsAuthenticated, "/is_authenticated/<string:access_token>")
# User routes
api.add_resource(user_ctrl.Login, "/login")
api.add_resource(user_ctrl.Register, "/register")
# Schedule routes
api.add_resource(schedule_ctrl.Schedule, "/schedule")
# Card routes
api.add_resource(card_ctrl.ActiveCards, "/cards")
api.add_resource(card_ctrl.UnknownCards, "/unknown_cards")
api.add_resource(card_ctrl.ActiveCardById, "/cards/<int:card_id>")
api.add_resource(card_ctrl.ActivateCard, "/activate_card/<int:uk_card_id>")
api.add_resource(card_ctrl.UnknownCardById, "/unknown_cards/<int:uk_card_id>")
api.add_resource(card_ctrl.CardValidation, "/card_validation/<string:card_number>")

# Swagger docs
docs = FlaskApiSpec(app)
# Index docs
docs.register(index_ctrl.Index)
docs.register(index_ctrl.LogDump)
docs.register(index_ctrl.IsAuthenticated)
# User docs
docs.register(user_ctrl.Login)
docs.register(user_ctrl.Register)
# Schedule docs
docs.register(schedule_ctrl.Schedule)
# Card docs
docs.register(card_ctrl.ActiveCards)
docs.register(card_ctrl.UnknownCards)
docs.register(card_ctrl.ActivateCard)
docs.register(card_ctrl.ActiveCardById)
docs.register(card_ctrl.CardValidation)
docs.register(card_ctrl.UnknownCardById)

with app.app_context():
    """
    Create database and tables if not exists
    """

    db.init_app(app)
    engine = db.engine.url

    try:
        created_now = False
        if not database_exists(engine):
            create_database(engine)
            created_now = True

        db.create_all()

        if created_now:
            from models.user import User
            user = User(
                first_name="Admin",
                last_name="Admin",
                birth_date="2000-01-01",
                phone_number="36203344567",
                address="Szeged",
                company_email="admin.admin@proj-aums.hu",
                personal_email="postmaster@proj-aums.hu",
                username="admin.admin",
                password=bcrypt.hashpw("admin".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))
            db.session.add(user)
            db.session.commit()

        log.info("Db created")
    except Exception as db_error:
        exit_app(f"Db error: {db_error}")

if __name__ == "__main__":
    """
    Main entry point, run app
    """

    log.info("Starting app")

    try:
        if selected_config == "Localhost": app.run(debug=True, port=5000, host="0.0.0.0")
        if selected_config == "Production": serve(app, host="0.0.0.0", port=5000)
    except Exception as app_error: exit_app(f"App error: {app_error}")