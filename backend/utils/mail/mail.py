# Local imports
from utils.close import exit_app
from utils.mail.mail_settings import mail

# External imports
try: from flask_mail import Message
except ImportError as import_error:
    exit_app(f"Module not found: {import_error}")

def send_mail(subject: str, body: str, sender_name: str, recipients: list) -> dict | None:
    """
    Sends an email to the recipients using gmail smtp

    Args:
        subject (str): Subject of the email
        body (str): Body of the email
        sender_name (str): Name of the sender
        recipients (list): List of recipients
    """

    message = Message(subject, body=body, sender=(sender_name, "proj.aums@gmail.com"), recipients=recipients)

    try:
        mail.send(message)
    except Exception as e:
        return {
            "status": "failed",
            "message": "Failed to send email" }, 500