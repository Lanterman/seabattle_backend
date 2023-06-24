from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

from . import models


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

    models.SecretKey.objects.create(secret_key=secret_key, user=user_id)


def delete_user_secret_key(user_id: int) -> None:
    """Delete user secret key from SecretKey model"""

    models.SecretKey.objects.filter(user=user_id).delete()


# action with JWTToken model instance
def create_user_token(token: str, user) -> None:
    """Create user token to JWTToken model"""

    delete_user_token(user.id)

    return Token.objects.create(user=user)


def delete_user_token(user_id: int) -> None:
    """Delete user token from JWTToken model"""

    Token.objects.filter(user=user_id).delete()