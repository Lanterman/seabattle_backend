import logging

from copy import deepcopy
from channels.db import database_sync_to_async
from rest_framework.test import APITestCase, APITransactionTestCase

from src.game import models, serializers
from src.user import models as user_models, serializers as user_serializers
from src.game.consumers import services, mixins, db_queries
from .test_data import column_name_list, ship_count_dict
from config.utilities import redis_instance


class TestRefreshBoardMixin(APITestCase):
    """Testing the RefreshBoardMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.board_1 = models.Board.objects.get(id=1)
        self.board_2 = models.Board.objects.get(id=2)
        self.board_3 = models.Board.objects.get(id=3)

        self.ser_board_1 = serializers.BoardSerializer(self.board_1).data
        self.ser_board_2 = serializers.BoardSerializer(self.board_2).data
        self.ser_board_3 = serializers.BoardSerializer(self.board_3).data

        self.instance = mixins.RefreshBoardMixin()
    
    def test_clear_board(self):
        """Testing the _clear_board method"""

        assert self.ser_board_1["A"]["A2"] == " space 7.1", self.ser_board_1["A"]["A2"]
        assert self.ser_board_2["A"]["A2"] == 26.3, self.ser_board_2["A"]["A2"]
        assert self.ser_board_3["A"]["A2"] == "", self.ser_board_3["A"]["A2"]

        board = {key: value for key, value in self.ser_board_1.items() if key in column_name_list}
        self.instance._clear_board(board)
        assert self.ser_board_1["A"]["A2"] == "", self.ser_board_1["A"]["A2"]

        board = {key: value for key, value in self.ser_board_2.items() if key in column_name_list}
        self.instance._clear_board(board)
        assert self.ser_board_2["A"]["A2"] == "", self.ser_board_2["A"]["A2"]

        board = {key: value for key, value in self.ser_board_3.items() if key in column_name_list}
        self.instance._clear_board(board)
        assert self.ser_board_3["A"]["A2"] == "", self.ser_board_3["A"]["A2"]


class TestRefreshShipsMixin(APITransactionTestCase):
    """Testing the RefreshShipsMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.ships_of_board_1 = models.Ship.objects.filter(board_id_id=1)
        self.ships_of_board_2 = models.Ship.objects.filter(board_id_id=2)
        self.ships_of_board_3 = models.Ship.objects.filter(board_id_id=3)

        self.ser_ships_of_board_1 = serializers.ShipSerializer(self.ships_of_board_1, many=True).data
        self.ser_ships_of_board_2 = serializers.ShipSerializer(self.ships_of_board_2, many=True).data
        self.ser_ships_of_board_3 = serializers.ShipSerializer(self.ships_of_board_3, many=True).data
        self.instance = mixins.RefreshShipsMixin()
        self.instance.ship_count_dict = ship_count_dict

    async def test_update_ships(self):
        """Testing the update_ships method"""

        count_ships_of_board_1 = [ship.count for ship in self.ships_of_board_1]
        count_ships_of_board_2 = [ship.count for ship in self.ships_of_board_2]
        count_ships_of_board_3 = [ship.count for ship in self.ships_of_board_3]

        assert count_ships_of_board_1 == [1, 2, 3, 4], count_ships_of_board_1
        assert count_ships_of_board_2 == [0, 0, 0, 0], count_ships_of_board_2
        assert count_ships_of_board_3 == [0, 0, 0, 0], count_ships_of_board_3

        ship_list = await self.instance.update_ships(1, self.ser_ships_of_board_1)
        up_count_ships_of_board_1 = [ship["count"] for ship in ship_list]
        assert up_count_ships_of_board_1 == [1, 2, 3, 4], up_count_ships_of_board_1
        assert ship_list == self.ser_ships_of_board_1, ship_list
        assert count_ships_of_board_1 == up_count_ships_of_board_1, up_count_ships_of_board_1

        ship_list = await self.instance.update_ships(1, self.ser_ships_of_board_2)
        up_count_ships_of_board_2 = [ship["count"] for ship in ship_list]
        assert up_count_ships_of_board_2 == [1, 2, 3, 4]
        assert ship_list != self.ser_ships_of_board_2, ship_list
        assert count_ships_of_board_2 != up_count_ships_of_board_2, up_count_ships_of_board_2

        ship_list = await self.instance.update_ships(1, self.ser_ships_of_board_3)
        up_count_ships_of_board_3 = [ship["count"] for ship in ship_list]
        assert up_count_ships_of_board_3 == [1, 2, 3, 4]
        assert ship_list != up_count_ships_of_board_3, ship_list
        assert count_ships_of_board_3 != up_count_ships_of_board_3, up_count_ships_of_board_3


class TestDropShipOnBoardMixin(APITestCase):
    """Testing the DropShipOnBoardMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.board_1 = models.Board.objects.get(id=1)
        self.board_2 = models.Board.objects.get(id=2)

        self.ser_board_1 = serializers.BoardSerializer(self.board_1).data
        self.ser_board_2 = serializers.BoardSerializer(self.board_2).data

        self.instance = mixins.DropShipOnBoardMixin()

    def test_drop_ship_on_board(self):
        """Testing the drop_ship_on_board method"""

        board_1 = {key: value for key, value in self.ser_board_1.items() if key in column_name_list}
        board_2 = {key: value for key, value in self.ser_board_2.items() if key in column_name_list}
        services.clear_board(board_1)
        services.clear_board(board_2)
        copy_board_1 = deepcopy(board_1)
        copy_board_2 = deepcopy(board_2)

        assert copy_board_1["G"]["G1"] == "", copy_board_1["G"]["G1"]
        assert copy_board_2["D"]["D1"] == "", copy_board_2["D"]["D1"]

        self.instance.drop_ship_on_board(1, 4, ["F1", "G1", "H1", "I1"], copy_board_1)
        assert copy_board_1 != board_1, copy_board_1
        assert copy_board_1["G"]["G1"] == 1.4, board_1["G"]["G1"]
        assert board_1["G"]["G1"] == "", board_1["G"]["G1"]

        self.instance.drop_ship_on_board(112123, 4123123, ["B1", "E1", "D1", "I1"], copy_board_2)
        assert copy_board_2 != board_2, copy_board_2
        assert copy_board_2["D"]["D1"] == 112123.4123123, copy_board_2["D"]["D1"]
        assert board_2["D"]["D1"] == "", board_2["D"]["D1"]


class TestAddSpaceAroundShipMixin(APITestCase):
    """Testing the AddSpaceAroundShipMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.board_1 = models.Board.objects.get(id=1)
        self.board_2 = models.Board.objects.get(id=2)
        self.board_3 = models.Board.objects.get(id=3)

        self.ser_board_1 = serializers.BoardSerializer(self.board_1).data
        self.ser_board_2 = serializers.BoardSerializer(self.board_2).data
        self.ser_board_3 = serializers.BoardSerializer(self.board_3).data

        self.instance = mixins.AddSpaceAroundShipMixin()
        self.instance.column_name_list = column_name_list

    def test_insert_space_around_ship(self):
        """Testing the insert_space_around_ship method"""

        board_1 = {key: value for key, value in self.ser_board_1.items() if key in column_name_list}
        board_2 = {key: value for key, value in self.ser_board_2.items() if key in column_name_list}
        board_3 = {key: value for key, value in self.ser_board_3.items() if key in column_name_list}
        services.clear_board(board_1)
        services.clear_board(board_2)
        services.clear_board(board_3)
        copy_board_1 = deepcopy(board_1)
        copy_board_2 = deepcopy(board_2)
        copy_board_3 = deepcopy(board_3)

        assert copy_board_1["G"]["G1"] == "", copy_board_1["G"]["G1"]
        assert copy_board_2["F"]["F1"] == "", copy_board_2["F"]["F1"]
        assert copy_board_3["H"]["H1"] == "", copy_board_3["H"]["H1"]

        self.instance.insert_space_around_ship(" space 27.4", "horizontal", ["F1", "G1", "H1", "I1"], copy_board_1)
        assert copy_board_1 != board_1, copy_board_1
        assert copy_board_1["G"]["G2"] == " space 27.4", copy_board_1["G"]["G2"]
        assert copy_board_1["F"]["F5"] == "", copy_board_1["F"]["F5"]
        assert copy_board_1["H"]["H2"] == " space 27.4", copy_board_1["H"]["H2"]

        self.instance.insert_space_around_ship(" space 27.3", "vertical", ["F1", "F2", "F3", "F4"], copy_board_2)
        assert copy_board_2 != board_2, copy_board_2
        assert copy_board_2["G"]["G2"] == " space 27.3", copy_board_2["G"]["G2"]
        assert copy_board_2["F"]["F5"] == " space 27.3", copy_board_2["F"]["F5"]
        assert copy_board_2["H"]["H2"] == "", copy_board_2["H"]["H2"]

        self.instance.insert_space_around_ship(" space 27.2", "vertical", ["H1", "H2", "H3", "H4"], copy_board_3)
        assert copy_board_3 != board_3, copy_board_3
        assert copy_board_3["G"]["G2"] == " space 27.2", copy_board_3["G"]["G2"]
        assert copy_board_3["F"]["F5"] == "", copy_board_3["F"]["F5"]
        assert copy_board_3["H"]["H2"] == "", copy_board_3["H"]["H2"]


class TestIsReadyToPlayMixin(APITransactionTestCase):
    """Testing the IsReadyToPlayMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        class_name = self.__class__.__name__
        info = f"{class_name}: Number of keys in Redis database before running tests: {len(redis_instance.keys())}"
        logging.info(info)

        self.lobby = models.Lobby.objects.get(id=1)

        self.instance = mixins.IsReadyToPlayMixin()
        self.lobby_name = str(self.lobby.slug)
        self.instance.lobby_name = self.lobby_name

        redis_instance.hset(name=self.lobby_name, mapping={"is_running": 1})
    
    def tearDown(self) -> None:
        class_name = self.__class__.__name__
        info = f"{class_name}: Number of keys in Redis database before closing: {len(redis_instance.keys())}"
        logging.info(info)
        redis_instance.delete(self.lobby_name)
        super().tearDown()

    async def test_ready_to_play(self):
        """Testing the ready_to_play method"""

        is_running = redis_instance.hget(name=self.lobby_name, key="is_running")
        assert is_running == "1", is_running

        is_ready = await self.instance._is_ready_to_play(1, False, True)
        is_running = redis_instance.hget(name=self.lobby_name, key="is_running")
        assert is_running == "1", is_running
        assert is_ready == False, is_ready

        is_ready = await self.instance._is_ready_to_play(1, True, False)
        is_running = redis_instance.hget(name=self.lobby_name, key="is_running")
        assert is_running == "1", is_running
        assert is_ready == True, is_ready

        is_ready = await self.instance._is_ready_to_play(1, True, True)
        is_running = redis_instance.hget(name=self.lobby_name, key="is_running")
        assert is_running == None, is_running
        assert is_ready == True, is_ready


class TestAddUserToGameMixin(APITransactionTestCase):
    """Testing the AddUserToGameMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.user_1 = user_models.User.objects.get(id=1)
        self.user_2 = user_models.User.objects.get(id=3)

        self.ser_user_1 = user_serializers.BaseUserSerializer(self.user_1).data
        self.ser_user_2 = user_serializers.BaseUserSerializer(self.user_2).data

        self.lobby_1 = models.Lobby.objects.get(id=1)
        self.lobby_2 = models.Lobby.objects.get(id=2)

        self.empty_board = models.Board.objects.get(lobby_id_id=2, user_id=None)

        self.instance = mixins.AddUserToGameMixin()

    async def test_is_lobby_free(self):
        """Testing the is_lobby_free method"""

        is_lobby_free = await self.instance.is_lobby_free(self.user_1, self.lobby_1)
        assert is_lobby_free == True, is_lobby_free

        is_lobby_free = await self.instance.is_lobby_free(self.user_2, self.lobby_1)
        assert is_lobby_free == False, is_lobby_free

        is_lobby_free = await self.instance.is_lobby_free(self.user_1, self.lobby_2)
        assert is_lobby_free == True, is_lobby_free

        is_lobby_free = await self.instance.is_lobby_free(self.user_2, self.lobby_2)
        assert is_lobby_free == True, is_lobby_free
    
    async def test_add_user_to_game(self):
        """Testing the _add_user_to_game method"""

        self.instance.lobby_name = str(self.lobby_1.slug)
        self.instance.user = self.user_1
        with self.assertNoLogs():
            ser_user = await self.instance._add_user_to_game(self.empty_board.id)
        assert ser_user == self.ser_user_1, ser_user

        self.instance.user = self.user_2
        with self.assertLogs():
            ser_user = await self.instance._add_user_to_game(self.empty_board.id)
        assert ser_user == None, ser_user

        self.instance.lobby_name = str(self.lobby_2.slug)
        self.instance.user = self.user_1
        with self.assertNoLogs():
            ser_user = await self.instance._add_user_to_game(self.empty_board.id)
        assert ser_user == self.ser_user_1, ser_user

        self.instance.user = self.user_2
        with self.assertNoLogs():
            ser_user = await self.instance._add_user_to_game(self.empty_board.id)
        assert ser_user == self.ser_user_2, ser_user


class TestSendMessageMixin(APITransactionTestCase):
    """Testing the SendMessageMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()

        self.user_1 = user_models.User.objects.get(id=1)
        self.user_2 = user_models.User.objects.get(id=2)

        self.instance = mixins.SendMessageMixin()

    async def test_send_message(self):
        """Testing the _send_message method"""

        self.instance.user = self.user_1
        response = await self.instance._send_message(1, "Test")
        assert response["type"] == "send_message", response["type"]
        assert response["message"]["owner"] == self.user_1.username, response["message"]["owner"]
        assert response["message"]["is_bot"] == False, response["message"]["is_bot"]

        response = await self.instance._send_message(1, "Test", True)
        assert response["type"] == "send_message", response["type"]
        assert response["message"]["owner"] == self.user_1.username, response["message"]["owner"]
        assert response["message"]["is_bot"] == True, response["message"]["is_bot"]

        self.instance.user = self.user_2
        response = await self.instance._send_message(1, "Test")
        assert response["type"] == "send_message", response["type"]
        assert response["message"]["owner"] == self.user_2.username, response["message"]["owner"]
        assert response["message"]["is_bot"] == False, response["message"]["is_bot"]
    
    async def test_preform_create_message(self):
        """Testing the preform_create_message method"""

        message_instance = await self.instance.preform_create_message(1, self.user_1.username, "Hi everyone!", False)
        assert message_instance.id == 4 , message_instance.id
        assert message_instance.owner == self.user_1.username, message_instance.owner
        assert message_instance.is_bot == False, message_instance.is_bot

        message_instance = await self.instance.preform_create_message(1, self.user_1.username, "Hi everyone!", True)
        assert message_instance.id == 5 , message_instance.id
        assert message_instance.owner == self.user_1.username, message_instance.owner
        assert message_instance.is_bot == True, message_instance.is_bot

        message_instance = await self.instance.preform_create_message(1, self.user_2.username, "Hi everyone!", False)
        assert message_instance.id == 6 , message_instance.id
        assert message_instance.owner == self.user_2.username, message_instance.owner
        assert message_instance.is_bot == False, message_instance.is_bot


class TestCreateNewGameMixin(APITransactionTestCase):
    """Testing the CreateNewGameMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()

        self.user = user_models.User.objects.get(id=1)
        self.lobby = models.Lobby.objects.get(id=1)

        self.ser_lobby = serializers.RetrieveLobbyWithUsersSerializer(self.lobby).data

        self.instance = mixins.CreateNewGameMixin()

    def test__create_new_game(self):
        """Testing the _create_new_game method"""

        name = self.instance._create_new_name("string")
        assert name == "string (1)", name

        name = self.instance._create_new_name("string (2)")
        assert name == "string (3)", name

        name = self.instance._create_new_name("(1) string test (2)")
        assert name == "(1) string test (3)", name
    
    async def test_create_new_game(self):
        """Testing the create_new_game method"""

        self.instance.user = self.user

        new_lobby_slug = await self.instance.create_new_game(30, "test", 30, 30, 2)
        new_lobby = await db_queries.get_lobby_by_slug(new_lobby_slug)
        new_board_list = await db_queries.get_lobby_boards(new_lobby_slug)
        assert new_lobby.name == "test (1)", new_lobby.name
        assert new_lobby.id == 3, new_lobby.id
        assert len(new_board_list) == 2, new_board_list

        new_lobby_slug = await self.instance.create_new_game(30, "(1) qwe test (3)", 30, 30, 2)
        new_lobby = await db_queries.get_lobby_by_slug(new_lobby_slug)
        new_board_list = await db_queries.get_lobby_boards(new_lobby_slug)
        assert new_lobby.name == "(1) qwe test (4)", new_lobby.name
        assert new_lobby.id == 4, new_lobby.id
        assert len(new_board_list) == 2, new_board_list
    
    async def test_get_new_game(self):
        """Testing the get_new_game method"""

        lobby = await self.instance.get_new_game(self.lobby.slug)
        assert lobby == self.ser_lobby, lobby


class TestCountDownTimerMixin(APITestCase):
    """Testing the CountDownTimerMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        info = f"{cls.__name__}: Number of keys in Redis database before running tests: {len(redis_instance.keys())}"
        logging.info(info)

        cls.lobby = models.Lobby.objects.get(id=1)
        cls.lobby_slug = str(cls.lobby.slug)

        cls.instance = mixins.CountDownTimerMixin()

        redis_instance.hset(name=cls.lobby_slug, mapping={"current_turn": 0, "is_running": 1, "time_left": 30})
    
    @classmethod
    def tearDownClass(cls) -> None:
        info = f"{cls.__name__}: Number of keys in Redis database before closing: {len(redis_instance.keys())}"
        logging.info(info)
        redis_instance.delete("celery", "_kombu.binding.celery", cls.lobby_slug)
        super().tearDownClass()

    async def test_countdown(self):
        """Testing the _countdown method"""

        resposne = await self.instance._countdown(self.lobby_slug, None)
        current_turn = redis_instance.hget(self.lobby_slug, "current_turn")
        is_task_in_progress = redis_instance.hget(self.lobby_slug, "is_running")
        assert resposne == {"type": "countdown", "time_left": 30}, resposne
        assert current_turn == "0", current_turn
        assert is_task_in_progress == "1", is_task_in_progress

        resposne = await self.instance._countdown(self.lobby_slug, 20)
        current_turn = redis_instance.hget(self.lobby_slug, "current_turn")
        assert resposne == {"type": "countdown", "time_left": 20}, resposne
        assert resposne["time_left"] == 20, resposne["time_left"]
        assert current_turn == "1", current_turn

        redis_instance.hdel(self.lobby_slug, "is_running")
        is_task_in_progress = redis_instance.hget(self.lobby_slug, "is_running")
        assert is_task_in_progress == None, is_task_in_progress

        resposne = await self.instance._countdown(self.lobby_slug, 15)
        current_turn = redis_instance.hget(self.lobby_slug, "current_turn")
        is_task_in_progress = redis_instance.hget(self.lobby_slug, "is_running")
        assert resposne == {"type": "countdown", "time_left": 15}, resposne
        assert current_turn == "2", current_turn
        assert is_task_in_progress == "1", is_task_in_progress

        resposne = await self.instance._countdown(self.lobby_slug, None)
        current_turn = redis_instance.hget(self.lobby_slug, "current_turn")
        is_task_in_progress = redis_instance.hget(self.lobby_slug, "is_running")
        assert resposne == {"type": "countdown", "time_left": 30}, resposne
        assert current_turn == "2", current_turn
        assert is_task_in_progress == "1", is_task_in_progress


class TestTakeShotMixin(APITransactionTestCase):
    """Testing the TakeShotMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()

        self.lobby = models.Lobby.objects.prefetch_related("users", "boards").get(id=1)
        self.board_1, self.board_2 = self.lobby.boards.all()
        self.user_2, self.user_1 = self.lobby.users.all()

        self.ser_board = serializers.BoardSerializer(self.board_1).data
        self.board = {key: value for key, value in self.ser_board.items() if key in column_name_list}
        self.lobby_slug = str(self.lobby.slug)

        self.instance = mixins.TakeShotMixin()

    def test_get_type_shot(self):
        """Testing the _get_type_shot method"""

        type_shot = self.instance._get_type_shot(self.board, "I4")
        assert type_shot == "hit"

        type_shot = self.instance._get_type_shot(self.board, "A1")
        assert type_shot == "miss"

        type_shot = self.instance._get_type_shot(self.board, "A2")
        assert type_shot == "miss"

        type_shot = self.instance._get_type_shot(self.board, "A1")
        assert type_shot == "miss"
    
    def test_shot(self):
        """Testing the _shot method"""

        assert self.ser_board["F"]["F1"] == " space 19.1", self.board["F"]["F1"]
        assert self.ser_board["A"]["A1"] == "", self.ser_board["A"]["A1"]
        assert self.ser_board["G"]["G9"] == 1.1, self.ser_board["G"]["G9"]

        field_value = self.instance._shot(self.board, "F1", "miss")
        assert field_value == " space 19.1", field_value
        assert self.board["F"]["F1"] == "miss", self.board["F"]["F1"]

        field_value = self.instance._shot(self.board, "A1", "miss")
        assert field_value == "", field_value
        assert self.board["A"]["A1"] == "miss", self.board["A"]["A1"]

        field_value = self.instance._shot(self.board, "G9", "hit")
        assert field_value == 1.1, field_value
        assert self.board["G"]["G9"] == "hit", self.board["G"]["G9"]

    def test_is_ship_has_sunk(self):
        """Testing the _is_ship_has_sunk method"""

        is_ship_has_sunk = self.instance._is_ship_has_sunk(1.1, self.board)
        assert is_ship_has_sunk == False, is_ship_has_sunk

        is_ship_has_sunk = self.instance._is_ship_has_sunk(4.1, self.board)
        assert is_ship_has_sunk == True, is_ship_has_sunk

        self.board["G"]["G9"] = "hit"

        is_ship_has_sunk = self.instance._is_ship_has_sunk(1.1, self.board)
        assert is_ship_has_sunk == True, is_ship_has_sunk
    
    def test_add_misses_around_sunken_ship(self):
        """Testing the _add_misses_around_sunken_ship method"""

        test_data = {"F8": "miss", "F9": "miss", "F10": "miss", "G8": "miss", 
                     "G10": "miss", "H8": "miss", "H9": "miss", "H10": "miss"}

        assert self.ser_board["G"]["G8"] == " space 1.1", self.board["G"]["G8"]
        assert self.ser_board["F"]["F8"] == " space 1.1", self.ser_board["F"]["F8"]
        assert self.ser_board["G"]["G9"] == 1.1, self.ser_board["G"]["G9"]

        field_name_dict = self.instance._add_misses_around_sunken_ship(1.1, self.board)
        assert field_name_dict == test_data, field_name_dict
        assert self.ser_board["G"]["G8"] == "miss", self.board["G"]["G8"]
        assert self.ser_board["F"]["F8"] == "miss", self.ser_board["F"]["F8"]
        assert self.ser_board["G"]["G9"] == 1.1, self.ser_board["G"]["G9"]

        field_name_dict = self.instance._add_misses_around_sunken_ship(4.1, self.board)
        assert field_name_dict == {} 
    
    async def test_take_shot(self):
        """Testing the take_shot method"""

        self.instance.column_name_list = column_name_list
        self.instance.user = self.user_1
        assert self.board_1.A[1:29] == "'A1': '', 'A2': ' space 7.1'", self.board_1.A[1:29]

        response = await self.instance.take_shot(self.lobby_slug, self.board_1.id, "A1")
        updated_board_1 = await database_sync_to_async(models.Board.objects.get)(id=1)
        updated_board_2 = await database_sync_to_async(models.Board.objects.get)(id=2)
        assert response == (False, {"A1": "miss"}, None), response
        assert self.board_1.is_my_turn != updated_board_1.is_my_turn, updated_board_1.is_my_turn
        assert self.board_2.is_my_turn != updated_board_2.is_my_turn, updated_board_2.is_my_turn
        assert self.board_1.is_my_turn == updated_board_2.is_my_turn, updated_board_2.is_my_turn
        assert updated_board_1.A[1:33] == "'A1': 'miss', 'A2': ' space 7.1'", updated_board_1.A[1:33]
        assert updated_board_1.A[1:33] != self.board_1.A[1:33], updated_board_1.A[1:33]

        self.instance.user = self.user_2
        assert self.board_2.A[1:32] == "'A1': ' space 26.3', 'A2': 26.3", self.board_2.A[1:32]

        response = await self.instance.take_shot(self.lobby_slug, self.board_2.id, "A1")
        updated_board_1 = await database_sync_to_async(models.Board.objects.get)(id=1)
        updated_board_2 = await database_sync_to_async(models.Board.objects.get)(id=2)
        assert response == (False, {"A1": "miss"}, None), response
        assert self.board_1.is_my_turn == updated_board_1.is_my_turn, updated_board_1.is_my_turn
        assert self.board_2.is_my_turn == updated_board_2.is_my_turn, updated_board_2.is_my_turn
        assert self.board_1.is_my_turn != updated_board_2.is_my_turn, updated_board_2.is_my_turn
        assert updated_board_2.A[1:25] == "'A1': 'miss', 'A2': 26.3", updated_board_2.A[1:25]
        assert updated_board_2.A[1:25] != self.board_1.A[1:25], updated_board_2.A[1:25]

        self.instance.suer = self.user_2
        assert self.board_1.C[1:50] == "'C1': 1.2, 'C2': ' space 1.2 space 7.1 space 7.3'", self.board_1.C[1:50]

        response = await self.instance.take_shot(self.lobby_slug, self.board_1.id, "C1")
        updated_board_1 = await database_sync_to_async(models.Board.objects.get)(id=1)
        updated_board_2 = await database_sync_to_async(models.Board.objects.get)(id=2)
        assert response == (True, {'C1': 'hit', 'B1': 'miss', 'B2': 'miss', 'C2': 'miss', 'D1': 'miss', 'D2': 'miss'}, 9), response
        assert self.board_1.is_my_turn == updated_board_1.is_my_turn, updated_board_1.is_my_turn
        assert self.board_2.is_my_turn == updated_board_2.is_my_turn, updated_board_2.is_my_turn
        assert self.board_1.is_my_turn != updated_board_2.is_my_turn, updated_board_2.is_my_turn
        assert updated_board_1.C[1:26] == "'C1': 'hit', 'C2': 'miss'", updated_board_1.C[1:26]
        assert updated_board_1.C[1:26] != self.board_1.C[1:26], updated_board_1.C[1:26]

        assert self.board_1.H[1:32] == "'H1': 19.1, 'H2': ' space 19.1'", self.board_1.H[1:32]

        response = await self.instance.take_shot(self.lobby_slug, self.board_1.id, "H1")
        updated_board_1 = await database_sync_to_async(models.Board.objects.get)(id=1)
        updated_board_2 = await database_sync_to_async(models.Board.objects.get)(id=2)
        assert response == (True, {'H1': 'hit'}, None), response
        assert self.board_1.is_my_turn == updated_board_1.is_my_turn, updated_board_1.is_my_turn
        assert self.board_2.is_my_turn == updated_board_2.is_my_turn, updated_board_2.is_my_turn
        assert self.board_1.is_my_turn != updated_board_2.is_my_turn, updated_board_2.is_my_turn
        assert updated_board_1.H[1:33] == "'H1': 'hit', 'H2': ' space 19.1'", updated_board_1.H[1:33]
        assert updated_board_1.H[1:33] != self.board_1.H[1:33], updated_board_1.H[1:33]


class TestRandomPlacementMixin(APITestCase):
    """Testing the RandomPlacementMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()

        self.db_board = models.Board.objects.get(id=1)
        self.db_ships = models.Ship.objects.filter(board_id=1)

        self.ships = serializers.ShipSerializer(self.db_ships, many=True).data
        self.ser_board = serializers.BoardSerializer(self.db_board).data
        self.board = {key: value for key, value in self.ser_board.items() if key in column_name_list}

        self.instance = mixins.RandomPlacementMixin()
        self.instance.column_name_list = column_name_list
        self.instance.string_number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.instance.ship_count_dict = ship_count_dict

    def test_is_put_on_board(self):
        """Testing the _is_put_on_board method"""

        is_put = self.instance._is_put_on_board(["A1", "A2", "A3"], self.board)
        assert is_put == False

        is_put = self.instance._is_put_on_board(["G3", "G4", "G5"], self.board)
        assert is_put == True

        is_put = self.instance._is_put_on_board(["A1"], self.board)
        assert is_put == True

        is_put = self.instance._is_put_on_board(["A3"], self.board)
        assert is_put == False

    def test_put_ship_on_board(self):
        """Testing the _put_ship_on_board method"""

        test_data = (self.board["F"]["F6"], self.board["G"]["G6"], self.board["H"]["H6"])
        assert test_data == ("", "", ""), test_data

        self.instance._put_ship_on_board(3, 1, ["F6", "G6", "H6"], self.board)
        test_data = (self.board["F"]["F6"], self.board["G"]["G6"], self.board["H"]["H6"])
        assert test_data == (3.1, 3.1, 3.1), test_data

        self.instance._put_ship_on_board(1, 4, ["G3", "G4", "G5"], self.board)
        test_data = (self.board["G"]["G3"], self.board["G"]["G4"], self.board["G"]["G5"])
        assert test_data == (1.4, 1.4, 1.4), test_data
    
    def test_get_field_list_horizontally(self):
        """Testing the get_field_list_horizontally method"""

        field_list = self.instance.get_field_list_horizontally(3, "A", 3, column_name_list)
        assert field_list == ["A3", "B3", "C3"]

        field_list = self.instance.get_field_list_horizontally(3, "J", 3, column_name_list)
        assert field_list == ["J3", "I3", "H3"]

        field_list = self.instance.get_field_list_horizontally(3, "I", 3, column_name_list)
        assert field_list == ["I3", "H3", "G3"]
    
    def test_get_field_list_vertically(self):
        """Testing the get_field_list_vertically method"""

        field_list = self.instance.get_field_list_vertically(1, "A", 3)
        assert field_list == ["A1", "A2", "A3"]

        field_list = self.instance.get_field_list_vertically(10, "A", 3)
        assert field_list == ["A10", "A9", "A8"]

        field_list = self.instance.get_field_list_vertically(9, "E", 3)
        assert field_list == ["E9", "E8", "E7"]
    
    async def test_get_field_list(self):
        """Testing the get_field_list method"""

        old_board = deepcopy(self.board)

        with self.assertLogs():
            new_board = await self.instance.get_field_list("horizontal", 4, self.board, self.ships)
        assert type(new_board) == dict
        assert new_board == self.board
        assert new_board != old_board
    
    async def test_random_placement(self):
        """Testing the random_placement method"""

        old_board = deepcopy(self.board)

        with self.assertLogs():
            new_board = await self.instance.get_field_list("horizontal", 4, self.board, self.ships)
        assert type(new_board) == dict
        assert new_board == self.board
        assert new_board != old_board

        is_full = sum(1 for column_name in column_name_list if new_board[column_name][f"{column_name}1"])
        assert is_full > 0


class TestChooseWhoWillShotFirstMixin(APITransactionTestCase):
    """Testing the ChooseWhoWillShotFirstMixin class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.user_1 = user_models.User.objects.get(id=1)

        self.lobby_1 = models.Lobby.objects.get(id=1)
        self.lobby_2 = models.Lobby.objects.get(id=2)

        self.board_1 = models.Board.objects.get(id=1)
        self.board_2 = models.Board.objects.get(id=2)
        self.board_3 = models.Board.objects.get(id=3)
        self.board_4 = models.Board.objects.get(id=4)

        self.lobby_1_slug = str(self.lobby_1.slug)
        self.lobby_2_slug = str(self.lobby_2.slug)

        self.instance = mixins.ChooseWhoWillShotFirstMixin()
        self.instance.user = self.user_1

    async def test_is_turn_determined(self):
        """Testing the is_turn_determined method"""

        is_turn_determined = await self.instance.is_turn_determined(self.board_1, self.board_2)
        assert is_turn_determined == True, is_turn_determined

        is_turn_determined = await self.instance.is_turn_determined(self.board_3, self.board_4)
        assert is_turn_determined == False, is_turn_determined

    async def test_choose_first_shooter(self):
        """Testing the choose_first_shooter method"""

        response = await self.instance.choose_first_shooter(self.lobby_1_slug)
        assert response is None, response

        response = await self.instance.choose_first_shooter(self.lobby_2_slug)
        assert type(response) == bool, response
