# Local imports
import re
import string
from utils.log import log
from datetime import date
from random import Random
from typing import Optional
from utils.close import exit_app
from models.user import User, db
from models.schedule import Schedule
from models.user_role import UserRole
from models.user_card import UserCard
from utils.mail.mail import send_mail

# External imports
try: import bcrypt
except ImportError as import_error:
    exit_app(f"Module not found: {import_error}")

def register_new_user(args: dict, password: Optional[str] = None, return_password: bool = False) -> dict:
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
    role_level = args["role_level"]
    phone_number = args["phone_number"]
    personal_email = args["personal_email"]

    arg_empty_check = [
        address,
        first_name,
        birth_date,
        role_level,
        phone_number,
        personal_email]

    is_empty = False
    for arg in arg_empty_check:
        if not arg: is_empty = True; break

    if is_empty:
        return {
            "status": "failed",
            "message": "One or more fields are empty" }, 400

    validations = [
        (phone_number, r"^\d{11}$", "The phone number is invalid"),
        (str(role_level), r"^[1-5]$", "The role level is invalid"),
        (address, r"^[a-zA-Z0-9\s,.\"-]{3,}$", "The address is invalid"),
        (birth_date, r"^\d{4}-\d{2}-\d{2}$", "The birth date is invalid"),
        (personal_email, r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", "The personal email is invalid"),
        (last_name, r"^[a-zA-ZáÁéÉíÍóÓöÖőŐúÚüÜűŰ]+(([\" ][a-zA-ZáÁéÉíÍóÓöÖőŐúÚüÜűŰ])?[a-zA-ZáÁéÉíÍóÓöÖőŐúÚüÜűŰ]*)*$", "The last name is invalid"),
        (first_name, r"^[a-zA-ZáÁéÉíÍóÓöÖőŐúÚüÜűŰ]+(([\" ][a-zA-ZáÁéÉíÍóÓöÖőŐúÚüÜűŰ])?[a-zA-ZáÁéÉíÍóÓöÖőŐúÚüÜűŰ]*)*$", "The first name is invalid")
    ]

    for value, pattern, error_message in validations:
        if isinstance(value, date):
            value = value.isoformat()

        if not re.match(pattern, value):
            return {
                "status": "failed",
                "message": error_message }, 400

    personal_email_exists = User.query.filter_by(personal_email=personal_email).first()
    if personal_email_exists:
        return {
            "status": "failed",
            "message": "Personal email already exists in the database" }, 409

    username, company_email = generate_unique_username_and_email(first_name, last_name)

    if password is None:
        pw_characters = string.ascii_letters + string.digits
        password = "".join(Random().choice(pw_characters) for i in range(8))

    hashed =  bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = User(first_name=first_name, last_name=last_name, birth_date=birth_date, phone_number=phone_number, address=address, company_email=company_email, personal_email=personal_email, username=username, password=hashed)
    db.session.add(user)

    try:
        db.session.commit()

        from models.role import Role
        from models.user_role import UserRole

        role_id_form_level = Role.query.filter_by(level=role_level).first().id
        user_role = UserRole(user_id=user.id, role_id=role_id_form_level)
        db.session.add(user_role)
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

    log.info(f"New user registered: {company_email}")

    if return_password:
        return {
            "status": "success",
            "message": "User successfully registered" }, 201, password, username
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

    from models.role import Role
    from models.user_role import UserRole

    user_role = UserRole.query.filter_by(user_id=user.id).first()
    role = Role.query.filter_by(id=user_role.role_id).first()

    return {
        "status": "success",
        "role_level": role.level,
        "access_token": access_token,
        "name": f"{user.first_name} {user.last_name}",
        "username": user.username,
        "birth_date": user.birth_date,
        "personal_email": user.personal_email,
        "company_email": user.company_email,
        "phone_number": user.phone_number,
        "address": user.address,
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

def remove_user_byId(user_id: int) -> dict:
    """
    Backend validation and removal of a user by id

    Args:
        user_id (int): The id of the user

    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    return _delete_user(User, "id", user_id)

def change_user_password(args) -> dict:
    """
    Backend validation and password change of a user by id

    Args:
        user_id (int): The id of the user
        args (dict): A dictionary containing the arguments for user password change

    Returns:
        dict: A dictionary containing the response and the status code of the request
    """

    access_token = args["access_token"]
    new_password = args["new_password"]
    current_password = args["current_password"]
    confirm_password = args["confirm_password"]

    validations = [
        (new_password, r"^[a-zA-Z0-9_\-\.]+$", "New password contains invalid characters"),
        (current_password, r"^[a-zA-Z0-9_\-\.]+$", "Current password contains invalid characters"),
        (confirm_password, r"^[a-zA-Z0-9_\-\.]+$", "Confirm password contains invalid characters")
    ]

    for value, regex, message in validations:
        if not re.match(regex, value):
            return {
                "status": "failed",
                "message": message }, 400

    if new_password != confirm_password:
        return {
            "status": "failed",
            "message": "New password and confirm password do not match" }, 400

    user = User.query.filter_by(access_token=access_token).first()

    if not user or not bcrypt.checkpw(current_password.encode("utf-8"), user.password.encode("utf-8")):
        return {
            "status": "failed",
            "message": "Invalid current password" }, 401

    user.password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    db.session.commit()

    return {
        "status": "success",
        "message": "Password successfully changed" }, 200

def _update_user(model, attribute, value, args) -> tuple:
    """
    Update a user

    Args:
        model (Any): The model of the user
        attribute (Any): The attribute of the user
        value (Any): The value of the attribute
        args (dict): A dictionary containing the arguments for user update

    Returns:
        tuple: The response and the status code of the request
    """

    if (len(args) == 0):
        return {
            "status": "failed",
            "message": "No arguments given" }, 400

    user = model.query.filter_by(**{attribute: value}).first()

    if not user:
        return {
            "status": "failed",
            "message": "User not found" }, 404

    update_username_and_email = False
    for key, value in args.items():
        if value is not None and value != "":
            if key in ["first_name", "last_name"]:
                update_username_and_email = True
            setattr(user, key, value)

    if update_username_and_email:
        new_username, new_company_email = generate_unique_username_and_email(user.first_name, user.last_name)
        user.username = new_username
        user.company_email = new_company_email

    try: db.session.commit()
    except Exception as e:
        return {
            "status": "failed",
            "message": str(e) }, 500

    return {
        "status": "success",
        "message": "User successfully updated" }, 200

def _delete_user(model, attribute, value) -> tuple:
    """
    Delete a user and its related records in other tables.

    Args:
        model (Any): The model of the user
        attribute (Any): The attribute of the user
        value (Any): The value of the attribute

    Returns:
        tuple: The response and the status code of the request
    """

    user = model.query.filter_by(**{attribute: value}).first()

    if not user:
        return {
            "status": "failed",
            "message": "User not found" }, 404

    UserRole.query.filter_by(user_id=user.id).delete()
    Schedule.query.filter_by(user_id=user.id).delete()
    UserCard.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)

    try: db.session.commit()
    except Exception as e:
        return {
            "status": "failed",
            "message": str(e) }, 500

    return {
        "status": "success",
        "message": "User successfully deleted" }, 200

def generate_unique_username_and_email(first_name: str, last_name: str) -> tuple:
    """
    Generate a unique username and company email for a user.

    Args:
        first_name (str): The user's first_name
        last_name (str): The user's last_name

    Returns:
        tuple: The generated username and company email
    """

    username = f"{first_name.lower()}.{last_name.lower()}"
    company_email = f"{username}@proj-aums.hu"

    invalid_chars = ["ö", "ü", "ó", "ő", "ú", "é", "á", "ű", "í"]
    valid_chars = ["o", "u", "o", "o", "u", "e", "a", "u", "i"]

    for i in range(len(invalid_chars)):
        username = username.replace(invalid_chars[i], valid_chars[i])
        company_email = company_email.replace(invalid_chars[i], valid_chars[i])

    while User.query.filter_by(username=username).first():
        random = Random().randint(0, 100)
        username = f"{first_name.lower()}.{last_name.lower()}{random}"
        company_email = f"{username}@proj-aums.hu"

        for i in range(len(invalid_chars)):
            username = username.replace(invalid_chars[i], valid_chars[i])
            company_email = company_email.replace(invalid_chars[i], valid_chars[i])

    return username, company_email