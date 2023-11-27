import uuid
from rest_framework.test import APITransactionTestCase

from src.game.bots import db_queries
from src.user.models import User


class TestBotDBQueriesModule(APITransactionTestCase):
    """Testing ./bot/db_queris module functions"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.get(id=1)
    
    async def test_create_lobby(self):
        """Testing create_lobby function"""

        lobby_id, lobby_slug = await db_queries.create_lobby("lobby", 30, 30, 60, self.user, "HIGH")
        assert lobby_id == 3, lobby_id
        self.assertEqual(type(lobby_slug), uuid.UUID, type(lobby_slug))
