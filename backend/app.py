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

# Local used controllers
import controllers.user_controller as user_ctrl
import controllers.card_controller as card_ctrl
import controllers.index_controller as index_ctrl
import controllers.schedule_controller as schedule_ctrl
import controllers.user_card_controller as user_card_ctrl

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

# User routes
api.add_resource(user_ctrl.Login, "/login")
api.add_resource(user_ctrl.Register, "/register")
api.add_resource(user_ctrl.Update, "/users/<int:user_id>")
api.add_resource(user_ctrl.Delete, "/users/<int:user_id>")
api.add_resource(user_ctrl.ChangePassword, "/change_password")
# Schedule routes
api.add_resource(schedule_ctrl.Schedule, "/schedule")
# UserCard routes
api.add_resource(user_card_ctrl.Users, "/users")
api.add_resource(user_card_ctrl.UserCard, "/user_cards", "/user_cards/<int:id>")
# Card routes
api.add_resource(card_ctrl.ActiveCards, "/cards")
api.add_resource(card_ctrl.UnknownCards, "/unknown_cards")
api.add_resource(card_ctrl.ActiveCardById, "/cards/<int:card_id>")
api.add_resource(card_ctrl.ActivateCard, "/activate_card/<int:uk_card_id>")
api.add_resource(card_ctrl.UnknownCardById, "/unknown_cards/<int:uk_card_id>")
api.add_resource(card_ctrl.CardValidation, "/card_validation/<string:card_number>")
# Index routes
api.add_resource(index_ctrl.Index, "/")
api.add_resource(index_ctrl.LogDump, "/log_dump")
api.add_resource(index_ctrl.IsAuthenticated, "/is_authenticated/<string:access_token>")

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
# UserCard docs
docs.register(user_card_ctrl.Users)
docs.register(user_card_ctrl.UserCard)
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

            hardware_user = User(
                first_name="Hardware",
                last_name="Hardware",
                birth_date="2000-01-01",
                phone_number="01234567890",
                address="Szeged",
                company_email="hardware0@proj-aums.hu",
                personal_email="hardware1@proj-aums.hu",
                username="hardware",
                password=bcrypt.hashpw("hardware".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                access_token="OOkbqF8pliyFSWOQOti45PsQfkUTqMfc9MY2w0WshjbyM8li98ffW1eC2xz4kLhscoxSfQI8ajVS2lRRZH8Dqbx6AnvMS6rYhwfjwtVhyAsRSTcVIlnwT9dIGqWnd59f")

            db.session.add(user)
            db.session.add(hardware_user)
            db.session.commit()

            from models.role import Role
            base_user_role = Role(name="Base User", level=1)
            authorized_user_role = Role(name="Authorized User", level=2)
            secretary_role = Role(name="Secretary", level=3)
            manager_role = Role(name="Manager", level=4)
            admin_role = Role(name="Admin", level=5)

            db.session.add(base_user_role)
            db.session.add(authorized_user_role)
            db.session.add(secretary_role)
            db.session.add(manager_role)
            db.session.add(admin_role)

            db.session.commit()

            from models.user_role import UserRole
            user_role = UserRole(user_id=user.id, role_id=admin_role.id)
            hardware_user_role = UserRole(user_id=hardware_user.id, role_id=admin_role.id)

            db.session.add(hardware_user_role)
            db.session.add(user_role)
            db.session.commit()

        log.info("Db created")
    except Exception as db_error: exit_app(f"Db error: {db_error}")

if __name__ == "__main__":
    """
    Main entry point, run app
    """

    log.info("Starting app")

    try:
        if selected_config == "Localhost": app.run(debug=True, port=5000, host="0.0.0.0")
        if selected_config == "Production": serve(app, host="0.0.0.0", port=5000)
    except Exception as app_error: exit_app(f"App error: {app_error}")