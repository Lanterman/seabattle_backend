from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import mixins
from ...user.models import User

import logging
from datetime import datetime


class LobbyListConsumer(AsyncJsonWebsocketConsumer):
    """Lobby list consumer"""

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        await self.send_json(content=content)


class LobbyConsumer(AsyncJsonWebsocketConsumer, 
                    mixins.RefreshBoardShipsMixin, 
                    mixins.DropShipAddSpaceMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.lobby_group_name = None
        self.column_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        self.ship_count_tuple = (4, 3, 2, 1)

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        self.scope["user"] = database_sync_to_async(User.objects.get)(id=content["user_id"])
        self.user = await self.scope["user"]

        if content["type"] == "refresh_board":
            await self.refresh(content["board_id"], content["ships"], content["board"])
            
        elif content["type"] == "drop_ship":
            await self.update_board(
                content["ship_id"], content["board_id"], content["ship_plane"], 
                content["ship_count"], content["field_name_list"], content["board"]
            )
