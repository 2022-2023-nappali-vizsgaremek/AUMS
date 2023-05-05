# Local imports
import string
from random import Random
from utils.log import log
from utils.close import exit_app
from models.user import User, db
from utils.mail.mail import send_mail

# External imports
try: import bcrypt
except ImportError as import_error:
    exit_app(f"Module not found: {import_error}")

def register_new_user(args: dict) -> dict:
    """
    Backend validation and registration of a new user with email notification

    Args:
        args (dict): A dictionary containing the arguments for user registration

    Returns:
        dict: A dictionary containing the status and message of the registration
    """

    address = args["address"]
    last_name = args["last_name"]
    first_name = args["first_name"]
    birth_date = args["birth_date"]
    phone_number = args["phone_number"]
    personal_email = args["personal_email"]

    arg_empty_check = [
        address,
        first_name,
        birth_date,
        phone_number,
        personal_email]

    is_empty = False
    for arg in arg_empty_check:
        if not arg: is_empty = True; break

    if is_empty:
        return {
            "status": "failed",
            "message": "One or more fields are empty" }, 400

    if not last_name:
        return {
            "status": "failed",
            "message": "The name field should consist of at least two words" }, 400

    personal_email_exists = User.query.filter_by(personal_email=personal_email).first()

    if personal_email_exists:
        return {
            "status": "failed",
            "message": "Personal email already exists in the database" }, 409

    username = f"{first_name.lower()}.{last_name.lower()}"
    company_email = f"{username}@proj-aums.hu"

    invalid_chars = ["ö", "ü", "ó", "ő", "ú", "é", "á", "ű", "í"]
    valid_chars = ["o", "u", "o", "o", "u", "e", "a", "u", "i"]

    while True:
        for i in range(len(invalid_chars)):
            username = username.replace(invalid_chars[i], valid_chars[i])
            company_email = company_email.replace(invalid_chars[i], valid_chars[i])

        user_exists = User.query.filter_by(username=username).first()

        if user_exists:
            random = Random().randint(0, 100)

            username = f"{first_name.lower()}.{last_name.lower()}{random}"
            company_email = f"{username}@proj-aums.hu"
        else: break

    pw_characters = string.ascii_letters + string.digits
    password = "".join(Random().choice(pw_characters) for i in range(8))

    hashed =  bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = User(first_name=first_name, last_name=last_name, birth_date=birth_date, phone_number=phone_number, address=address, company_email=company_email, personal_email=personal_email, username=username, password=hashed)
    db.session.add(user)

    try:
        db.session.commit()
        email_resp = send_mail("AUMS Registration", f"AUMS Registration\n\nYour username is: {company_email}\nYour password is: {password}\n\nYou can login at: https://proj-aums.hu/", "AUMS", [personal_email])

        if email_resp:
            log.error(f"Failed to send email to {personal_email}")

            new_password = bcrypt.hashpw(company_email.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            user.password = new_password
            db.session.commit()

    except Exception as e:
        return {
            "status": "failed",
            "message": str(e) }, 500

    return {
        "status": "success",
        "message": "User successfully registered" }, 201

def login_user(args: dict) -> dict:
    """
    Backend validation and login of a user

    Args:
        args (dict): A dictionary containing the arguments for user login

    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    password = args["password"]
    company_email = args["company_email"]
    user = User.query.filter((User.company_email == company_email) | (User.username == company_email)).first()

    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return {
            "status": "failed",
            "message": "Invalid company email or password" }, 401

    token_chars = string.ascii_letters + string.digits
    access_token = "".join(Random().choice(token_chars) for i in range(128))

    user.access_token = access_token
    db.session.commit()

    return {
        "status": "success",
        "access_token": access_token,
        "message": "User successfully logged in" }, 200

def update_user_byId(user_id: int, args: dict) -> dict:
    """
    Backend validation and update of a user by id

    Args:
        user_id (int): The id of the user
        args (dict): A dictionary containing the arguments for user update

    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    return _update_user(User, "id", user_id, args)


def _update_user(model, attribute, value, args) -> tuple:
    """
    

    """

    if (args.len()==0):
        return {
            "status": "failed",
            "message": "No arguments given" }, 400
    
    user = model.query.filter_by(**{attribute: value}).first()

    if not user:
        return {
            "status": "failed",
            "message": "User not found" }, 404
    

    for key, value in args.items():
        if key == "password":
            hashed = bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            setattr(user, key, hashed)
        else:
            setattr(user, key, value)

    try:
        db.session.commit()
    except Exception as e:
        return {
            "status": "failed",
            "message": str(e) }, 500
    
    return {
        "status": "success",
        "message": "User successfully updated" }, 200

    