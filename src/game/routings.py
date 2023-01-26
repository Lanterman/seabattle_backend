from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path("ws/lobbies/", consumers.LobbyListConsumer.as_asgi()),
    re_path(r"ws/lobby/(?P<lobby_slug>\w+)/", consumers.LobbyConsumer.as_asgi()),
]
