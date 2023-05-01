# Local imports
from utils.env import get_env
from utils.close import exit_app

# External imports
try: from flask_mail import Mail
except ImportError as import_error:
    exit_app(f"Module not found: {import_error}")

mail = Mail()

def configure_mail(app):
    """
    Configure mail settings

    Args:
        app (Flask): Flask app instance
    """

    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_PORT"] = get_env("MAIL_PORT")
    app.config["MAIL_SERVER"]= get_env("MAIL_SERVER")
    app.config["MAIL_USERNAME"] = get_env("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = get_env("MAIL_PASSWORD")

    mail.init_app(app)