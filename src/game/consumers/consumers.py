from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import mixins
from ...user.models import User


class LobbyListConsumer(AsyncJsonWebsocketConsumer):
    """Lobby list consumer"""

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        await self.send_json(content=content)


class LobbyConsumer(AsyncJsonWebsocketConsumer, mixins.RefreshBoard):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        self.scope["user"] = database_sync_to_async(User.objects.get)(id=content["user_id"])
        self.user = await self.scope["user"]

        if content["type"] == "refresh_board":
            cleared_board, field_name_list = await self.refresh_board(content["board_id"], content["board"])
        await self.send_json(content={"cleared_board": cleared_board, "field_name_list": field_name_list})
