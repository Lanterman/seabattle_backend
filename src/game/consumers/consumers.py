import random
import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from ..bots import bot_interfaces

from config.utilities import redis_instance
from . import mixins, db_queries
from .. import services


class MainConsumer(AsyncJsonWebsocketConsumer, mixins.CreateNewGameMixin):
    """Main consumer"""

    async def connect(self):
        self.lobby_group_name = "lobby_list"
        await self.channel_layer.group_add(self.lobby_group_name, self.channel_name)
        # redis_instance.flushall()
        # logging.warning(redis_instance.keys())

        await self.accept()

    async def receive_json(self, content, **kwargs):
        if content["type"] == "created_game":
            lobby = await self.get_new_game(content["lobby_slug"])
            data = {"type": content["type"], "lobby": lobby, "user_id": self.scope["user"].id}
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "deleted_game":
            await self.channel_layer.group_send(self.lobby_group_name, content)
        
        elif content["type"] == "add_user_to_game":
            data = {"type": content["type"], "lobby_id": content["lobby_id"], "user_id": self.scope["user"].id}
            await self.channel_layer.group_send(self.lobby_group_name, data)
    
    async def created_game(self, event):
        """Called when created new game"""

        if self.scope["user"].id != event["user_id"]:
            logging.info("sent 'created_game' message")
            await self.send_json(event)
    
    async def deleted_game(self, event):
        """Called when deleted game"""

        logging.info("sent 'deleted_game' message")
        await self.send_json(event)
    
    async def add_user_to_game(self, event):
        """Called when added user to game"""

        if self.scope["user"].id != event["user_id"]:
            logging.info("sent 'add_user_to_game' message")
            await self.send_json(event)


class LobbyConsumer(AsyncJsonWebsocketConsumer, 
                    mixins.RefreshBoardShipsMixin, 
                    mixins.DropShipAddSpaceMixin,
                    mixins.TakeShotMixin,
                    mixins.IsReadyToPlayMixin,
                    mixins.RandomPlacementClearShipsMixin,
                    mixins.ChooseWhoWillShotFirstMixin,
                    mixins.DetermineWinnerMixin,
                    mixins.CountDownTimerMixin,
                    mixins.AddUserToGameMixin,
                    mixins.SendMessageMixin,
                    mixins.PlayAgainMixin,
                    mixins.CreateNewGameMixin,
                    mixins.CalculateRatingAndCash,
                    
                    # Add a bot
                    bot_interfaces.GenericBotInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.lobby_group_name = None
        self.column_name_list = services.column_name_list
        self.string_number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.ship_count_dict = services.ship_count_dict  

    async def connect(self):
        self.user = self.scope["user"]
        self.lobby_name = self.scope["url_route"]["kwargs"]["lobby_slug"]
        self.lobby_group_name = f"lobby_{self.lobby_name}"
        # redis_instance.flushall()
        # logging.warning(redis_instance.keys())
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
        
        # A bot makes to shot
        elif content["type"] == "bot_take_to_shot":
            await self.bot_take_shot(
                self.user, content["lobby_id"], self.lobby_name, content["board_id"], content["time_to_turn"], 
                content["last_hit"], content["ships"], self.column_name_list, content["bot_level"]
            )

        elif content["type"] == "take_shot":
            is_my_turn, field_name_dict, enemy_ships = await self.take_shot(
                self.lobby_name, content["board_id"], content["field_name"]
            )
            countdown = await self._countdown(self.lobby_name, content["time_to_turn"])
            data = {"type": "send_shot", "field_name_dict": field_name_dict, "user_id": self.user.id, 
                      "is_my_turn": is_my_turn, "enemy_ships": enemy_ships, "time_left": countdown["time_left"]}
            
            if content["bot_level"] and random.randrange(0, 2) == 1:
                bot_message = self.get_bot_message_with_user_action(content["bot_level"], field_name_dict)
                if bot_message:
                    dict_message = await self._send_message(content["lobby_id"], bot_message, True)
                    data["bot_message"] =  dict_message["message"]
            
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "is_ready_to_play":
            is_ready = await self._is_ready_to_play(content["board_id"], content["is_ready"], content["is_enemy_ready"])
            data = {
                "type": "is_ready_to_play", 
                "is_ready": is_ready, 
                "user_id": self.user.id, 
                "board_id": content["board_id"],
            }
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "random_placement":
            await self.random_placement_and_clear_ships(content["board_id"], content["board"], content["ships"])
        
        elif content["type"] == "who_starts":
            is_my_turn = await self.choose_first_shooter(self.lobby_name)

            if is_my_turn is not None:
                data = {"type": "who_starts", "is_my_turn": is_my_turn, "user_id": self.user.id}
                await self.channel_layer.group_send(self.lobby_group_name, data)
            else:
                logging.info(f"For lobby '{self.lobby_name}' turn is determined!")

        elif content["type"] == "determine_winner":
            winner = await self.detemine_winner_name(content["user_id"], content["is_bot"])
            data = {"winner": winner}

            if content["is_bot"]:
                _mthd = self.get_bot_message_user_won if winner == self.user.username else self.get_bot_message_bot_won
                bot_message = _mthd(content["is_bot"])
                dict_message = await self._send_message(content["lobby_id"], bot_message, True)
                data["bot_message"] =  dict_message["message"]

            await self.determine_winner_of_game(self.lobby_name, data["winner"])

            if not content["is_bot"]:
                await self.calculate_rating_and_cash_of_game(winner, content["bet"])
            
            self.remove_current_turn_in_lobby_from_redis(self.lobby_name)
            await self.channel_layer.group_send(self.lobby_group_name, {"type": "determine_winner", "winner": winner})

        elif content["type"] == "countdown":
            data = await self._countdown(self.lobby_name, content["time_to_turn"])
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "time_is_over":
            await self.random_placement_and_clear_ships(
                content["board_id"], content["board"], content["ships"], content["bot_level"]
            )
            is_ready = await self._is_ready_to_play(content["board_id"], True, True)
            data = {
                "type": "is_ready_to_play", 
                "is_ready": is_ready, 
                "user_id": self.user.id, 
                "board_id": content["board_id"],
            }
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "add_user_to_game":
            user = await self._add_user_to_game(content["board_id"])
            data = {"type": "add_user_to_game", "user": user}

            if user:
                message = self.get_bot_message_with_connected_player(self.user.username)
                dict_message = await self._send_message(content["lobby_id"], message, True)
                data["message"] = dict_message["message"]
            
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "send_message":
            data = await self._send_message(content["lobby_id"], content["message"])
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "is_play_again":
            message = self.get_bot_message_with_offer(content["answer"], self.user.username)
            dict_message = await self._send_message(content["lobby_id"], message, True)
            dict_answer = {"type": "is_play_again", "is_play_again": content["answer"], "user_id": self.user.id, 
                           "message": dict_message["message"]}

            await self.preform_update_play_again_field(content["board_id"], content["answer"])
            await self.channel_layer.group_send(self.lobby_group_name, dict_answer)       

        elif content["type"] == "create_new_game":
            if content["is_bot"]:
                lobby_slug = await self.bot_creates_new_game(content["name"], content["bet"], content["time_to_move"],
                                                             content["time_to_placement"], self.user, content["is_bot"])
                data = {"type": "new_group", "lobby_slug": lobby_slug}
            elif self.user.cash - int(content["bet"]) >= int(content["bet"]):
                lobby_slug = await self.create_new_game(content["bet"], content["name"], content["time_to_move"],
                                                        content["time_to_placement"], content["enemy_id"])
                data = {"type": "new_group", "lobby_slug": lobby_slug}
            
            else:
                message = self.get_bot_message_dont_have_enough_money(self.user.username)
                data = await self._send_message(content["lobby_id"], message, True)
            
            await self.channel_layer.group_send(self.lobby_group_name, data)
        
        elif content["type"] == "delete_game":
            await db_queries.delete_lobby(self.lobby_name)
            redis_instance.delete(self.lobby_name)

    async def send_shot(self, event):
        """Called when someone fires at an enemy board"""

        logging.info("sent 'send_shot' message")
        await self.send_json(event)
    
    async def is_ready_to_play(self, event):
        """Called when someone change ready to play field"""

        logging.info("sent 'is_ready_to_play' message")
        await self.send_json(event)
    
    async def who_starts(self, event):
        """Called when a player who shoots first is chosen"""

        logging.info("sent 'who_starts' message")
        await self.send_json(event)
    
    async def determine_winner(self, event):
        """Called when a player destroed all enemy ships"""

        logging.info("sent 'determine_winner' message")
        await self.send_json(event)
    
    async def add_user_to_game(self, event):
        """Called when a add a user to lobby"""

        logging.info("sent 'add_user_to_game' message")
        await self.send_json(event)
    
    async def countdown(self, event):
        """Called when a player destroed all enemy ships"""

        logging.info("sent 'countdown' message")
        await self.send_json(event)
    
    async def send_message(self, event):
        """Called when a player sends a message to the chat"""

        logging.info("sent 'send_message' message")
        await self.send_json(event)
    
    async def is_play_again(self, event):
        """Called when someone decides whether to play again"""

        logging.info("sent 'is_play_again' message")
        await self.send_json(event)
    
    async def new_group(self, event):
        """Called when players want to play again"""

        logging.info("sent 'new_group' message")
        await self.send_json(event)
