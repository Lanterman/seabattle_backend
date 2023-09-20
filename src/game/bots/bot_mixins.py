import os
import re
import logging
import random

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

    @staticmethod
    def bot_gets_ship_dict_on_the_board(board: dict) -> dict:
        """A bot gets ships on the board"""

        ship_dict = {}

        for column_value in board.values():
            for field_value in column_value.values():
                if type(field_value) == float:
                    field_value = int(field_value)
                    if field_value not in ship_dict:
                        ship_dict[field_value] = 1
                    else:
                        ship_dict[field_value] += 1

        return ship_dict
    
    @staticmethod
    def bot_gets_ship_size_and_name_list(ships: dict) -> dict:
        """A bot creates a list of ship sizes and their identifier in the tuple"""

        ship_size_and_name_list = []

        for ship_item in ships:
            ship_size_and_name_list.append((ship_item["size"], ship_item["id"]))
        
        return sorted(ship_size_and_name_list, reverse=True)


    @staticmethod
    def bot_selects_target(ship_dict_on_board: dict, ship_size_and_name_list: dict) -> tuple:
        """Bot selects the best a target"""

        for ship_size, ship_id in ship_size_and_name_list:
            if ship_id in ship_dict_on_board and ship_dict_on_board[ship_id] > 0:
                return ship_size 

    @staticmethod
    def bot_get_field_list(field_dict: dict, board: dict, column_name_list: list, max_index: int) -> None:
        """Get a list of valid fields for a shot """

        index = max_index - 1 if max_index > 1 else 1
        for char in column_name_list[::-1]:
            index = index if index <= max_index else 1
            for num in range(index, 11, max_index):
                if board[char][f"{char}{num}"] not in ("hit", "miss"):
                    type_to_shot = "hit" if type(board[char][f"{char}{num}"]) == float else "miss"
                    field_dict[f"{char}{num}"] = type_to_shot

            index += 1


    async def bot_take_shot(self, lobby_slug: str, board_id: int, time_to_turn: int, ships: dict) -> tuple:
        board = await ws_db_queries.get_board(board_id, self.column_name_list)
        ws_services.confert_to_json(board)
        ship_dict_on_board = self.bot_gets_ship_dict_on_the_board(board)
        ship_size_and_name_list = self.bot_gets_ship_size_and_name_list(ships)
        max_index = self.bot_selects_target(ship_dict_on_board, ship_size_and_name_list)

        field_dict = {}
        self.bot_get_field_list(field_dict, board, self.column_name_list, max_index)

        while True:
            random_shot = random.choice(list(field_dict))
            field_dict = {random_shot: field_dict[random_shot]}
            output_data = {"type": "bot_taken_to_shot", "field_dict": field_dict}

            if field_dict[random_shot] == "miss":
                output_data["is_bot_hitted"] = False
                await self.send_json(content=output_data)
                break
            logging.info(field_dict)
            await self.send_json(content=output_data)



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