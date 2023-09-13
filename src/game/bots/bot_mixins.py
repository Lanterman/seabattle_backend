import os
import re

from channels.db import database_sync_to_async
from .. import db_queries as game_queries


from . import db_queries


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


class BotCreatesNewGame:
    """A bot creates a new game with its own options"""

    @staticmethod
    def _create_new_name(name: str) -> str:
        """Create new name of lobby"""

        default_name_of_game = os.getenv("DOC_DEFAULT_NAME_OF_THE_GAME", os.environ["DEFAULT_NAME_OF_THE_GAME"])

        if name != default_name_of_game:
            return f"{default_name_of_game} (1)"
        
        repeat_number = re.search(r"[\d]+", name)
        return f"{default_name_of_game} ({int(repeat_number) + 1})"

    async def bot_creates_new_game(self, name: str, bet: int, time_to_move: int, time_to_placement: int) -> str:
        new_name = self._create_new_name(name)
        lobby_id, lobby_slug = await db_queries.create_lobby(new_name, bet, time_to_move, time_to_placement, self.user)
        first_board_id, second_board_id = await database_sync_to_async(game_queries.create_lobby_boards)(lobby_id, self.user.id)
        await database_sync_to_async(game_queries.create_ships_for_boards)(first_board_id, second_board_id)
        return str(lobby_slug)


class GenericBotMixin(BotMessage, BotCreatesNewGame):
    """Interface class for all other bot mixins"""