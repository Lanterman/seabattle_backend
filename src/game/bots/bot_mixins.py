import os
import re
import logging

from channels.db import database_sync_to_async

from . import db_queries
from .. import db_queries as game_queries
from src.game.consumers import services as ws_services, db_queries as ws_db_queries
from config.utilities import redis_instance


class BotMessage:
    """Mixin that generates message from the bot"""

    def get_bot_message_with_offer(self, answer: bool) -> str:
        """Get a bot message with a response to the offer to play again"""
   
        if answer:
            return f"{self.user.username.capitalize()} want to play again."
        else:
            return f"{self.user.username.capitalize()} doesn't want to play again."
    
    def get_bot_message_with_connected_player(self) -> str:
        """Get a message from a bot with a connected player"""

        return f"{self.user.username.capitalize()} connected to the game."
    
    def get_bot_message_dont_have_enough_money(self) -> str:
        """Get a message about don't have enough money to play"""

        return f"{self.user.username.capitalize()} don't have enough money to play."


class BotTakeShot:
    """A bot take shot"""

    async def bot_take_shot(self, lobby_slug: str, board_id: int, field_name: str) -> tuple:
        board = await ws_db_queries.get_board(board_id, self.column_name_list)
        ws_services.confert_to_json(board)
        type_to_shot = "hit" if type(board["C"]["C1"]) == float else "miss"
        board["C"]["C1"] = type_to_shot
        await self.send_json(content={"type": "bot_taken_to_shot", "field_name_dict": {"C1": type_to_shot}})
        # shot_type = self._get_type_shot(board, field_name)
        # field_value = self._shot(board, field_name, shot_type)
        # is_my_turn = True if shot_type == "hit" else False
        # number_of_enemy_ships, field_name_dict = None, {field_name: shot_type}

        # if is_my_turn:
        #     if self._is_ship_has_sunk(field_value, board):
        #         field_name_dict.update(self._add_misses_around_sunken_ship(field_value, board))
        #         number_of_enemy_ships = ws_services.determine_number_of_enemy_ships(board)
        # else: 
        #     await self.hand_over_to_the_enemy(lobby_slug)

        # redis_instance.hdel(lobby_slug, "is_running")

        # await self.perform_write_shot(board_id, board)
        # return is_my_turn, field_name_dict, number_of_enemy_ships


class BotCreatesNewGame:
    """A bot creates a new game with its own options"""

    @staticmethod
    def _bot_creates_new_name(name: str) -> str:
        """Create new name of lobby"""

        default_name_of_game = os.getenv("DOC_DEFAULT_NAME_OF_THE_GAME", os.environ["DEFAULT_NAME_OF_THE_GAME"])

        if name[:len(default_name_of_game)] != default_name_of_game:
            return f"{default_name_of_game} (1)"
        
        repeat_number = re.search(r"[\d]+", name[len(default_name_of_game):])
        return f"{default_name_of_game} ({int(repeat_number.group()) + 1})"

    async def bot_creates_new_game(self, name: str, bet: int, time_to_move: int, time_to_placement: int) -> str:
        new_name = self._bot_creates_new_name(name)
        lobby_id, lobby_slug = await db_queries.create_lobby(new_name, bet, time_to_move, time_to_placement, self.user)
        first_board_id, second_board_id = await database_sync_to_async(game_queries.create_lobby_boards)(lobby_id, self.user.id)
        await database_sync_to_async(game_queries.create_ships_for_boards)(first_board_id, second_board_id)
        return str(lobby_slug)


class GenericBotMixin(BotMessage, BotTakeShot, BotCreatesNewGame):
    """Interface class for all other bot mixins"""