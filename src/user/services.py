import jwt
import string
import secrets
import hashlib

from random import choice

from . import db_queries
from .celery_tasks import tasks
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
    return f"{salt}${hashed}"


# action to JWT token
def create_user_secret_key(user_id: int) -> hex:
    """Create a random user secret"""

    secret_key = secrets.token_hex()

    db_queries.create_user_secret_key(secret_key=secret_key, user_id=user_id)

    return secret_key


def create_jwttoken(user_id: int, user_email: str = None):
    """Create a JWTToken model instance"""

    _secret_key = create_user_secret_key(user_id=user_id)
    _access_token= jwt.encode(
        payload={settings.JWT_SETTINGS["USER_ID_CLAIM"]: user_id, "type_token": "access"},
        key=_secret_key, 
        algorithm=settings.JWT_SETTINGS["ALGORITHM"]
    )
    _refresh_token= jwt.encode(
        payload={settings.JWT_SETTINGS["USER_ID_CLAIM"]: user_id, "type_token": "refresh"}, 
        key=_secret_key, 
        algorithm=settings.JWT_SETTINGS["ALGORITHM"]
    )

    query = db_queries.create_jwttoken(access_token=_access_token, refresh_token=_refresh_token, user_id=user_id)
    
    if user_email: 
        tasks.send_account_activation.delay(user_email, _secret_key)

    return query
