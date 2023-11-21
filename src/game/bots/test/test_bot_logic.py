from rest_framework.test import APITransactionTestCase

from src.game.bots import bot_logic


class TestBotCreatesNewGame(APITransactionTestCase):
    """Testing BotCreatesNewGame class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()

        self.instance = bot_logic.BotCreatesNewGame()
    
    def test_bot_creates_new_name(self):
        """Testing _bot_creates_new_name method"""

        game_name = self.instance._bot_creates_new_name("new_game")
        assert game_name == "Game with bot (1)", game_name

        game_name = self.instance._bot_creates_new_name("Game with bot (1)")
        assert game_name == "Game with bot (2)", game_name

        game_name = self.instance._bot_creates_new_name("(1) Game with bot (1)")
        assert game_name == "Game with bot (1)", game_name
    
    def test_bot_creates_new_game(self):
        """Testing bot_creates_new_game method"""
