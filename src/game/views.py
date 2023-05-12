import uuid

from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from . import models as game_models, serializers, services, permissions, db_queries
from config.utilities import redis_instance


class LobbyListView(ListCreateAPIView):
    """List of lobbies and create lobby"""

    queryset = game_models.Lobby.objects.all().prefetch_related("users")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ListLobbySerializer
        else:
            return serializers.CreateLobbySerializer

    def perform_create(self, serializer):
        lobby = serializer.save()
        lobby.users.add(self.request.user)
        first_board_id, second_board_id = db_queries.create_lobby_boards(lobby.id, self.request.user.id)
        db_queries.create_ships_for_boards(first_board_id, second_board_id)


class DetailLobbyView(RetrieveAPIView):
    """Detailed description of the lobby, update and destroy lobby"""

    queryset = game_models.Lobby.objects.all().prefetch_related("users", "boards", "boards__ships", "messages")
    permission_classes = [IsAuthenticated, permissions.IsLobbyFree]
    serializer_class = serializers.RetrieveLobbySerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance).data
        index, enemy_board = services.clear_enemy_board(request.user, serializer["boards"])
        serializer["boards"][index] = enemy_board

        if not serializer["winner"]:
            serializer["time_left"] = self.add_countdown(self.kwargs["slug"], serializer)

        headers = {"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"}
        return Response(serializer, headers=headers)

    def add_countdown(self, slug: uuid, data: dict) -> int:
        """Add time_left variable with countdown"""

        if data["boards"][0]["is_ready"] and data["boards"][1]["is_ready"]:
            return self.get_time_left(slug, redis_instance.hget(slug, "time_left"), data["time_to_move"])
        else:
            return self.get_time_left(slug, redis_instance.hget(slug, "time_left"), data["time_to_placement"])

    @staticmethod
    def get_time_left(slug: uuid, time_from_redis: str, time_to_serializer: int) -> int:
        """Get a time left to placement ships or make a turn"""

        if not time_from_redis:
            redis_instance.hset(name=slug, mapping={"time_left": time_to_serializer, "current_turn": 0})
            return time_to_serializer
        return int(time_from_redis)
