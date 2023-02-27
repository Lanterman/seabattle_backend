import logging

from datetime import datetime
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import mixins
from ..services import column_name_list


class LobbyListConsumer(AsyncJsonWebsocketConsumer):
    """Lobby list consumer"""

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        await self.send_json(content=content)


class LobbyConsumer(AsyncJsonWebsocketConsumer, 
                    mixins.RefreshBoardShipsMixin, 
                    mixins.DropShipAddSpaceMixin,
                    mixins.TakeShotMixin,
                    mixins.IsReadyToPlayMixin,
                    mixins.RandomPlacementClearShipsMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.lobby_group_name = None
        self.column_name_list = column_name_list
        self.string_number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.ship_count_tuple = (4, 3, 2, 1)

    async def connect(self):
        self.user = self.scope["user"]
        self.lobby_name = self.scope["url_route"]["kwargs"]["lobby_slug"]
        self.lobby_group_name = f"lobby_{self.lobby_name}"

        await self.channel_layer.group_add(self.lobby_group_name, self.channel_name)

        await self.accept()

    async def receive_json(self, content, **kwargs):

        if content["type"] == "refresh_board":
            await self.refresh(content["board_id"], content["ships"], content["board"])
            
        elif content["type"] == "drop_ship":
            await self.drop_ship(
                content["ship_id"], content["board_id"], content["ship_plane"], 
                content["ship_count"], content["field_name_list"], content["board"]
            )
        
        elif content["type"] == "take_shot":
            board = await self.take_shot(content["board_id"], content["field_name"])
            data = {"type": "send_shot", "board": board, "user_id": self.user.id}
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "is_ready_to_play":
            is_ready = await self.ready_to_play(content["board_id"], content["is_ready"])
            data = {"type": "is_ready_to_play", "is_ready": is_ready, "user_id": self.user.id}
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "random_placement":
            await self.random_placement_and_clear_ships(content["board_id"], content["board"], content["ships"])

    async def send_shot(self, event):
        """Called when someone fires at an enemy board"""

        await self.send_json(event)
    
    async def is_ready_to_play(self, event):
        """Called when someone change ready to play field"""

        await self.send_json(event)
