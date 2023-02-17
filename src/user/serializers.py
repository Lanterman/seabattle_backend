from rest_framework import serializers
from rest_framework.authtoken.models import Token

from . import models


class BaseUserSerializer(serializers.HyperlinkedModelSerializer):
    """Base user serializer"""

    class Meta:
        model = models.User
        fields = ("id", "username", "first_name", "last_name", "email", "slug")
        # extra_kwargs = {"url": {"lookup_field": "slug"}}


class ProfileSerializer(serializers.ModelSerializer):
    """Profile user serializer"""

    class Meta:
        model = models.User
        fields = ["id", "username", "slug", "first_name", "last_name", "email", "mobile_number", "cash", 
                  "created_in", "updated_in", "photo"]


class LoginRequestSerializer(serializers.Serializer):
    model = models.User

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class BaseTokenSerializer(serializers.ModelSerializer):
    """Base token serializer"""

    class Meta:
        model = Token
        fields = ["key", "user", "created"]
