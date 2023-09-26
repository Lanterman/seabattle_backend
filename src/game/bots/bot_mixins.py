import os
import re
import asyncio
import logging
import random

from channels.db import database_sync_to_async

from . import db_queries
from .. import db_queries as game_queries
from src.game.consumers import services as ws_services, db_queries as ws_db_queries


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
        """
        A bot gets ships on the board. 
        Return a following dictionary:
            {<ship_id>.<serial number of a ship of this type>: <number of fields it stands on>}.
        """

        ship_dict = {}

        for column_value in board.values():
            for field_value in column_value.values():
                if type(field_value) == float:
                    if field_value not in ship_dict:
                        ship_dict[field_value] = 1
                    else:
                        ship_dict[field_value] += 1

        return ship_dict
    
    @staticmethod
    def bot_gets_ship_size_and_name_list(ships: dict) -> dict:
        """A bot creates a sorted list of ship sizes and their identifier in the tuple."""

        ship_size_and_name_list = []

        for ship_item in ships:
            ship_size_and_name_list.append((ship_item["size"], ship_item["id"]))
        
        return sorted(ship_size_and_name_list, reverse=True)


    @staticmethod
    def bot_selects_target(ship_dict_on_board: dict, ship_size_and_name_list: dict) -> tuple:
        """Bot selects the best a target"""

        ship_id_list = set(int(ship_id) for ship_id in ship_dict_on_board)

        for ship_size, ship_id in ship_size_and_name_list:
            if ship_id in ship_id_list:
                return ship_size 

    @staticmethod
    def bot_get_field_list(field_dict: dict, board: dict, column_name_list: list, max_index: int) -> None:
        """Get a list of valid fields for a shot """

        index = max_index - 1 if max_index > 1 else 1
        for char in column_name_list[::-1]:
            index = index if index <= max_index else 1
            for num in range(index, 11, max_index):
                _field = f"{char}{num}"
                if board[char][_field] not in ("hit", "miss"):
                    field_dict[_field] = board[char][_field]

            index += 1
    
    @staticmethod
    def bot_defines_plane(field: str, board: dict, column_name_list: list) -> str or None:
        """A bot defines plane (horizontal or vertical)"""

        f_name = field[0]
        f_num = int(field[1:])
        f_index = column_name_list.index(f_name)
        if ((f_num > 1 and board[f_name][f"{f_name}{f_num - 1}"] == "hit") or 
            (f_num < 10 and board[f_name][f"{f_name}{f_num + 1}"] == "hit")):
            return "vertical"
        elif ((f_index > 0 and board[column_name_list[f_index - 1]][f"{column_name_list[f_index - 1]}{f_num}"] == "hit") or
              (f_index < 9 and board[column_name_list[f_index + 1]][f"{column_name_list[f_index + 1]}{f_num}"] == "hit")):
            return "horizontal"
    
    def botEasy_gets_fields_around_hit(self, random_shot: str, board: dict, column_name_list: list) -> dict:
        """A easy bot receives fields around the board"""

        field_dict = {}
        field_number = int(random_shot[1:])
        column_name = random_shot[0]
        column_index = column_name_list.index(column_name)

        plane = self.bot_defines_plane(random_shot, board, column_name_list)

        if not plane:
            field = f"{column_name}{field_number - 1}"
            if field_number > 1 and board[column_name][field] not in ("hit", "miss"):
                field_dict[field] = board[column_name][field]
            
            field = f"{column_name}{field_number + 1}"
            if field_number < 10 and board[column_name][field] not in ("hit", "miss"):
                field_dict[field] = board[column_name][field]
            
            if column_index > 0:
                _column_name = column_name_list[column_index - 1]
                _field = f"{_column_name}{field_number}"
                if board[_column_name][_field] not in ("hit", "miss"):
                    field_dict[_field] = board[_column_name][_field]
            
            if column_index < 9:
                _column_name = column_name_list[column_index + 1]
                _field = f"{_column_name}{field_number}"
                if board[_column_name][_field] not in ("hit", "miss"):
                    field_dict[_field] = board[_column_name][_field]
        
        elif plane == "vertical":
            for top_num in range(field_number - 1, 0, -1):
                _field = f"{column_name}{top_num}"
                _field_value = board[column_name][_field]

                if _field_value == "miss":
                    break

                if _field_value != "hit":
                    field_dict[_field] = board[column_name][_field]
                    break
            
            for bottom_num in range(field_number + 1, 11):
                _field = f"{column_name}{bottom_num}"
                _field_value = board[column_name][_field]

                if _field_value == "miss":
                    break

                if _field_value != "hit":
                    field_dict[_field] = board[column_name][_field]
                    break

        elif plane == "horizontal":
            if column_index > 0:
                for left_column_name in column_name_list[column_index - 1::-1]:
                    _field_value = board[left_column_name][f"{left_column_name}{field_number}"]

                    if _field_value == "miss":
                        break

                    if _field_value != "hit":
                        _field = f"{left_column_name}{field_number}"
                        field_dict[_field] = board[left_column_name][_field]
                        break
            
            if column_index < 9:
                for right_column_name in column_name_list[column_index + 1::]:
                    _field_value = board[right_column_name][f"{right_column_name}{field_number}"]
                    
                    if _field_value == "miss":
                        break

                    if _field_value != "hit":
                        _field = f"{right_column_name}{field_number}"
                        field_dict[_field] = board[right_column_name][_field]
                        break

        return field_dict
    
    async def bot_passes_move_to_user(self, lobby_slug: str) -> None:
        boards = await self.get_lobby_boards(lobby_slug)
        my_board, enemy_board = await self.determine_whoose_boards(boards)
        await self.perform_update_boards(True, my_board, enemy_board)

    async def bot_take_shot(
            self, lobby_slug: str, board_id: int, time_to_turn: int, ships: dict, column_name_list: list
        ) -> tuple:
        """A bot shooting logic. A bot's shooting cycle will end on a first miss"""

        board = await ws_db_queries.get_board(board_id, column_name_list)

        ws_services.confert_to_json(board)

        ship_dict_on_board = self.bot_gets_ship_dict_on_the_board(board)
        ship_size_and_name_list = self.bot_gets_ship_size_and_name_list(ships)
        max_index = self.bot_selects_target(ship_dict_on_board, ship_size_and_name_list)

        field_dict = {}
        self.bot_get_field_list(field_dict, board, column_name_list, max_index)
        # Сделать обстрел полей возле места попадания, если потом бот промазал - сохранять этот список
        # Если уничтожен корабль, проверять надо ли меня диапазон выстрелов
        # Удалять redis_instance.hdel(lobby_slug, "is_running") хз зачем
        while True:
            # Обновляем время хода
            countdown = await self._countdown(self.lobby_name, time_to_turn)

            random_shot = random.choice(list(field_dict))
            type_to_shot = "hit" if type(board[random_shot[0]][random_shot]) == float else "miss"
            fields = {random_shot: type_to_shot}
            output_data = {
                "type": "bot_taken_to_shot", 
                "field_dict": fields, 
                "is_my_turn": False, 
                "time_left": countdown["time_left"]
            }
            logging.info(random_shot)
            if type_to_shot == "miss":
                output_data["is_my_turn"] = True
                board[random_shot[0]][random_shot] = type_to_shot
                await self.bot_passes_move_to_user(lobby_slug)
                await self.perform_write_shot(board_id, board)
                await self.send_json(content=output_data)
                break                
            
            found_ship = board[random_shot[0]][random_shot]
            ship_dict_on_board[found_ship] -= 1
            board[random_shot[0]][random_shot] = type_to_shot
            await self.perform_write_shot(board_id, board)
            
            if ship_dict_on_board[found_ship] == 0:
                fields.update(self._add_misses_around_sunken_ship(found_ship, board))
                del ship_dict_on_board[found_ship]
                del field_dict[random_shot]
                # Если нет больше кораблей, добавить "enemy_ships" ключ к ответу с "0"
                # if not ship_dict_on_board:
                #     logging.info("bye")
                #     break
            else:
                field_dict = self.botEasy_gets_fields_around_hit(random_shot, board, column_name_list)

            await self.send_json(content=output_data)
            await asyncio.sleep(1)


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