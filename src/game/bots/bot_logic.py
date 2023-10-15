import os
import re

from channels.db import database_sync_to_async

from . import db_queries, bot_levels
from config.utilities import redis_instance
from src.game import db_queries as game_db_queries, models
from src.game.consumers import db_queries as ws_db_queries, services as ws_services


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

    async def bot_creates_new_game(
            self, name: str, bet: int, time_to_move: int, time_to_placement: int, user: models.User, bot_level: str
        ) -> str:
        new_name = self._bot_creates_new_name(name)
        lobby_id, lobby_slug = await db_queries.create_lobby(new_name, bet, time_to_move, time_to_placement, user, bot_level)
        first_board_id, second_board_id = await database_sync_to_async(game_db_queries.create_lobby_boards)(lobby_id, user.id)
        await database_sync_to_async(game_db_queries.create_ships_for_boards)(first_board_id, second_board_id)
        return str(lobby_slug)


class BotTakeShot(bot_levels.EasyBot, bot_levels.MediumBot, bot_levels.HighBot):
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
    def bot_gets_ship_size_and_name_list(ships: dict) -> list:
        """A bot creates a sorted list of ship sizes and their identifier in the tuple."""

        ship_size_and_name_list = []

        for ship_item in ships:
            ship_size_and_name_list.append((ship_item["size"], ship_item["id"]))
        
        return sorted(ship_size_and_name_list, reverse=True)


    @staticmethod
    def bot_selects_target(ship_dict_on_board: dict, ship_size_and_name_list: dict) -> int:
        """Bot selects the best a target"""

        ship_id_list = set(int(ship_id) for ship_id in ship_dict_on_board)

        for ship_size, ship_id in ship_size_and_name_list:
            if ship_id in ship_id_list:
                return ship_size

    @staticmethod
    def bot_get_field_list(board: dict, column_name_list: list, max_index: int) -> dict:
        """Get a list of valid fields for a shot """

        field_dict = {}
        index = max_index - 1 if max_index > 1 else 1
        for char in column_name_list[::-1]:
            index = index if index <= max_index else 1
            for num in range(index, 11, max_index):
                _field = f"{char}{num}"
                if board[char][_field] not in ("hit", "miss"):
                    field_dict[_field] = board[char][_field]

            index += 1
        
        return field_dict
    
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
    
    def bot_gets_fields_around_hit(self, current_field: str, board: dict, column_name_list: list) -> dict:
        """A easy bot receives fields around the board"""

        field_dict = {}
        field_number = int(current_field[1:])
        column_name = current_field[0]
        column_index = column_name_list.index(column_name)

        plane = self.bot_defines_plane(current_field, board, column_name_list)

        if not plane:
            _field = f"{column_name}{field_number - 1}"
            if field_number > 1 and board[column_name][_field] not in ("hit", "miss"):
                field_dict[_field] = board[column_name][_field]
            
            _field = f"{column_name}{field_number + 1}"
            if field_number < 10 and board[column_name][_field] not in ("hit", "miss"):
                field_dict[_field] = board[column_name][_field]
            
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
    
    async def bot_passes_move_to_user(self, lobby_slug: str, user) -> None:
        boards = await ws_db_queries.get_lobby_boards(lobby_slug)
        my_board, enemy_board = await ws_services.determine_whoose_boards(user, boards)
        await ws_db_queries.update_boards(True, my_board, enemy_board)

    async def bot_take_shot(
            self, user, lobby_slug: str, board_id: int, time_to_turn: int, last_hit: str, 
            ships: dict, column_name_list: list, bot_level: str
        ) -> tuple:
        """A bot shooting logic. A bot's shooting cycle will end on a first miss"""

        if bot_level == "EASY":
            await self.easy_bot_take_shot(user, lobby_slug, board_id, time_to_turn, last_hit, ships, column_name_list)
        
        elif bot_level == "MEDIUM":
            await self.medium_bot_take_shot(user, lobby_slug, board_id, time_to_turn, last_hit, ships, column_name_list)
        
        elif bot_level == "HIGH":
            await self.high_bot_take_shot(user, lobby_slug, board_id, time_to_turn, last_hit, ships, column_name_list)
        
        else:
            raise ValueError()
