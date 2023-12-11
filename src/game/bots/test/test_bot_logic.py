from rest_framework.test import APITransactionTestCase
from channels.db import database_sync_to_async

from src.game import models as game_models
from src.game.bots import bot_logic
from src.user.models import User


class TestBotCreatesNewGame(APITransactionTestCase):
    """Testing BotCreatesNewGame class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()

        self.user = User.objects.get(id=1)

        self.instance = bot_logic.BotCreatesNewGame()
    
    def test_bot_creates_new_name(self):
        """Testing _bot_creates_new_name method"""

        game_name = self.instance._bot_creates_new_name("new_game")
        assert game_name == "Game with bot (1)", game_name

        game_name = self.instance._bot_creates_new_name("Game with bot (1)")
        assert game_name == "Game with bot (2)", game_name

        game_name = self.instance._bot_creates_new_name("(1) Game with bot (1)")
        assert game_name == "Game with bot (1)", game_name
    
    async def test_bot_creates_new_game(self):
        """Testing bot_creates_new_game method"""

        count_lobby = await database_sync_to_async(game_models.Lobby.objects.count)()
        count_board = await database_sync_to_async(game_models.Board.objects.count)()
        count_ship = await database_sync_to_async(game_models.Ship.objects.count)()
        assert count_lobby == 2, count_lobby
        assert count_board == 4, count_board
        assert count_ship == 16, count_ship

        new_lobby_slug = await self.instance.bot_creates_new_game("lobby", 50, 30, 30, self.user, "EASY")
        count_lobby = await database_sync_to_async(game_models.Lobby.objects.count)()
        count_board = await database_sync_to_async(game_models.Board.objects.count)()
        count_ship = await database_sync_to_async(game_models.Ship.objects.count)()
        self.assertTrue(new_lobby_slug)
        assert len(new_lobby_slug) >= 20, new_lobby_slug
        assert count_lobby == 3, count_lobby
        assert count_board == 6, count_board
        assert count_ship == 24, count_ship


class TestBotTakeToShot(APITransactionTestCase):
    """Testing BotCreatesNewGame class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()

        self.user = User.objects.get(id=1)

        self.instance = bot_logic.BotTakeShot()
    
    async def test_bot_take_shot(self) -> None:
        """Testing method bot_take_shot (only ValueError)"""

        with self.assertRaises(ValueError):
            await self.instance.bot_take_shot(self.user, 1, "slug", 1, 30, "", {}, [], "easy" )
