import uuid

from django.http import HttpResponseRedirect
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from . import models as game_models, serializers, services, permissions
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

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs).data
        return HttpResponseRedirect(redirect_to=reverse(viewname="lobby-detail", kwargs={"slug": data["slug"]}))


class DetailLobbyView(RetrieveUpdateDestroyAPIView):
    """Detailed description of the lobby, update and destroy lobby"""

    queryset = game_models.Lobby.objects.all().prefetch_related("users", "boards", "boards__ships")
    permission_classes = [IsAuthenticated, permissions.IsLobbyFree]
    serializer_class = serializers.RetrieveLobbySerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance).data
        index, enemy_board = services.clear_enemy_board(request.user, serializer["boards"])
        serializer["boards"][index] = enemy_board
        serializer["time_left"] = self.add_countdown(self.kwargs["slug"], serializer)
        return Response(serializer)

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
            redis_instance.hmset(slug, {"time_left": time_to_serializer, "current_turn": 0})
            return time_to_serializer
        return int(time_from_redis)
