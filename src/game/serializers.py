import json

from rest_framework import serializers
from . import models, services
from ..user import serializers as user_serializers


class ShipSerializer(serializers.ModelSerializer):
    """Basic board serializer"""

    class Meta:
        model = models.Ship
        fields = ["id", "name", "plane", "size", "count"]
        extra_kwargs = {"board_id": {"read_only": True}}


class BoardSerializer(serializers.ModelSerializer):
    """Basic board serializer"""

    ships = ShipSerializer(many=True, read_only=True)

    class Meta:
        model = models.Board
        fields = ["id", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "is_ready", "is_my_turn", "is_play_again", 
                  "lobby_id", "user_id", "ships"]
        extra_kwargs = {"user_id": {"read_only": True}, "lobby_id": {"read_only": True}}

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for column_name, in services.column_name_list:
            ret[column_name] = json.loads(ret[column_name].replace("'", '"'))
        return ret


class MessageSerializer(serializers.ModelSerializer):
    """Basic message serializer"""

    class Meta:
        model = models.Message
        fields = ["message", "owner", "is_bot", "created_in"]


class ListLobbySerializer(serializers.HyperlinkedModelSerializer):
    """List lobby serializer"""

    users = user_serializers.BaseUserSerializer(many=True)

    class Meta:
        model = models.Lobby
        fields = ["url", "id", "name", "created_in", "bet", "password", "time_to_move", "time_to_placement", "slug", "users"]
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class CreateLobbySerializer(serializers.ModelSerializer):
    """Create lobby serializer"""

    class Meta:
        model = models.Lobby
        fields = ["name", "bet", "time_to_move", "time_to_placement", "password", "slug"]
        extra_kwargs = {
            "slug": {"read_only": True},
            "name": {"write_only": True},
            "bet": {"write_only": True},
            "time_to_move": {"write_only": True},
            "time_to_placement": {"write_only": True},
            "password": {"write_only": True},
        }


class RetrieveLobbySerializer(serializers.ModelSerializer):
    """Retrieve serializer"""

    users = user_serializers.BaseUserSerializer(many=True, read_only=True)
    boards = BoardSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True)

    class Meta:
        model = models.Lobby
        fields = ["id", "name", "bet", "winner", "password", "time_to_move", "time_to_placement", "users", "boards", "messages"]


class RetrieveLobbyWithUsersSerializer(serializers.ModelSerializer):
    """Retrieve serializer"""

    users = user_serializers.BaseUserSerializer(many=True, read_only=True)

    class Meta:
        model = models.Lobby
        fields = ["id", "name", "created_in", "bet", "password", "time_to_move", "time_to_placement", "slug", "users"]
