import random
import asyncio

from config.utilities import redis_instance
from src.game.consumers import db_queries as ws_db_queries, services as ws_services


class EasyBot:
    """Easy bot level"""

    async def easy_bot_take_shot(
            self, user, lobby_slug: str, board_id: int, time_to_turn: int, last_hit: str, 
            ships: dict, column_name_list: list
        ) -> tuple:
        """A bot shooting logic. A bot's shooting cycle will end on a first miss"""


class MediumBot:
    """Medium bot level"""

    async def medium_bot_take_shot(
            self, user, lobby_slug: str, board_id: int, time_to_turn: int, last_hit: str, 
            ships: dict, column_name_list: list
        ) -> tuple:
        """A bot shooting logic. A bot's shooting cycle will end on a first miss"""

        board = await ws_db_queries.get_board(board_id, column_name_list)
        ws_services.confert_to_json(board)
        ship_dict_on_board = self.bot_gets_ship_dict_on_the_board(board)
        ship_size_and_name_list = self.bot_gets_ship_size_and_name_list(ships)
        output_data = {
                "type": "bot_taken_to_shot", 
                "field_dict": {}, 
                "is_my_turn": False,
                "last_hit": "",
                "time_left": 1
            }
        
        if not ship_dict_on_board:
            output_data["enemy_ships"] = 0
            return await self.send_json(content=output_data)

        # Checking whether there is a wounded ship on the user's board
        if last_hit:
            field_dict = self.bot_gets_fields_around_hit(last_hit, board, column_name_list)
        else:
            max_index = self.bot_selects_target(ship_dict_on_board, ship_size_and_name_list)
            field_dict = self.bot_get_field_list(board, column_name_list, max_index)

        while True:
            # Delete "is_running" key from <lobby_slug> (remove this key from the redis dictionary to update the timer)
            redis_instance.hdel(lobby_slug, "is_running")
            
            # Update move time
            countdown = await self._countdown(self.lobby_name, time_to_turn)

            if not field_dict:
                field_dict = self.bot_get_field_list(board, column_name_list, 1)
            
            random_shot = random.choice(list(field_dict))
            type_to_shot = "hit" if type(board[random_shot[0]][random_shot]) == float else "miss"
            fields = {random_shot: type_to_shot}

            output_data["field_dict"] = fields
            output_data["last_hit"] = last_hit
            output_data["time_left"] = countdown["time_left"]

            if type_to_shot == "miss":
                output_data["is_my_turn"] = True
                board[random_shot[0]][random_shot] = type_to_shot
                await self.bot_passes_move_to_user(lobby_slug, user)
                await self.perform_write_shot(board_id, board)
                return await self.send_json(content=output_data)             
            
            found_ship = board[random_shot[0]][random_shot]
            ship_dict_on_board[found_ship] -= 1
            board[random_shot[0]][random_shot] = type_to_shot
            await self.perform_write_shot(board_id, board)
            
            if ship_dict_on_board[found_ship] == 0:
                last_hit = ""
                del ship_dict_on_board[found_ship]

                fields.update(self._add_misses_around_sunken_ship(found_ship, board))

                if ship_dict_on_board:
                    max_index = self.bot_selects_target(ship_dict_on_board, ship_size_and_name_list)
                    field_dict = self.bot_get_field_list(board, column_name_list, max_index)
                else:
                    output_data["enemy_ships"] = 0
                    return await self.send_json(content=output_data)
            else:
                field_dict = self.bot_gets_fields_around_hit(random_shot, board, column_name_list)
                last_hit = random_shot

            await self.send_json(content=output_data)
            await asyncio.sleep(1)


class HighBot:
    """High bot level"""

    async def high_bot_take_shot(
            self, user, lobby_slug: str, board_id: int, time_to_turn: int, last_hit: str, 
            ships: dict, column_name_list: list
        ) -> tuple:
        """A bot shooting logic. A bot's shooting cycle will end on a first miss"""