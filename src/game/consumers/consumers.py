from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import mixins, services
from ...user.models import User

import logging


class LobbyListConsumer(AsyncJsonWebsocketConsumer):
    """Lobby list consumer"""

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        await self.send_json(content=content)


class LobbyConsumer(AsyncJsonWebsocketConsumer, 
                    mixins.RefreshBoardMixin, 
                    mixins.DropShipAddSpaceMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.lobby_group_name = None
        self.column_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        self.ship_count_dict = (4, 3, 2, 1)

    async def connect(self):
        await self.accept()
    
    
    async def _drop_ship(
        self, plane: str, ship_name: str, field_name_list: list, board: list, board_id
    ) -> dict:
        """Drop ship on board"""

        self.drop_ship_on_board(field_name_list, ship_name, self.column_name_list, board)
        self.insert_space_around_ship(plane, field_name_list, self.column_name_list, board)
        column_dictionary = services.create_column_dict(self.column_name_list, board)
        await services.get_board(board_id, column_dictionary)
        
        return {"board": board}

    async def _refresh_board(self, board_id: int, board: list) -> dict:
        """Refresh user board"""

        cleared_board, field_name_list = self.refresh_board(board)
        column_dictionary = services.create_column_dict(self.column_name_list, cleared_board)
        await services.get_board(board_id, column_dictionary)

        return cleared_board, field_name_list
    
    async def _refresh_ships(self, board_id: int, ships: list) -> list:
        """"Refresh ships for current board"""

        ship_from_bd = await services.get_ships(board_id)
        await services.update_ships(ship_from_bd, self.ship_count_dict)
        refreshed_ships = [ship | {"plane": "horizontal", "count": count} for ship, count in zip(ships, self.ship_count_dict)]

        return refreshed_ships

    async def receive_json(self, content, **kwargs):
        self.scope["user"] = database_sync_to_async(User.objects.get)(id=content["user_id"])
        self.user = await self.scope["user"]

        if content["type"] == "refresh_board":
            cleared_board, field_name_list = await self._refresh_board(content["board_id"], content["board"])
            ships = await self._refresh_ships(content["board_id"], content["ships"])
            content = {"cleared_board": cleared_board, "field_name_list": field_name_list, "ships": ships}

        elif content["type"] == "put_ship":
            await self._drop_ship(
                content["plane"], content["ship_name"], content["field_name_list"], content["board"], content["board_id"]
            )
        
        await self.send_json(content=content)
