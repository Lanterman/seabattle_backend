import os
import re

from channels.db import database_sync_to_async

from . import db_queries, bot_levels
from src.game import db_queries as game_db_queries, models


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

    async def bot_take_shot(
            self, user, lobby_id: int, lobby_slug: str, board_id: int, time_to_turn: int, 
            last_hit: str, ships: dict, column_name_list: list, bot_level: str
        ) -> tuple:
        """A bot shooting logic. A bot's shooting cycle will end on a first miss"""

        if bot_level == "EASY":
            await self.easy_bot_take_shot(user, lobby_id, lobby_slug, board_id, time_to_turn, last_hit, ships, column_name_list)
        
        elif bot_level == "MEDIUM":
            await self.medium_bot_take_shot(user, lobby_id, lobby_slug, board_id, time_to_turn, last_hit, ships, column_name_list)
        
        elif bot_level == "HIGH":
            await self.high_bot_take_shot(user, lobby_id, lobby_slug, board_id, time_to_turn, last_hit, ships, column_name_list)
        
        else:
            raise ValueError()
