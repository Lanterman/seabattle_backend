from uuid import uuid4
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.decorators import action

from . import models, serializers


class LobbyListConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    """Lobby list consumer"""


class LobbyConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = models.Lobby.objects.all()
    serializer_class = serializers.CreateLobbySerializer
    lookup_field = "slug"

    @database_sync_to_async
    def create_me(self, name, bet):
        lobby = models.Lobby.objects.create(name=name, bet=bet, slug=uuid4(), finished_in="2022-12-30 17:37:38.895446+00")
        return lobby

    @database_sync_to_async
    def get_lobby(self, lobby_id):
        return models.Lobby.objects.get(id=lobby_id)

    @action()
    async def create_lobby(self, name, bet, **kwargs):
        lobby = await self.create_me(name, bet)
        print(lobby)
        return lobby

    @action()
    async def async_cons(self, lobby_id, **kwargs):
        lobby = await self.get_lobby(lobby_id)
        print(lobby)
        await self.send_json({"qwe": 123})
