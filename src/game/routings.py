from django.urls import path
from .consumers import consumers

websocket_urlpatterns = [
    path("ws/main/", consumers.MainConsumer.as_asgi()),
    path(r"ws/lobby/<lobby_slug>/", consumers.LobbyConsumer.as_asgi()),
]
