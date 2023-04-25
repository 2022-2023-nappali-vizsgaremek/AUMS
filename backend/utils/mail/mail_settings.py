# Local imports
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

    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USE_TLS"] = False
    app.config["TEMPLATES_FOLDER"] = "./"
    app.config["MAIL_SERVER"]="smtp.gmail.com"
    app.config["MAIL_PASSWORD"] = "vxcsjerwoeutzgvv"
    app.config["MAIL_USERNAME"] = "proj.aums@gmail.com"

    mail.init_app(app)