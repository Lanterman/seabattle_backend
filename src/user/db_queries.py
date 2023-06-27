from datetime import datetime
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

from . import models
from .auth import models as auth_models


def get_or_none(username: str) -> models.User or None:
    """If model instance exists, return it, otherwise return None"""

    try:
        query = models.User.objects.get(username=username)
    except models.User.DoesNotExist:
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
def get_jwttoken_instance_by_refresh_token(refresh_token: str) -> auth_models.JWTToken or None:
    """Get a JWTToken model instance or None"""

    try:
        return auth_models.JWTToken.objects.get(refresh_token=refresh_token)
    except auth_models.JWTToken.DoesNotExist:
        raise exceptions.ValidationError(_('Invalid refresh token.'))


def create_jwttoken(access_token: str, refresh_token: str, user_id: int) -> auth_models.JWTToken:
    """Create user token to JWTToken model"""

    instance, _ = auth_models.JWTToken.objects.update_or_create(
        user_id=user_id,
        defaults={"access_token":access_token, "refresh_token":refresh_token, "created": datetime.now()}
    )

    return instance
