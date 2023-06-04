from rest_framework import serializers
from rest_framework.authtoken.models import Token

from . import models


class BaseUserSerializer(serializers.HyperlinkedModelSerializer):
    """Base user serializer"""

    class Meta:
        model = models.User
        fields = ("id", "username", "first_name", "last_name", "email", "rating")


class MyProfileSerializer(serializers.ModelSerializer):
    """Profile user serializer"""

    class Meta:
        model = models.User
        fields = ["id", "username", "first_name", "last_name", "email", "mobile_number", "cash", "rating",
                  "created_in", "updated_in", "photo"]
        extra_kwargs = {"cash": {"read_only": True}, "rating": {"read_only": True}, "updated_in": {"read_only": True}}


class EnemyProfileSerializer(serializers.ModelSerializer):
    """Profile user serializer"""

    class Meta:
        model = models.User
        fields = ["username", "first_name", "last_name", "email", "mobile_number", "rating", "created_in", 
                  "updated_in", "photo"]
        extra_kwargs = {"rating": {"read_only": True}, "updated_in": {"read_only": True}}


class UpdateUserPhotoSerializer(serializers.ModelSerializer):
    """Profile user serializer"""

    class Meta:
        model = models.User
        fields = ["photo"]
    
    def validate_photo(self, value):
        if value.name.split(".")[-1] not in ["jpeg", "jpg", "png", "ico"]:
            raise serializers.ValidationError('Only JPEG, PNG, ICO files are accepted!!')
        return value


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
