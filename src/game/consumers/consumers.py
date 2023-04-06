import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import mixins, db_queries
from .. import services


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
                    mixins.RandomPlacementClearShipsMixin,
                    mixins.ChooseWhoWillShotFirstMixin,
                    mixins.DetermineWinnerMixin,
                    mixins.CountDownTimer,
                    mixins.AddUserToGame,
                    mixins.SendMessage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.lobby_group_name = None
        self.column_name_list = services.column_name_list
        self.string_number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.ship_count_tuple = (4, 3, 2, 1)

    async def connect(self):
        self.user = self.scope["user"]
        self.lobby_name = self.scope["url_route"]["kwargs"]["lobby_slug"]
        self.lobby_group_name = f"lobby_{self.lobby_name}"

        await self.channel_layer.group_add(self.lobby_group_name, self.channel_name)

        await self.accept()
    
    async def disconnect(self, close_code):
        if close_code is None:
            logging.info(msg="Websocket disconect.")
        elif close_code < 1002:
            logging.info(msg=f"Websocket disconect. Code - {close_code}")
        else: 
            logging.warning(msg=f"Emergency shutdown. Code - {close_code}")

        await self.channel_layer.group_discard(self.lobby_group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):

        if content["type"] == "refresh_board":
            await self.refresh(content["board_id"], content["ships"], content["board"])
            
        elif content["type"] == "drop_ship":
            await self.drop_ship(
                content["ship_id"], content["board_id"], content["ship_plane"], 
                content["ship_count"], content["field_name_list"], content["board"]
            )
        
        elif content["type"] == "take_shot":
            board, is_my_turn, enemy_ships = await self.take_shot(
                self.lobby_name, content["board_id"], content["field_name"]
            )
            data_1 = await self._countdown(self.lobby_name, content["time_to_turn"])
            data_2 = {"type": "send_shot", "board": board, "user_id": self.user.id, "is_my_turn": is_my_turn, 
                    "enemy_ships": enemy_ships}
            await self.channel_layer.group_send(self.lobby_group_name, data_2)
            await self.channel_layer.group_send(self.lobby_group_name, data_1)
        
        elif content["type"] == "is_ready_to_play":
            is_ready = await self.ready_to_play(content["board_id"], content["is_ready"], content["is_enemy_ready"])
            data = {"type": "is_ready_to_play", "is_ready": is_ready, "user_id": self.user.id}
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "random_placement":
            await self.random_placement_and_clear_ships(content["board_id"], content["board"], content["ships"])
        
        elif content["type"] == "who_starts":
            is_my_turn = await self.choose_first_shooter(self.lobby_name)

            if is_my_turn is not None:
                data = {"type": "who_starts", "is_my_turn": is_my_turn, "user_id": self.user.id}
                await self.channel_layer.group_send(self.lobby_group_name, data)
            else:
                logging.warning("Turn is determined!")

        elif content["type"] == "determine_winner":
            winner = await db_queries.get_user(content["enemy_id"]) if len(content) == 2 else self.user.username
            await self.determine_winner_of_game(self.lobby_name, winner)
            self.remove_lobby_from_redis(self.lobby_name)
            await self.channel_layer.group_send(self.lobby_group_name, {"type": "determine_winner", "winner": winner})

        elif content["type"] == "countdown":
            data = await self._countdown(self.lobby_name, content["time_to_turn"])
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "time_is_over":
            await self.random_placement_and_clear_ships(content["board_id"], content["board"], content["ships"])
            is_ready = await self.ready_to_play(content["board_id"], True, True)
            data = {"type": "is_ready_to_play", "is_ready": is_ready, "user_id": self.user.id}
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "add_user_to_game":
            user = await self._add_user_to_game(content["board_id"])
            await self.channel_layer.group_send(self.lobby_group_name, {"type": "add_user_to_game", "user": user})
        
        elif content["type"] == "send_message":
            data = await self._send_message(content["lobby_id"], content["message"])
            await self.channel_layer.group_send(self.lobby_group_name, data)

    async def send_shot(self, event):
        """Called when someone fires at an enemy board"""

        await self.send_json(event)
    
    async def is_ready_to_play(self, event):
        """Called when someone change ready to play field"""

        await self.send_json(event)
    
    async def who_starts(self, event):
        """Called when a player who shoots first is chosen"""

        await self.send_json(event)
    
    async def determine_winner(self, event):
        """Called when a player destroed all enemy ships"""

        await self.send_json(event)
    
    async def add_user_to_game(self, event):
        """Called when a add a user to lobby"""

        await self.send_json(event)
    
    async def countdown(self, event):
        """Called when a player destroed all enemy ships"""

        await self.send_json(event)
    
    async def send_message(self, event):
        """Called when a player sends a message to the chat"""

        await self.send_json(event)
