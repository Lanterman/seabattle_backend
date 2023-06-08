from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

from . import models


def get_or_none(username) -> models.User or None:
    """If user model instance exists, return it, otherwise return None"""

    try:
        query = models.User.objects.get(username=username)
    except ObjectDoesNotExist:
        query = None

    return query


def get_user_by_username(username: str):
    """Get user by username""" 

    query = get_or_none(username)
    return query


def create_user_token(user: models.User) -> Token:
    """Create user token"""

    query, _ = Token.objects.get_or_create(user=user)
    return query