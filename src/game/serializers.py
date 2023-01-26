from rest_framework import serializers
from . import models
from ..user import serializers as user_serializers


class MapSerializer(serializers.ModelSerializer):
    """Basic map serializer"""

    class Meta:
        model = models.Map
        fields = ["id", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "lobby_id", "user_id"]
        extra_kwargs = {"user_id": {"read_only": True}, "lobby_id": {"read_only": True}}


class ListLobbySerializer(serializers.HyperlinkedModelSerializer):
    """List lobby serializer"""

    users = user_serializers.BaseUserSerializer(many=True)

    class Meta:
        model = models.Lobby
        fields = ["url", "name", "created_in", "bet", "password", "time_to_move", "users", "slug"]
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class CreateLobbySerializer(serializers.ModelSerializer):
    """Lobby serializer"""

    class Meta:
        model = models.Lobby
        fields = ["name", "bet", "time_to_move", "password", "slug"]
        extra_kwargs = {"slug": {"read_only": True}}

    def create(self, validated_data):
        return super().create(validated_data)


class RetrieveLobbySerializer(serializers.ModelSerializer):
    """Retrieve serializer"""

    users = user_serializers.BaseUserSerializer(many=True, read_only=True)
    maps = MapSerializer(many=True, read_only=True)

    class Meta:
        model = models.Lobby
        fields = ["name", "created_in", "bet", "password", "time_to_move", "users", "maps"]
