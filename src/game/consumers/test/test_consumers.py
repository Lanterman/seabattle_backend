import logging

from django.urls import path
from django.test import TestCase
from rest_framework.authtoken.models import Token
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

from .data import board, ships, column_name_list, row
from src.game.consumers import consumers
from src.game import models
from src.user.models import User
from config.utilities import redis_instance
from config.middlewares import TokenAuthMiddlewareStack


application = TokenAuthMiddlewareStack(URLRouter([
    path("ws/lobbies/", consumers.LobbyListConsumer.as_asgi()),
    path(r"ws/lobby/<lobby_slug>/", consumers.LobbyConsumer.as_asgi()),
]))


class Config(TestCase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.warning(f"Number of keys in Redis database before running tests: {len(redis_instance.keys())}")

        cls.user = User.objects.create(username='user1', password='password', email="user1@mail.ru")
        cls.second_user = User.objects.create(username='second_user1', password='password', 
                                                    email="second_user1@mail.ru")
        cls.third_user = User.objects.create(username='third_user1', password='password',
                                                  email="third_user1@gmail.com")

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
        super().tearDownClass()

    async def launch_websocket_communicator(self, path: str):
        """Launch websocket communicator"""

        communicator = WebsocketCommunicator(application, path)
        communicator.scope['url_route'] = {"kwargs": {"lobby_slug": self.lobby.slug}} if path != "/ws/lobbies/" else {}
        communicator.scope["user"] = self.user
        connected, sub_protocol = await communicator.connect()
        assert connected
        assert sub_protocol is None
        return communicator


class TestLobbyConsumer(Config):
    """Testing MainPageConsumer consumer"""

    # async def test_refresh_board(self):
    #     """Testing refresh board"""

    #     communicator = await self.launch_websocket_communicator(path=f"ws/lobby/{self.lobby.slug}/")

    #     assert communicator.scope["user"].id == self.user.id, communicator.scope["user"].id
    #     assert self.first_board.A == row, self.first_board.A

    #     test_data = {"type": "refresh_board", "board_id": self.first_board.id, "ships": ships, 
    #             "board": board}

    #     await communicator.send_json_to(test_data)


    #     await communicator.disconnect()

    # async def test_create_new_game(self):
    #     """Testing create_new_game"""

    #     communicator = await self.launch_websocket_communicator(path=f"ws/lobby/{self.lobby.slug}/?token={self.user_token}")

    #     test_data = {"type": "create_new_game", "bet": 30, "name": "name", "time_to_move": 30, 
    #                  "time_to_placement": 60, "enemy_id": self.second_user.id}

    #     await communicator.send_json_to(test_data)

    #     await communicator.disconnect()
