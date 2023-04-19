import logging

from channels.consumer import AsyncConsumer
from django.test import TestCase
from rest_framework.authtoken.models import Token
from channels.testing import WebsocketCommunicator

from .data import board, ships
from .. import consumers
from src.game import models
from src.user.models import User
from config.utilities import redis_instance


column_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
row = "{'A1': '', 'A2': 'qwe', 'A3': '', 'A4': '', 'A5': '12', 'A6': '', 'A7': 'qwe', 'A8': '', 'A9': '', 'A10': ''}"

class Config(TestCase):

    @classmethod
    def setUpTestData(cls):
        logging.warning(f"Number of keys in Redis database before running tests: {len(redis_instance.keys())}")

        cls.user = User.objects.create_user(username='user', password='password', email="user@mail.ru")
        cls.second_user = User.objects.create_user(username='second_user', password='password', 
                                                    email="second_user@mail.ru")
        cls.third_user = User.objects.create_user(username='third_user', password='password')

        cls.user_token = Token.objects.create(user=cls.user)
        cls.third_user_token = Token.objects.create(user=cls.third_user)
    
        cls.lobby = models.Lobby.objects.create(name="test", bet=10, time_to_move=30, time_to_placement=30)
        cls.lobby.users.add(cls.user, cls.second_user)

        cls.first_board = models.Board.objects.create(lobby_id_id=cls.lobby.id, user_id_id=cls.user.id, A=row)
        cls.second_board = models.Board.objects.create(lobby_id_id=cls.lobby.id, user_id_id=cls.second_user.id)

        models.Ship.objects.bulk_create([
            models.Ship(name="singledeck", size=1, count=0, board_id_id=cls.first_board.id),
            models.Ship(name="doubledeck", size=2, count=0, board_id_id=cls.first_board.id),
            models.Ship(name="tripledeck", size=3, count=0, board_id_id=cls.first_board.id),
            models.Ship(name="fourdeck", size=4, count=1, board_id_id=cls.first_board.id),
            models.Ship(name="singledeck", size=1, count=4, board_id_id=cls.second_board.id),
            models.Ship(name="doubledeck", size=2, count=3, board_id_id=cls.second_board.id),
            models.Ship(name="tripledeck", size=3, count=2, board_id_id=cls.second_board.id),
            models.Ship(name="fourdeck", size=4, count=1, board_id_id=cls.second_board.id),
    ])

        models.Message.objects.create(message="Hi, tester!", owner=cls.user.username, lobby_id_id=cls.lobby.id)
        models.Message.objects.create(message="I'm a bot!", owner=cls.user.username, is_bot=True, lobby_id_id=cls.lobby.id)

    @classmethod
    def tearDownClass(cls) -> None:
        logging.warning(f"Number of keys in Redis database before closing: {len(redis_instance.keys())}")
        redis_instance.flushall()

    async def launch_websocket_communicator(
            self, consumer: type[AsyncConsumer] = consumers.LobbyConsumer, path: str = f"ws/lobby/"
    ):
        """Launch websocket communicator"""

        communicator = WebsocketCommunicator(consumer.as_asgi(), path)
        communicator.scope['url_route'] = {"kwargs": {"lobby_slug": self.lobby.slug}} if path != "/ws/lobby/" else {}
        communicator.scope["user"] = self.user
        connected, _ = await communicator.connect()
        assert connected
        return communicator


class TestLobbyConsumer(Config):
    """Testing MainPageConsumer consumer"""

    async def test_refresh_board(self):
        """Testing refresh board"""

        communicator = await self.launch_websocket_communicator()

        assert self.first_board.A == row, self.first_board.A

        data = {"type": "refresh_board", "board_id": self.first_board.id, "ships": ships, 
                "board": board}

        await communicator.send_json_to(data)

        response = await communicator.receive_json_from()
        # assert response == test_data, response
        assert 1 == 2, response

        await communicator.disconnect()
