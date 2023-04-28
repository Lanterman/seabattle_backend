import logging

from django.urls import path
from django.test.testcases import TransactionTestCase
from rest_framework.authtoken.models import Token
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

from .test_data import column_name_list
from src.game.consumers import consumers
from src.game import models, serializers
from src.user.models import User
from config.utilities import redis_instance
from config.middlewares import TokenAuthMiddlewareStack


application = TokenAuthMiddlewareStack(URLRouter([
    path("ws/lobbies/", consumers.LobbyListConsumer.as_asgi()),
    path(r"ws/lobby/<lobby_slug>/", consumers.LobbyConsumer.as_asgi()),
]))


class Config(TransactionTestCase):

    fixtures = ["./src/game/consumers/test/test_data.json"]
        
    def setUp(self):
        super().setUp()
        logging.warning(f"Number of keys in Redis database before running tests: {len(redis_instance.keys())}")

        self.lobby_1 = models.Lobby.objects.get(id=1)
        self.lobby_2 = models.Lobby.objects.get(id=2)
        self.user_1 = User.objects.get(id=1)
        self.user_2 = User.objects.get(id=2)
        self.token_1 = Token.objects.create(user_id=self.user_1.id)
        self.token_2 = Token.objects.create(user_id=self.user_2.id)
        
    def tearDown(self) -> None:
        logging.warning(f"Number of keys in Redis database before closing: {len(redis_instance.keys())}")
        redis_instance.flushall()
        super().tearDown()

    async def launch_websocket_communicator(self, path: str):
        """Launch websocket communicator"""

        communicator = WebsocketCommunicator(application, path)
        connected, sub_protocol = await communicator.connect()

        assert connected
        assert sub_protocol is None

        return communicator


class TestLobbyConsumer(Config):
    """Testing MainPageConsumer consumer"""

    def setUp(self):
        super().setUp()
        self.board_1 = models.Board.objects.get(id=1)
        self.board_1_ships = models.Ship.objects.filter(board_id_id=self.board_1.id)

        self.ser_board_1 = serializers.BoardSerializer(self.board_1).data
        self.ser_board_1_ships = serializers.ShipSerializer(self.board_1_ships, many=True).data

        self.board_column_list = {key: value for key, value in self.ser_board_1.items() if key in column_name_list}

    async def test_refresh_board(self):
        """Testing refresh board"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)

        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id
        assert self.board_1.A[1:49] == "'A1': '', 'A2': ' space 7.1', 'A3': ' space 7.1'", self.board_1.A[1:49]

        test_data = {"type": "refresh_board", "board_id": self.board_1.id, "ships": self.ser_board_1_ships, 
                "board": self.board_column_list}

        await communicator.send_json_to(test_data)
        response = await communicator.receive_json_from()
        assert False, response


        await communicator.disconnect()

    # async def test_create_new_game(self):
    #     """Testing create_new_game"""

    #     communicator = await self.launch_websocket_communicator(path=f"ws/lobby/{self.lobby.slug}/?token={self.user_token}")

    #     test_data = {"type": "create_new_game", "bet": 30, "name": "name", "time_to_move": 30, 
    #                  "time_to_placement": 60, "enemy_id": self.second_user.id}

    #     await communicator.send_json_to(test_data)

    #     await communicator.disconnect()
