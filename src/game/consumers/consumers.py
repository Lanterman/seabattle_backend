from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import mixins, services
from ...user.models import User


class LobbyListConsumer(AsyncJsonWebsocketConsumer):
    """Lobby list consumer"""

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        await self.send_json(content=content)


class LobbyConsumer(AsyncJsonWebsocketConsumer, mixins.RefreshBoardMixin, mixins.DropShipAddSpaceMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.column_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        self.scope["user"] = database_sync_to_async(User.objects.get)(id=content["user_id"])
        self.user = await self.scope["user"]

        if content["type"] == "refresh_board":
            cleared_board, field_name_list = await self.refresh_board(content["board"])
            column_dictionary = services.create_column_dict(self.column_name_list, cleared_board)
            await services.get_map(content["board_id"], column_dictionary)
            content = {"cleared_board": cleared_board, "field_name_list": field_name_list}

        elif content["type"] == "put_ship":
            put_ship = await self.put_ship_on_board(content["field_name_list"], content["ship_name"], self.column_name_list, content["board"])
            content = {"board": put_ship}
        
        await self.send_json(content=content)
