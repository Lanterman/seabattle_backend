from rest_framework import serializers
from . import models


class BaseUserSerializer(serializers.HyperlinkedModelSerializer):
    """Base user serializer"""

    class Meta:
        model = models.User
        fields = ("username", "first_name", "last_name", "slug")
        # extra_kwargs = {"url": {"lookup_field": "slug"}}


class ProfileSerializer(serializers.ModelSerializer):
    """Profile user serializer"""

    class Meta:
        model = models.User
        fields = ["id", "username", "slug"]
