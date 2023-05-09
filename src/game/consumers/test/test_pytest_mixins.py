import pytest

from copy import deepcopy

from .test_data import board, ships, column_name_list, ship_count_dict
from src.game.consumers import services, mixins


@pytest.fixture
def copy_board():
    return deepcopy(board)


@pytest.fixture
def copy_ships():
     return deepcopy(ships)


class TestRefreshBoardMixin:
    """Testing the RefreshBoardMixin class methods"""
    
    @pytest.mark.parametrize("test_input, output", [("A1", 27.4), ("B3", 27.3), ("B9", 33.3)])
    def test_clear_board(self, copy_board: dict, test_input: str, output: float):
        """Testing the _clear_board method"""

        assert copy_board[test_input[0]][test_input] == output, copy_board[test_input[0]][test_input]

        mixins.RefreshBoardMixin._clear_board(copy_board)

        assert copy_board != board, copy_board
        assert board[test_input[0]][test_input] == output, board[test_input[0]][test_input]
        assert copy_board[test_input[0]][test_input] == "", copy_board[test_input[0]][test_input]


class TestDropShipOnBoardMixin:
    """Testing the DropShipOnBoardMixin class methods"""

    def test_drop_ship_on_board(self, copy_board: dict):
        """Testing the drop_ship_on_board method"""

        assert copy_board == board

        services.clear_board(copy_board)
        mixins.DropShipOnBoardMixin.drop_ship_on_board(ships[0]["id"], ships[0]["count"], 
                                                       ["F1", "G1", "H1", "I1"], copy_board)
        assert copy_board != board
        assert board["G"]["G1"] == 27.1


class TestAddSpaceAroundShipMixin:
    """Testing the AddSpaceAroundShipMixin class methods"""

    @pytest.fixture(autouse=True)
    def instance(self):
        _instance = mixins.AddSpaceAroundShipMixin()
        _instance.column_name_list = column_name_list
        return _instance

    @pytest.mark.parametrize(
        "test_input, output", 
        [
            ((f" space 27.4", "horizontal", ["F1", "G1", "H1", "I1"]), (" space 27.4", "", " space 27.4")), 
            ((f" space 27.3", "vertical", ["F1", "F2", "F3", "F4"]), (" space 27.3", " space 27.3", "")), 
            ((f" space 27.2", "vertical", ["H1", "H2", "H3", "H4"]), (" space 27.2", "", ""))
        ]
    )
    def test_insert_space_around_ship(
        self, test_input: tuple, output: tuple, copy_board: dict, instance: mixins.AddSpaceAroundShipMixin
    ):
        """Testing the insert_space_around_ship method"""

        assert copy_board == board

        services.clear_board(copy_board)
        instance.insert_space_around_ship(board=copy_board, *test_input)
        assert copy_board != board
        assert copy_board["G"]["G2"] == output[0]
        assert copy_board["F"]["F5"] == output[1]
        assert copy_board["H"]["H2"] == output[2]


class TestCreateNewGameMixin:
    """Testing the CreateNewGameMixin class methods"""

    @pytest.fixture(autouse=True)
    def instance(self):
        _instance = mixins.CreateNewGameMixin()
        return _instance

    @pytest.mark.parametrize(
            "test_input, output", 
            [("string", "string (1)"), ("string (2)", "string (3)"), ("(1) string test (2)", "(1) string test (3)")]
    )
    def test__create_new_game(self, test_input: str, output: str, instance: mixins.CreateNewGameMixin):
        """Testing the _create_new_game method"""

        name = instance._create_new_name(test_input)
        assert name == output


class TestTakeShotMixin:
    """Testing the TakeShotMixin class methods"""

    @pytest.fixture(autouse=True)
    def instance(self):
        _instance = mixins.TakeShotMixin()
        return _instance

    @pytest.mark.parametrize("test_input, output", [("F1", "hit"), ("A5", "miss"), ("F2", "miss")])
    def test_get_type_shot(self, copy_board: dict, test_input: str, output: str, instance: mixins.TakeShotMixin):
        """Testing the _get_type_shot method"""

        type_shot = instance._get_type_shot(copy_board, test_input)
        assert type_shot == output
    
    @pytest.mark.parametrize(
        "test_input, output", 
        [
            (("F1", "hit"), ("F1", 27.1, "hit")), 
            (("A5", "miss"), ("A5", "", "miss")), 
            (("F2", "miss"), ("F2", " space 27.1 space 33.1", "miss"))
        ]
    )
    def test_shot(self, test_input: tuple, output: tuple, copy_board: dict, instance: mixins.TakeShotMixin):
        """Testing the _shot method"""

        assert copy_board[output[0][0]][output[0]] == output[1]

        field_value = instance._shot(copy_board, *test_input)
        assert field_value == output[1]
        assert copy_board[output[0][0]][output[0]] == output[2]

    @pytest.mark.parametrize("test_input, output", [(45.1, (False,)), (45.1, ("hit", True)), (45.4, (True,))])
    def test_is_ship_has_sunk(self, test_input: float, output: bool, copy_board: dict, instance: mixins.TakeShotMixin):
        """Testing the _is_ship_has_sunk method"""

        if len(output) == 2: copy_board["H"]["H10"] = output[0]

        is_ship_has_sunk = instance._is_ship_has_sunk(test_input, copy_board)
        assert is_ship_has_sunk == output[-1]
    
    def test_add_misses_around_sunken_ship(self, copy_board: dict, instance: mixins.TakeShotMixin):
        """Testing the _add_misses_around_sunken_ship method"""

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


class TestRandomPlacementMixin:
    """Testing the RandomPlacementMixin class methods"""

    @pytest.fixture(autouse=True)
    def instance(self):
        ins = mixins.RandomPlacementMixin()
        ins.column_name_list = column_name_list
        ins.string_number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ins.ship_count_tuple = ship_count_dict
        return ins

    @pytest.mark.parametrize(
        "test_input, output", 
        [(["A1", "A2", "A3"], False), (["A5", "A6", "A7"], True), (["J10"], True), (["B5"], False)]
    )
    def test_is_put_on_board(
        self, test_input: list, output: bool, copy_board: dict, instance: mixins.RandomPlacementMixin
    ):
        """Testing the _is_put_on_board method"""

        is_put = instance._is_put_on_board(test_input, copy_board)
        assert is_put == output

    def test_put_ship_on_board(self, copy_board: dict, instance: mixins.RandomPlacementMixin):
        """Testing the _put_ship_on_board method"""

        assert (copy_board["A"]["A5"], copy_board["A"]["A6"], copy_board["A"]["A7"]) == ("", "", "")

        instance._put_ship_on_board(3, 1, ["A5", "A6", "A7"], copy_board)

        assert (copy_board["A"]["A5"], copy_board["A"]["A6"], copy_board["A"]["A7"]) == (3.1, 3.1, 3.1)
    
    @pytest.mark.parametrize(
        "test_input, output", 
        [
            ((3, "A", 3, column_name_list), ["A3", "B3", "C3"]), 
            ((3, "J", 3, column_name_list), ["J3", "I3", "H3"]),
            ((3, "I", 3, column_name_list), ["I3", "H3", "G3"])
        ]
    )
    def test_get_field_list_horizontally(self, test_input: tuple, output: list, instance: mixins.RandomPlacementMixin):
        """Testing the get_field_list_horizontally method"""

        field_list = instance.get_field_list_horizontally(*test_input)
        assert field_list == output
    
    @pytest.mark.parametrize(
        "test_input, output", 
        [
            ((1, "A", 3), ["A1", "A2", "A3"]), 
            ((10, "A", 3), ["A10", "A9", "A8"]), 
            ((9, "E", 3), ["E9", "E8", "E7"])
        ]
    )
    def test_get_field_list_vertically(self, test_input: tuple, output: list, instance: mixins.RandomPlacementMixin):
        """Testing the get_field_list_vertically method"""

        field_list = instance.get_field_list_vertically(*test_input)
        assert field_list == output
    
    @pytest.mark.asyncio
    async def test_get_field_list(self, copy_board: dict, copy_ships: list, instance: mixins.RandomPlacementMixin):
        """Testing the get_field_list method"""

        old_board = deepcopy(copy_board)

        new_board = await instance.get_field_list("horizontal", 4, copy_board, copy_ships)
        assert type(new_board) == dict
        assert new_board == copy_board
        assert new_board != old_board
    
    @pytest.mark.asyncio
    async def test_random_placement(self, copy_board: dict, copy_ships: list, instance: mixins.RandomPlacementMixin):
        """Testing the random_placement method"""

        old_board = deepcopy(copy_board)

        new_board = await instance.get_field_list("horizontal", 4, copy_board, copy_ships)
        assert type(new_board) == dict
        assert new_board == copy_board
        assert new_board != old_board

        is_full = sum(1 for column_name in column_name_list if new_board[column_name][f"{column_name}1"])
        assert is_full > 0
