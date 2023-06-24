import jwt
import string
import secrets
import hashlib

from random import choice

from . import db_queries
from config import settings


# to password hashing
def create_salt(length: int = 12) -> hex:
    """Create a random string"""

    return "".join(choice(string.ascii_letters) for _ in range(length))


def password_hashing(password: str, salt: str | None = None) -> hex:
    """Hashing the user password"""

    if not salt:
        salt = create_salt()

    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)

    return enc.hex()


def validate_password(password: str, hashed_password: str) -> bool:
    """Check if the password matches the hashed password from database"""

    salt, hashed = hashed_password.split("$")
    return password_hashing(password, salt) == hashed


def create_hashed_password(password: str) -> str:
    """Create a hashed_password field of a User model instance"""

    salt = create_salt()
    hashed = password_hashing(password, salt)
    return  f"{salt}${hashed}"


# action to JWT token
def create_user_secret_key(user_id: int) -> hex:
    """Create a random user secret"""

    query = secrets.token_hex()

    db_queries.delete_user_secret_key(user_id)
    db_queries.create_user_secret_key(secret_key=query, user_id=user_id)

    return query


def create_user_token(user_id: int):
    """Create a JWTToken model instance"""

    db_queries.delete_user_token(user_id)

    _secret_key = create_user_secret_key(user_id=user_id)
    _token = jwt.encode(payload={"user_id": user_id}, key=_secret_key, algorithm=settings.JWTTOKEN_SETTINGS["ALGORITHM"])
    query = db_queries.create_user_token(token=_token, user=user_id)

    return query


# async def send_link_to_mail(email: EmailStr, user_id: int) -> None:
#     """Send user account activation link to mail"""

#     link = f"{utils.DOMAIN}/user/{user_id}/activate_account"
#     body = f"To activate your account follow the link: {link}"

#     message = MessageSchema(subject="Activate account", recipients=[email], body=body, subtype="plain")
#     fm = FastMail(conf)
#     await fm.send_message(message)


# async def activate_account(current_user) -> None:
#     """Activate user account"""

#     await current_user.update(is_activated=True)


# async def create_google_user(back_task: BackgroundTasks, first_name: str, last_name: str, email: str) -> int:
#     """Create user with Google"""

#     google_user = await models.Users.objects.get_or_none(email=email)

#     if not google_user:
#         hashed_password = password_hashing(password=create_random_salt(15))
#         user_info = {
#             "first_name": first_name, "last_name": last_name, "email": email, "phone": "1111111111", "gender": "Man",
#             "age": 15, "city": "not specified", "description": "not specified", "password": hashed_password,
#             "is_activated": True
#         }
#         google_user = await models.Users.objects.create(**user_info)

#         back_task.add_task(create_user_directory, google_user.id)

#     return google_user.id


# async def google_auth(back_task: BackgroundTasks, first_name: str, last_name: str, email: str) -> models.Token:
#     """Google authenticated"""

#     google_user_id = await create_google_user(back_task, first_name, last_name, email)
#     token = await create_user_token(google_user_id)
#     return token