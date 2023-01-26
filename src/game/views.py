from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.reverse import reverse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from . import models as game_models, serializers
from ..user import models as user_models


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

    queryset = game_models.Lobby.objects.all().prefetch_related("users", "maps")
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RetrieveLobbySerializer
    lookup_field = "slug"


def index(request):
    lobby = game_models.Lobby.objects.first()
    user = user_models.User.objects.get(username="lanterman")
    return render(request, "index.html", {"lobby": lobby, "user1": user})
