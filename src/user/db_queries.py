from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from . import models
from .auth import models as auth_models


def get_or_none(username: str, model = models.User):
    """If model instance exists, return it, otherwise return None"""

    try:
        query = model.objects.get(username=username)
    except ObjectDoesNotExist:
        query = None

    return query


def get_user_by_username(username: str) -> models.User or None:
    """Get user by username""" 

    query = get_or_none(username)
    return query


# action with SecretKey model instance
def create_user_secret_key(secret_key: str, user_id: int) -> None:
    """Create user secret key to SecretKey model"""

    auth_models.SecretKey.objects.update_or_create(user_id=user_id, defaults={"key":secret_key, "created": datetime.now()})


# action with JWTToken model instance
def create_jwttoken(access_token: str, refresh_token: str, user_id: models.User) -> auth_models.JWTToken:
    """Create user token to JWTToken model"""

    instance, _ = auth_models.JWTToken.objects.update_or_create(
        user_id=user_id,
        defaults={"access_token":access_token, "refresh_token":refresh_token, "created": datetime.now()}
    )

    return instance
