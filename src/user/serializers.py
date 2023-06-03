from rest_framework import serializers
from rest_framework.authtoken.models import Token

from . import models


class BaseUserSerializer(serializers.HyperlinkedModelSerializer):
    """Base user serializer"""

    class Meta:
        model = models.User
        fields = ("id", "username", "first_name", "last_name", "email")


class MyProfileSerializer(serializers.ModelSerializer):
    """Profile user serializer"""

    class Meta:
        model = models.User
        fields = ["id", "username", "first_name", "last_name", "email", "mobile_number", "cash", "rating",
                  "created_in", "updated_in", "photo"]
        extra_kwargs = {"cash": {"read_only": True}, "updated_in": {"read_only": True}}


class UserProfileSerializer(serializers.ModelSerializer):
    """Profile user serializer"""

    class Meta:
        model = models.User
        fields = ["username", "first_name", "last_name", "email", "mobile_number", "rating", "created_in", 
                  "updated_in", "photo"]


class UpdateUserPhotoSerializer(serializers.ModelSerializer):
    """Profile user serializer"""

    class Meta:
        model = models.User
        fields = ["photo"]


class UpdateUserInfoSerializer(serializers.ModelSerializer):
    """Profile user serializer"""

    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email", "mobile_number"]


class LoginRequestSerializer(serializers.Serializer):
    model = models.User

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class BaseTokenSerializer(serializers.ModelSerializer):
    """Base token serializer"""

    class Meta:
        model = Token
        fields = ["key", "user", "created"]
