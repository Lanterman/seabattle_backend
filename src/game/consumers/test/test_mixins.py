import re
import pytest

from copy import deepcopy

from .data import board, ships, column_name_list
from src.game.consumers import services, mixins


@pytest.fixture
def copy_board():
    return deepcopy(board)


@pytest.fixture
def copy_ships():
     return deepcopy(ships)


class TestRefreshBoardMixin:
    """Testing RefreshBoardMixin class methods"""
    
    def test_clear_board(self, copy_board: dict):
        """Testing _clear_board method"""

        assert copy_board["A"]["A1"] == 27.4, copy_board["A"]["A1"]

        field_name_list = mixins.RefreshBoardMixin._clear_board(copy_board)

        assert len(field_name_list) == 96, len(field_name_list)
        assert copy_board != board, copy_board
        assert board["A"]["A1"] == 27.4, board["A"]["A1"]
        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]


class TestDropShipOnBoardMixin:
    """Testing DropShipOnBoardMixin class methods"""

    def test_drop_ship_on_board(self, copy_board: dict):
        """Testing drop_ship_on_board method"""

        assert copy_board == board

        services.clear_board(copy_board)
        mixins.DropShipOnBoardMixin.drop_ship_on_board(ships[0]["id"], ships[0]["count"], 
                                                       ["F1", "G1", "H1", "I1"], copy_board)
        assert copy_board != board
        assert board["G"]["G1"] == 27.1


class TestAddSpaceAroundShipMixin:
    """Testing AddSpaceAroundShipMixin class methods"""

    @pytest.fixture(autouse=True)
    def instance(self):
        _instance = mixins.AddSpaceAroundShipMixin()
        _instance.column_name_list = column_name_list
        return _instance

    def test_insert_space_around_ship(self, copy_board: dict, instance: mixins.AddSpaceAroundShipMixin):
        """Testing insert_space_around_ship method"""

        assert copy_board == board

        services.clear_board(copy_board)
        instance.insert_space_around_ship(f" space 27.4", "horizontal", ["F1", "G1", "H1", "I1"], copy_board)
        assert copy_board != board
        assert copy_board["G"]["G2"] == " space 27.4"
        assert copy_board["E"]["E2"] == " space 27.4"
        assert copy_board["H"]["H2"] == " space 27.4"
        assert copy_board["F"]["F5"] == ""

        services.clear_board(copy_board)
        instance.insert_space_around_ship(f" space 27.3", "vertical", ["F1", "F2", "F3", "F4"], copy_board)
        assert copy_board != board
        assert copy_board["G"]["G2"] == " space 27.3"
        assert copy_board["F"]["F5"] == " space 27.3"
        assert copy_board["H"]["H2"] == ""

        instance.insert_space_around_ship(f" space 27.2", "vertical", ["H1", "H2", "H3", "H4"], copy_board)
        assert copy_board != board
        assert copy_board["G"]["G2"] == " space 27.3 space 27.2"
        assert copy_board["I"]["I5"] == " space 27.2"
        assert copy_board["H"]["H2"] == ""


class TestIsReadyToPlayMixin:
    """Testing IsReadyToPlayMixin class methods"""

    def test_ready_to_play(self):
        """Testing ready_to_play method"""


class TestAddUserToGameMixin:
    """Testing AddUserToGameMixin class methods"""

    def test_is_lobby_free(self):
        """Testing is_lobby_free method"""
    
    def test_add_user_to_game(self):
        """Testing _add_user_to_game method"""


class TestSendMessageMixin:
    """Testing SendMessageMixin class methods"""

    def test_send_message(self):
        """Testing _send_message method"""


class TestCreateNewGameMixin:
    """Testing CreateNewGameMixin class methods"""

    @pytest.fixture(autouse=True)
    def instance(self):
        _instance = mixins.CreateNewGameMixin()
        return _instance

    def test__create_new_game(self, instance: mixins.CreateNewGameMixin):
        """Testing _create_new_game method"""

        name = instance._create_new_name("string")
        assert name == "string (1)"

        name = instance._create_new_name("string (2)")
        assert name == "string (3)"

        name = instance._create_new_name("(1) string test (2)")
        assert name == "(1) string test (3)"
    
    def test_create_new_game(self):
        """Testing create_new_game method"""


class TestCountDownTimerMixin:
    """Testing CountDownTimerMixin class methods"""

    def test_countdown(self):
        """Testing _countdown method"""


class TestTakeShotMixin:
    """Testing TakeShotMixin class methods"""

    @pytest.fixture(autouse=True)
    def instance(self):
        _instance = mixins.TakeShotMixin()
        return _instance

    def test_get_type_shot(self, copy_board: dict, instance: mixins.TakeShotMixin):
        """Testing _get_type_shot method"""

        type_shot = instance._get_type_shot(copy_board, "F1")
        assert type_shot == "hit"

        type_shot = instance._get_type_shot(copy_board, "A5")
        assert type_shot == "miss"

        type_shot = instance._get_type_shot(copy_board, "F2")
        assert type_shot == "miss"
    
    def test_shot(self, copy_board, instance: mixins.TakeShotMixin):
        """Testing _shot method"""

        assert copy_board["F"]["F1"] == 27.1
        assert copy_board["A"]["A5"] == ""
        assert copy_board["F"]["F2"] == " space 27.1 space 33.1"

        field_value = instance._shot(copy_board, "F1", "hit")
        assert field_value == 27.1
        assert copy_board["F"]["F1"] == "hit"

        field_value = instance._shot(copy_board, "A5", "miss")
        assert field_value == ""
        assert copy_board["A"]["A5"] == "miss"

        field_value = instance._shot(copy_board, "F2", "miss")
        assert field_value == " space 27.1 space 33.1"
        assert copy_board["F"]["F2"] == "miss"

    def test_is_ship_has_sunk(self, copy_board, instance: mixins.TakeShotMixin):
        """Testing _is_ship_has_sunk method"""

        is_ship_has_sunk = instance._is_ship_has_sunk(45.1, copy_board)
        assert is_ship_has_sunk == False

        copy_board["H"]["H10"] = "hit"

        is_ship_has_sunk = instance._is_ship_has_sunk(45.1, copy_board)
        assert is_ship_has_sunk == True

        is_ship_has_sunk = instance._is_ship_has_sunk(45.4, copy_board)
        assert is_ship_has_sunk == True
    
    def test_add_misses_around_sunken_ship(self, copy_board, instance: mixins.TakeShotMixin):
        """Testing _add_misses_around_sunken_ship method"""

        test_data_dict = {
            "G9": " space 27.2 space 45.1", 
            "G10": " space 27.2 space 45.1", 
            "H9": " space 45.1", 
            "I9": " space 33.2 space 45.1", 
            "I10": " space 45.1"
        }
        test_data_value = (
            copy_board["G"]["G9"], 
            copy_board["G"]["G9"], 
            copy_board["H"]["H9"], 
            copy_board["I"]["I9"], 
            copy_board["I"]["I10"]
        )

        assert test_data_value == tuple(value for value in test_data_dict.values())

        for key in test_data_dict:
            test_data_dict[key] = "miss"

        field_name_dict = instance._add_misses_around_sunken_ship(45.1, copy_board)
        assert field_name_dict == test_data_dict
        assert (copy_board["G"]["G9"], copy_board["H"]["H9"]) == ("miss", "miss")

        field_name_dict = instance._add_misses_around_sunken_ship(45.3, copy_board)
        assert field_name_dict == {} 
    
    def test_take_shot(self):
        """Testing take_shot method"""


class TestRandomPlacementMixin:
    """Testing RandomPlacementMixin class methods"""

    @pytest.fixture(autouse=True)
    def instance(self):
        ins = mixins.RandomPlacementMixin()
        ins.column_name_list = column_name_list
        ins.string_number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ins.ship_count_tuple = (4, 3, 2, 1)
        return ins

    def test_is_put_on_board(self, copy_board: dict, instance: mixins.RandomPlacementMixin):
        """Testing _is_put_on_board method"""

        is_put = instance._is_put_on_board(["A1", "A2", "A3"], copy_board)
        assert is_put == False

        is_put = instance._is_put_on_board(["A5", "A6", "A7"], copy_board)
        assert is_put == True
    
        is_put = instance._is_put_on_board(["J10"], copy_board)
        assert is_put == True

        is_put = instance._is_put_on_board(["B5"], copy_board)
        assert is_put == False

    def test_put_ship_on_board(self, copy_board: dict, instance: mixins.RandomPlacementMixin):
        """Testing _put_ship_on_board method"""

        assert (copy_board["A"]["A5"], copy_board["A"]["A6"], copy_board["A"]["A7"]) == ("", "", "")

        instance._put_ship_on_board(3, 1, ["A5", "A6", "A7"], copy_board)

        assert (copy_board["A"]["A5"], copy_board["A"]["A6"], copy_board["A"]["A7"]) == (3.1, 3.1, 3.1)
    
    def test_get_field_list_horizontally(self, instance: mixins.RandomPlacementMixin):
        """Testing get_field_list_horizontally method"""

        field_list = instance.get_field_list_horizontally(3, "A", 3, column_name_list)
        assert field_list == ["A3", "B3", "C3"]

        field_list = instance.get_field_list_horizontally(3, "J", 3, column_name_list)
        assert field_list == ["J3", "I3", "H3"]

        field_list = instance.get_field_list_horizontally(3, "I", 3, column_name_list)
        assert field_list == ["I3", "H3", "G3"]
    
    def test_get_field_list_vertically(self, instance: mixins.RandomPlacementMixin):
        """Testing get_field_list_vertically method"""

        field_list = instance.get_field_list_vertically(1, "A", 3)
        assert field_list == ["A1", "A2", "A3"]

        field_list = instance.get_field_list_vertically(10, "A", 3)
        assert field_list == ["A10", "A9", "A8"]

        field_list = instance.get_field_list_vertically(9, "E", 3)
        assert field_list == ["E9", "E8", "E7"]
    
    @pytest.mark.asyncio
    async def test_get_field_list(self, copy_board: dict, copy_ships: list, instance: mixins.RandomPlacementMixin):
        """Testing get_field_list method"""

        old_board = deepcopy(copy_board)

        new_board = await instance.get_field_list("horizontal", 4, copy_board, copy_ships)
        assert type(new_board) == dict
        assert new_board == copy_board
        assert new_board != old_board
    
    @pytest.mark.asyncio
    async def test_random_placement(self, copy_board: dict, copy_ships: list, instance: mixins.RandomPlacementMixin):
        """Testing random_placement method"""

        old_board = deepcopy(copy_board)

        new_board = await instance.get_field_list("horizontal", 4, copy_board, copy_ships)
        assert type(new_board) == dict
        assert new_board == copy_board
        assert new_board != old_board

        is_full = sum(1 for column_name in column_name_list if new_board[column_name][f"{column_name}1"])
        assert is_full > 0


class TestChooseWhoWillShotFirstMixin:
    """Testing ChooseWhoWillShotFirstMixin class methods"""

    def test_is_turn_determined(self):
        """Testing is_turn_determined method"""

    def test_choose_first_shooter(self):
        """Testing choose_first_shooter method"""
    