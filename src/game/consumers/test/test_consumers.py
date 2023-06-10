from django.urls import path
from django.test.testcases import TransactionTestCase
from rest_framework.authtoken.models import Token
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

from .test_data import column_name_list
from src.game.consumers import consumers, services
from src.game import models, serializers
from src.user import models as user_models, serializers as user_serializers
from config.utilities import redis_instance
from config.middlewares import TokenAuthMiddlewareStack


application = TokenAuthMiddlewareStack(URLRouter([
    path("ws/main/", consumers.MainConsumer.as_asgi()),
    path(r"ws/lobby/<lobby_slug>/", consumers.LobbyConsumer.as_asgi()),
]))


class Config(TransactionTestCase):

    fixtures = ["./src/game/consumers/test/test_data.json"]
    
    def setUp(self):
        super().setUp()
        self.user_1 = user_models.User.objects.get(id=1)
        self.user_3 = user_models.User.objects.get(id=3)
        self.token_1 = Token.objects.create(user_id=self.user_1.id)
        self.token_3 = Token.objects.create(user_id=self.user_3.id)

        self.ser_user_1 = user_serializers.BaseUserSerializer(self.user_1).data
        self.ser_user_3 = user_serializers.BaseUserSerializer(self.user_3).data
        
    def tearDown(self) -> None:
        redis_instance.flushall()
        super().tearDown()

    async def launch_websocket_communicator(self, path: str):
        """Launch websocket communicator"""

        communicator = WebsocketCommunicator(application, path)
        connected, sub_protocol = await communicator.connect()
        assert connected
        assert sub_protocol is None
        return communicator


class TestMainConsumer(Config):
    """Testing MainConsumer consumer"""

    def setUp(self):
        super().setUp()
        self.lobby_1 = models.Lobby.objects.get(id=1)
        self.lobby_2 = models.Lobby.objects.get(id=2)

        self.ser_lobby_1 = serializers.RetrieveLobbyWithUsersSerializer(self.lobby_1).data
        self.ser_lobby_2 = serializers.RetrieveLobbyWithUsersSerializer(self.lobby_2).data
    
    async def test_created_game(self):
        """Testing created_game event"""

        path_1 = f"ws/main/?token={self.token_1.key}"
        path_2 = f"ws/main/?token={self.token_3.key}"
        communicator_1 = await self.launch_websocket_communicator(path=path_1)
        communicator_2 = await self.launch_websocket_communicator(path=path_2)
        assert communicator_1.scope["user"].id == self.user_1.id, communicator_1.scope["user"].id

        await communicator_1.send_json_to({"type": "created_game", "lobby_slug": str(self.lobby_1.slug)})
        response_1 = await communicator_1.receive_nothing()
        response_2 = await communicator_2.receive_json_from()
        assert response_1 == True, response_1
        assert response_2 == {"type": "created_game", "lobby": self.ser_lobby_1, "user_id": self.user_1.id}, response_2
        
    async def test_deleted_game(self):
        """Testing deleted_game event"""

        path = f"ws/main/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        await communicator.send_json_to({"type": "deleted_game", "lobby_id": self.lobby_1.id})
        response = await communicator.receive_json_from()
        assert response == {"type": "deleted_game", "lobby_id": self.lobby_1.id}, response
    
    async def test_add_user_to_game(self):
        """Testing add_user_to_game event"""

        path_1 = f"ws/main/?token={self.token_1.key}"
        path_2 = f"ws/main/?token={self.token_3.key}"
        communicator_1 = await self.launch_websocket_communicator(path=path_1)
        communicator_2 = await self.launch_websocket_communicator(path=path_2)
        assert communicator_1.scope["user"].id == self.user_1.id, communicator_1.scope["user"].id
        assert communicator_2.scope["user"].id == self.user_3.id, communicator_2.scope["user"].id

        await communicator_1.send_json_to({"type": "add_user_to_game", "lobby_id": self.lobby_1.id})
        response_1 = await communicator_1.receive_nothing()
        response_2 = await communicator_2.receive_json_from()
        data = {"type": "add_user_to_game", "lobby_id": 1, "user_id": self.user_1.id}
        assert response_1 == True, response_1
        assert response_2 == data, response_2



class TestLobbyConsumer(Config):
    """Testing MainPageConsumer consumer"""

    def setUp(self):
        super().setUp()
        self.lobby_1 = models.Lobby.objects.get(id=1)
        self.lobby_2 = models.Lobby.objects.get(id=2)
        self.board_1 = models.Board.objects.get(id=1)
        self.board_1_ships = models.Ship.objects.filter(board_id_id=self.board_1.id)

        self.ser_board_1 = serializers.BoardSerializer(self.board_1).data
        self.ser_board_1_ships = serializers.ShipSerializer(self.board_1_ships, many=True).data

        self.board_column_list = {key: value for key, value in self.ser_board_1.items() if key in column_name_list}

    async def test_refresh_board(self):
        """Testing refresh_board event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id
        assert self.board_1.A[1:49] == "'A1': '', 'A2': ' space 7.1', 'A3': ' space 7.1'", self.board_1.A[1:49]

        test_data = {
            "type": "refresh_board", 
            "board_id": self.board_1.id, 
            "ships": self.ser_board_1_ships, 
            "board": self.board_column_list
        }

        await communicator.send_json_to(test_data)
        response = await communicator.receive_json_from()
        services.clear_board(self.board_column_list)

        test_response = {
            "type": "clear_board", 
            "board": self.board_column_list, 
            "ships": [
                {'id': 1, 'name': 'fourdeck', 'plane': 'horizontal', 'size': 4, 'count': 1}, 
                {'id': 5, 'name': 'tripledeck', 'plane': 'horizontal', 'size': 3, 'count': 2}, 
                {'id': 9, 'name': 'doubledeck', 'plane': 'horizontal', 'size': 2, 'count': 3}, 
                {'id': 13, 'name': 'singledeck', 'plane': 'horizontal', 'size': 1, 'count': 4}
            ]
        }

        assert test_response == response, (response["board"], test_response["board"])
        with self.assertLogs(level="INFO"):
            await communicator.disconnect()

    async def test_drop_ship(self):
        """Testing drop_ship event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        services.clear_board(self.board_column_list)
        test_data = {
            "type": "drop_ship",
            "ship_id": 1,
            "board_id": 1,
            "ship_plane": "horizontal",
            "ship_count": 1,
            "field_name_list": ["A3", "B3", "C3", "D3"],
            "board": self.board_column_list
        }

        await communicator.send_json_to(test_data)
        resposne = await communicator.receive_json_from()

        ships = [
            {'id': 1, 'name': 'fourdeck', 'plane': 'horizontal', 'size': 4, 'count': 0}, 
            {'id': 5, 'name': 'tripledeck', 'plane': 'horizontal', 'size': 3, 'count': 2}, 
            {'id': 9, 'name': 'doubledeck', 'plane': 'horizontal', 'size': 2, 'count': 3}, 
            {'id': 13, 'name': 'singledeck', 'plane': 'horizontal', 'size': 1, 'count': 4}
        ]

        assert resposne["type"] == "drop_ship", resposne["type"]
        assert resposne["ships"] == ships, resposne["ships"]
        assert resposne["board"]["A"]["A3"] == 1.1, resposne["board"]["A"]["A3"]
        assert resposne["board"]["A"]["A4"] == " space 1.1", resposne["board"]["A"]["A4"]
        assert resposne["board"]["A"]["A5"] == "", resposne["board"]["A"]["A5"]
        assert resposne["board"]["E"]["E3"] == " space 1.1", resposne["board"]["E"]["E3"]
        with self.assertLogs(level="INFO"):
            await communicator.disconnect()

    async def test_take_shot(self):
        """Testing take_shot event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        redis_instance.hset(name=str(self.lobby_1.slug), mapping={"current_turn": 0})
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        # miss
        await communicator.send_json_to({"type": "take_shot", "board_id": 1, "field_name": "A2", "time_to_turn": 30})
        resposne = await communicator.receive_json_from()

        data = {
            "type": "send_shot", 
            "field_name_dict": {"A2": "miss"}, 
            "user_id": self.user_1.id, 
            "is_my_turn": False, 
            "enemy_ships": None, 
            "time_left": 30
        }
        
        assert resposne == data, resposne

        # hit
        await communicator.send_json_to({"type": "take_shot", "board_id": 1, "field_name": "A3", "time_to_turn": 30})
        resposne = await communicator.receive_json_from()

        data = {
            "type": "send_shot", 
            "field_name_dict": {"A3": "miss"}, 
            "user_id": self.user_1.id, 
            "is_my_turn": False, 
            "enemy_ships": None, 
            "time_left": 30
        }

        assert resposne == data, resposne

        # hit (destroy ship)
        await communicator.send_json_to({"type": "take_shot", "board_id": 1, "field_name": "C1", "time_to_turn": 30})
        resposne = await communicator.receive_json_from()

        data = {
            "type": "send_shot", 
            "field_name_dict": {'C1': 'hit', 'B1': 'miss', 'B2': 'miss', 'C2': 'miss', 'D1': 'miss', 'D2': 'miss'}, 
            "user_id": self.user_1.id, 
            "is_my_turn": True, 
            "enemy_ships": 9, 
            "time_left": 30
        }

        assert resposne == data, resposne
        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
    
    async def test_is_ready_to_play(self):
        """Testing is_ready_to_play event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        redis_instance.hset(name=str(self.lobby_1.slug), mapping={"is_running": 1})
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        # players are not ready
        await communicator.send_json_to(
            {"type": "is_ready_to_play", "is_ready": False, "is_enemy_ready": True, "board_id": 1}
        )
        response = await communicator.receive_json_from()
        is_running = redis_instance.hget(str(self.lobby_1.slug), "is_running")
        assert is_running == "1", is_running
        assert response == {"type": "is_ready_to_play", "is_ready": False, "user_id": self.user_1.id}, response

        # players are not ready
        await communicator.send_json_to(
            {"type": "is_ready_to_play", "is_ready": True, "is_enemy_ready": False, "board_id": 1}
        )
        response = await communicator.receive_json_from()
        is_running = redis_instance.hget(str(self.lobby_1.slug), "is_running")
        assert is_running == "1", is_running
        assert response == {"type": "is_ready_to_play", "is_ready": True, "user_id": self.user_1.id}, response

        # players are ready
        await communicator.send_json_to(
            {"type": "is_ready_to_play", "is_ready": True, "is_enemy_ready": True, "board_id": 1}
        )
        response = await communicator.receive_json_from()
        is_running = redis_instance.hget(str(self.lobby_1.slug), "is_running")
        assert is_running == None, is_running
        assert response == {"type": "is_ready_to_play", "is_ready": True, "user_id": self.user_1.id}, response
        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
    
    async def test_random_placement(self):
        """Testing random_placement event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        await communicator.send_json_to(
            {"type": "random_placement", "board_id": 1, "board": self.board_column_list ,"ships": self.ser_board_1_ships}
        )
        response = await communicator.receive_json_from()
        
        ships = [
            {'id': 1, 'name': 'fourdeck', 'plane': 'horizontal', 'size': 4, 'count': 0}, 
            {'id': 5, 'name': 'tripledeck', 'plane': 'horizontal', 'size': 3, 'count': 0}, 
            {'id': 9, 'name': 'doubledeck', 'plane': 'horizontal', 'size': 2, 'count': 0}, 
            {'id': 13, 'name': 'singledeck', 'plane': 'horizontal', 'size': 1, 'count': 0}
        ]

        assert response["type"] == "random_placed", response["type"]
        assert response["ships"] == ships, response["ships"]
        assert response["board"] != self.board_column_list, response["board"]
        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
    
    async def test_who_starts(self):
        """Testing who_starts event"""

        # receive dict
        path = f"ws/lobby/{self.lobby_2.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        await communicator.send_json_to({"type": "who_starts"})
        response = await communicator.receive_json_from()
        assert response["type"] == "who_starts", response["type"]
        self.assertIn(response["is_my_turn"], [True, False], response["is_my_turn"])
        self.assertIn(response["user_id"], [1, 2], response["user_id"])
        with self.assertLogs(level="INFO"):
            await communicator.disconnect()

        # receive nothing
        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        await communicator.send_json_to({"type": "who_starts"})
        with self.assertLogs(level="INFO"):
            response = await communicator.receive_nothing()
        assert response == True, response
        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
    
    async def test_determine_winner(self):
        """Testing determine_winner event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        # admin is winner
        redis_instance.hset(str(self.lobby_1.slug), mapping={"time_left": 30, "current_turn": 1})
        await communicator.send_json_to({"type": "determine_winner", "bet": 50})
        response = await communicator.receive_json_from()
        key_in_redis = redis_instance.hget(str(self.lobby_1.slug), "current_turn")
        assert response == {"type": "determine_winner", "winner": "admin"}, response
        assert key_in_redis == None, key_in_redis
        
        # enemy is winner
        redis_instance.hset(str(self.lobby_1.slug), "time_left", 30)
        await communicator.send_json_to({"type": "determine_winner", "bet": 50, "enemy_id": 2})
        response = await communicator.receive_json_from()
        key_in_redis = redis_instance.hget(str(self.lobby_1.slug), "current_turn")
        assert response == {"type": "determine_winner", "winner": "lanterman"}, response
        assert key_in_redis == None, key_in_redis

        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
    
    async def test_countdown(self):
        """Testing countdown event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        # time_left argument is not passed and is_running key exists
        redis_instance.hset(str(self.lobby_1.slug), mapping={"current_turn": 1, "time_left": 30, "is_running": 1})
        await communicator.send_json_to({"type": "countdown", "time_to_turn": None})
        response = await communicator.receive_json_from()
        current_turn = redis_instance.hget(str(self.lobby_1.slug), "current_turn")
        is_running = redis_instance.hget(str(self.lobby_1.slug), "is_running")
        assert response == {"type": "countdown", "time_left": 30}, response
        assert current_turn == "1", current_turn
        assert is_running == "1", is_running

        redis_instance.hdel(str(self.lobby_1.slug), "is_running")

        # time_left argument is passed and is_running key not exists
        await communicator.send_json_to({"type": "countdown", "time_to_turn": 20})
        response = await communicator.receive_json_from()
        current_turn = redis_instance.hget(str(self.lobby_1.slug), "current_turn")
        is_running = redis_instance.hget(str(self.lobby_1.slug), "is_running")
        assert response == {"type": "countdown", "time_left": 20}, response
        assert current_turn == "2", current_turn
        assert is_running == "1", is_running

        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
    
    async def test_time_is_over(self):
        """Testing time_is_over event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        redis_instance.hset(str(self.lobby_1.slug), "is_running", 1)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        await communicator.send_json_to(
            {"type": "time_is_over", "board_id": 1 ,"ships": self.ser_board_1_ships, "board": self.board_column_list}
        )
        response = await communicator.receive_json_from()

        ships = [
            {'id': 1, 'name': 'fourdeck', 'plane': 'horizontal', 'size': 4, 'count': 0}, 
            {'id': 5, 'name': 'tripledeck', 'plane': 'horizontal', 'size': 3, 'count': 0}, 
            {'id': 9, 'name': 'doubledeck', 'plane': 'horizontal', 'size': 2, 'count': 0}, 
            {'id': 13, 'name': 'singledeck', 'plane': 'horizontal', 'size': 1, 'count': 0}
        ]

        assert response["type"] == "random_placed", response["type"]
        assert response["ships"] == ships, response["ships"]
        assert response["board"] != self.board_column_list, response["board"]

        response = await communicator.receive_json_from()
        is_running = redis_instance.hget(str(self.lobby_1.slug), "is_running")
        assert response == {"type": "is_ready_to_play", "is_ready": True, "user_id": self.user_1.id}, response
        assert is_running == None, is_running

        response = await communicator.receive_nothing()
        assert response == True

        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
    
    async def test_add_user_to_game(self):
        """Testing add_user_to_game event"""

        # two players in lobby and player is already in lobby
        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        await communicator.send_json_to({"type": "add_user_to_game", "lobby_id": 1, "board_id": 1})
        response = await communicator.receive_json_from()
        assert response["type"] == "add_user_to_game", response["type"]
        assert response["user"] == self.ser_user_1, response["user"]
        assert response["message"]["message"] ==  "Admin connected to the game.", response["message"]["message"]

        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
        
        # two players in lobby and player is not in lobby
        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_3.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_3.id, communicator.scope["user"].id

        await communicator.send_json_to({"type": "add_user_to_game", "lobby_id": 1, "board_id": 1})
        with self.assertLogs(level="INFO"):
            response = await communicator.receive_json_from()
        assert response["type"] == "add_user_to_game", response["type"]
        assert response["user"] == None, response["user"]
        with self.assertRaises(KeyError):
            assert response["message"]

        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
        
        # one players in lobby
        path = f"ws/lobby/{self.lobby_2.slug}/?token={self.token_3.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_3.id, communicator.scope["user"].id

        await communicator.send_json_to({"type": "add_user_to_game", "lobby_id": 1, "board_id": 1})
        response = await communicator.receive_json_from()
        assert response["type"] == "add_user_to_game", response["type"]
        assert response["user"] == self.ser_user_3, response["user"]
        assert response["message"]["message"] ==  "User connected to the game.", response["message"]["message"]

        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
    
    async def test_send_message(self):
        """Testing send_message event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        await communicator.send_json_to({"type": "send_message", "lobby_id": 1, "message": "Hi there!"})
        response = await communicator.receive_json_from()
        assert response["type"] == "send_message", response["type"]
        assert response["message"]["message"] == "Hi there!", response["message"]["message"]
        assert response["message"]["owner"] == "admin", response["message"]["owner"]
        assert response["message"]["is_bot"] == False, response["message"]["is_bot"]

        with self.assertLogs(level="INFO"):
            await communicator.disconnect()
    
    async def test_is_play_again(self):
        """Testing is_play_again event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        # want to play again
        await communicator.send_json_to({"type": "is_play_again", "lobby_id": 1, "board_id": 1, "answer": True})
        response = await communicator.receive_json_from()
        assert response["type"] == "is_play_again", response["type"]
        assert response["is_play_again"] == True, response["is_play_again"]
        assert response["message"]["message"] == "Admin want to play again.", response["message"]["message"]

        # doesn't want to play again
        await communicator.send_json_to({"type": "is_play_again", "lobby_id": 1, "board_id": 1, "answer": False})
        response = await communicator.receive_json_from()
        assert response["type"] == "is_play_again", response["type"]
        assert response["is_play_again"] == False, response["is_play_again"]
        assert response["message"]["message"] == "Admin doesn't want to play again.", response["message"]["message"]

        with self.assertLogs(level="INFO"):
            await communicator.disconnect()

    async def test_create_new_game(self):
        """Testing create_new_game event"""

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id
        number_of_lobby_1 = await database_sync_to_async(models.Lobby.objects.all)()

        test_data = {
            "type": "create_new_game", 
            "bet": 100, 
            "name": "string", 
            "time_to_move": 30, 
            "time_to_placement": 60, 
            "enemy_id": 2
        }

        await communicator.send_json_to(test_data)
        number_of_lobby_2 = await database_sync_to_async(models.Lobby.objects.all)()
        response = await communicator.receive_json_from()
        assert response["type"] == "new_group", response["type"]
        assert type(response["lobby_slug"]) == str, response
        assert number_of_lobby_1 != number_of_lobby_2

        with self.assertLogs(level="INFO"):
            await communicator.disconnect()

    async def test_delete_game(self):
        """Testing delete_game event"""

        @database_sync_to_async
        def is_exist_fun(lobby_id):
            """Check if a lobby instance is exists"""

            query = models.Lobby.objects.filter(id=lobby_id).exists()
            return query

        path = f"ws/lobby/{self.lobby_1.slug}/?token={self.token_1.key}"
        communicator = await self.launch_websocket_communicator(path=path)
        assert communicator.scope["user"].id == self.user_1.id, communicator.scope["user"].id

        is_exists = await is_exist_fun(1)
        assert is_exists == True, is_exists

        await communicator.send_json_to({"type": "delete_game"})
        response = await communicator.receive_nothing()
        is_exists = await is_exist_fun(1)
        assert response == True, response
        assert is_exists == False, is_exists

