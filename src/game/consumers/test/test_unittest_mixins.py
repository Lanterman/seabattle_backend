import logging

from copy import deepcopy
from rest_framework.test import APITestCase, APITransactionTestCase

from src.game import models, serializers
from src.user import models as user_models, serializers as user_serializers
from src.game.consumers import services, mixins, db_queries
from .test_data import column_name_list
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
        field_name_list = self.instance._clear_board(board)
        assert len(field_name_list) == 85, len(field_name_list)
        assert self.ser_board_1["A"]["A2"] == "", self.ser_board_1["A"]["A2"]

        board = {key: value for key, value in self.ser_board_2.items() if key in column_name_list}
        field_name_list = self.instance._clear_board(board)
        assert len(field_name_list) == 93, len(field_name_list)
        assert self.ser_board_2["A"]["A2"] == "", self.ser_board_2["A"]["A2"]

        board = {key: value for key, value in self.ser_board_3.items() if key in column_name_list}
        field_name_list = self.instance._clear_board(board)
        assert len(field_name_list) == 97, len(field_name_list)
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
        self.instance.ship_count_tuple = (1, 2, 3, 4)

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
        logging.warning(f"Number of keys in Redis database before running tests: {len(redis_instance.keys())}")

        self.lobby = models.Lobby.objects.get(id=1)

        self.instance = mixins.IsReadyToPlayMixin()
        self.lobby_name = str(self.lobby.slug)
        self.instance.lobby_name = self.lobby_name

        redis_instance.hset(name=self.lobby_name, mapping={"is_running": 1})
    
    def tearDown(self) -> None:
        logging.info(f"Number of keys in Redis database before closing: {len(redis_instance.keys())}")
        redis_instance.flushall()
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
        ser_user = await self.instance._add_user_to_game(self.empty_board.id)
        assert ser_user == self.ser_user_1, ser_user

        self.instance.user = self.user_2
        ser_user = await self.instance._add_user_to_game(self.empty_board.id)
        assert ser_user == None, ser_user

        self.instance.lobby_name = str(self.lobby_2.slug)
        self.instance.user = self.user_1
        ser_user = await self.instance._add_user_to_game(self.empty_board.id)
        assert ser_user == self.ser_user_1, ser_user

        self.instance.user = self.user_2
        ser_user = await self.instance._add_user_to_game(self.empty_board.id)
        assert ser_user == self.ser_user_2, ser_user
        assert 1 == 2, "asserWarngs (self::test_add_user_to_game, views::test_url_of_unauthenticated_user && test_is_lobby_not_free)"

# class TestSendMessageMixin:
#     """Testing the SendMessageMixin class methods"""

#     def test_send_message(self):
#         """Testing the _send_message method"""


# class TestCreateNewGameMixin:
#     """Testing the CreateNewGameMixin class methods"""

#     @pytest.fixture(autouse=True)
#     def instance(self):
#         _instance = mixins.CreateNewGameMixin()
#         return _instance

#     @pytest.mark.parametrize(
#             "test_input, output", 
#             [("string", "string (1)"), ("string (2)", "string (3)"), ("(1) string test (2)", "(1) string test (3)")]
#     )
#     def test__create_new_game(self, test_input: str, output: str, instance: mixins.CreateNewGameMixin):
#         """Testing the _create_new_game method"""

#         name = instance._create_new_name(test_input)
#         assert name == output
    
#     def test_create_new_game(self):
#         """Testing the create_new_game method"""


# class TestCountDownTimerMixin:
#     """Testing the CountDownTimerMixin class methods"""

#     def test_countdown(self):
#         """Testing the _countdown method"""


# class TestTakeShotMixin:
#     """Testing the TakeShotMixin class methods"""

#     @pytest.fixture(autouse=True)
#     def instance(self):
#         _instance = mixins.TakeShotMixin()
#         return _instance

#     @pytest.mark.parametrize("test_input, output", [("F1", "hit"), ("A5", "miss"), ("F2", "miss")])
#     def test_get_type_shot(self, copy_board: dict, test_input: str, output: str, instance: mixins.TakeShotMixin):
#         """Testing the _get_type_shot method"""

#         type_shot = instance._get_type_shot(copy_board, test_input)
#         assert type_shot == output
    
#     @pytest.mark.parametrize(
#         "test_input, output", 
#         [
#             (("F1", "hit"), ("F1", 27.1, "hit")), 
#             (("A5", "miss"), ("A5", "", "miss")), 
#             (("F2", "miss"), ("F2", " space 27.1 space 33.1", "miss"))
#         ]
#     )
#     def test_shot(self, test_input: tuple, output: tuple, copy_board: dict, instance: mixins.TakeShotMixin):
#         """Testing the _shot method"""

#         assert copy_board[output[0][0]][output[0]] == output[1]

#         field_value = instance._shot(copy_board, *test_input)
#         assert field_value == output[1]
#         assert copy_board[output[0][0]][output[0]] == output[2]

#     @pytest.mark.parametrize("test_input, output", [(45.1, (False,)), (45.1, ("hit", True)), (45.4, (True,))])
#     def test_is_ship_has_sunk(self, test_input: float, output: bool, copy_board: dict, instance: mixins.TakeShotMixin):
#         """Testing the _is_ship_has_sunk method"""

#         if len(output) == 2: copy_board["H"]["H10"] = output[0]

#         is_ship_has_sunk = instance._is_ship_has_sunk(test_input, copy_board)
#         assert is_ship_has_sunk == output[-1]
    
#     def test_add_misses_around_sunken_ship(self, copy_board: dict, instance: mixins.TakeShotMixin):
#         """Testing the _add_misses_around_sunken_ship method"""

#         test_data_dict = {
#             "G9": " space 27.2 space 45.1", 
#             "G10": " space 27.2 space 45.1", 
#             "H9": " space 45.1", 
#             "I9": " space 33.2 space 45.1", 
#             "I10": " space 45.1"
#         }
#         test_data_value = (
#             copy_board["G"]["G9"], 
#             copy_board["G"]["G9"], 
#             copy_board["H"]["H9"], 
#             copy_board["I"]["I9"], 
#             copy_board["I"]["I10"]
#         )

#         assert test_data_value == tuple(value for value in test_data_dict.values())

#         for key in test_data_dict:
#             test_data_dict[key] = "miss"

#         field_name_dict = instance._add_misses_around_sunken_ship(45.1, copy_board)
#         assert field_name_dict == test_data_dict
#         assert (copy_board["G"]["G9"], copy_board["H"]["H9"]) == ("miss", "miss")

#         field_name_dict = instance._add_misses_around_sunken_ship(45.3, copy_board)
#         assert field_name_dict == {} 
    
#     def test_take_shot(self):
#         """Testing the take_shot method"""


# class TestRandomPlacementMixin:
#     """Testing the RandomPlacementMixin class methods"""

#     @pytest.fixture(autouse=True)
#     def instance(self):
#         ins = mixins.RandomPlacementMixin()
#         ins.column_name_list = column_name_list
#         ins.string_number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#         ins.ship_count_tuple = (4, 3, 2, 1)
#         return ins

#     @pytest.mark.parametrize(
#         "test_input, output", 
#         [(["A1", "A2", "A3"], False), (["A5", "A6", "A7"], True), (["J10"], True), (["B5"], False)]
#     )
#     def test_is_put_on_board(
#         self, test_input: list, output: bool, copy_board: dict, instance: mixins.RandomPlacementMixin
#     ):
#         """Testing the _is_put_on_board method"""

#         is_put = instance._is_put_on_board(test_input, copy_board)
#         assert is_put == output

#     def test_put_ship_on_board(self, copy_board: dict, instance: mixins.RandomPlacementMixin):
#         """Testing the _put_ship_on_board method"""

#         assert (copy_board["A"]["A5"], copy_board["A"]["A6"], copy_board["A"]["A7"]) == ("", "", "")

#         instance._put_ship_on_board(3, 1, ["A5", "A6", "A7"], copy_board)

#         assert (copy_board["A"]["A5"], copy_board["A"]["A6"], copy_board["A"]["A7"]) == (3.1, 3.1, 3.1)
    
#     @pytest.mark.parametrize(
#         "test_input, output", 
#         [
#             ((3, "A", 3, column_name_list), ["A3", "B3", "C3"]), 
#             ((3, "J", 3, column_name_list), ["J3", "I3", "H3"]),
#             ((3, "I", 3, column_name_list), ["I3", "H3", "G3"])
#         ]
#     )
#     def test_get_field_list_horizontally(self, test_input: tuple, output: list, instance: mixins.RandomPlacementMixin):
#         """Testing the get_field_list_horizontally method"""

#         field_list = instance.get_field_list_horizontally(*test_input)
#         assert field_list == output
    
#     @pytest.mark.parametrize(
#         "test_input, output", 
#         [
#             ((1, "A", 3), ["A1", "A2", "A3"]), 
#             ((10, "A", 3), ["A10", "A9", "A8"]), 
#             ((9, "E", 3), ["E9", "E8", "E7"])
#         ]
#     )
#     def test_get_field_list_vertically(self, test_input: tuple, output: list, instance: mixins.RandomPlacementMixin):
#         """Testing the get_field_list_vertically method"""

#         field_list = instance.get_field_list_vertically(*test_input)
#         assert field_list == output
    
#     @pytest.mark.asyncio
#     async def test_get_field_list(self, copy_board: dict, copy_ships: list, instance: mixins.RandomPlacementMixin):
#         """Testing the get_field_list method"""

#         old_board = deepcopy(copy_board)

#         new_board = await instance.get_field_list("horizontal", 4, copy_board, copy_ships)
#         assert type(new_board) == dict
#         assert new_board == copy_board
#         assert new_board != old_board
    
#     @pytest.mark.asyncio
#     async def test_random_placement(self, copy_board: dict, copy_ships: list, instance: mixins.RandomPlacementMixin):
#         """Testing the random_placement method"""

#         old_board = deepcopy(copy_board)

#         new_board = await instance.get_field_list("horizontal", 4, copy_board, copy_ships)
#         assert type(new_board) == dict
#         assert new_board == copy_board
#         assert new_board != old_board

#         is_full = sum(1 for column_name in column_name_list if new_board[column_name][f"{column_name}1"])
#         assert is_full > 0


# class TestChooseWhoWillShotFirstMixin:
#     """Testing the ChooseWhoWillShotFirstMixin class methods"""

#     def test_is_turn_determined(self):
#         """Testing the is_turn_determined method"""

#     def test_choose_first_shooter(self):
#         """Testing the choose_first_shooter method"""
    