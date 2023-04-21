import pytest

from copy import deepcopy

from .data import board, ships, column_name_list
from ..services import clear_board
from ..addspace import add_space


@pytest.fixture
def copy_board():
    return deepcopy(board)


@pytest.fixture
def copy_ships():
     return deepcopy(ships)


def test_clear_board(copy_board):
    """Testing _clear_board method"""

    field_name_list = []

    assert copy_board["A"]["A1"] == 27.4, copy_board["A"]["A1"]

    for column in copy_board.values():
        for key in column:
            if column[key]:
                if column[key] != "space":
                    field_name_list.append(key)
                column[key] = ""

    assert len(field_name_list) == 96, len(field_name_list)
    assert copy_board != board, copy_board
    assert board["A"]["A1"] == 27.4, board["A"]["A1"]
    assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]


def test_drop_ship_on_board(copy_board):
    """Testing drop_ship_on_board method"""

    assert copy_board == board

    clear_board(copy_board)

    for field_name in ["F1", "G1", "H1", "I1"]:
        board[field_name[0]][field_name] = float(f"{ships[0]['id']}.{ships[0]['count']}")

    assert copy_board != board
    assert board["G"]["G1"] == 27.1


def test_insert_space_around_ship(copy_board):
    """Testing insert_space_around_ship method"""

    def insert_space_around_ship(space_name: str, ship_plane: str, field_name_list: list, board: dict) -> None:
        if ship_plane == "horizontal": 
            add_space.AddSpaceAroundShipHorizontally(space_name, field_name_list, column_name_list, board)
        else:
            add_space.AddSpaceAroundShipVertically(space_name, field_name_list, column_name_list, board)

    assert copy_board == board

    clear_board(copy_board)

    insert_space_around_ship(f"space 27.4", "horizontal", ["F1", "G1", "H1", "I1"], copy_board)

    assert copy_board != board
    assert copy_board["G"]["G2"] == "space 27.4"
    assert copy_board["E"]["E2"] == "space 27.4"
    assert copy_board["H"]["H2"] == "space 27.4"
    assert copy_board["F"]["F5"] == ""

    clear_board(copy_board)

    insert_space_around_ship(f"space 27.4", "vertical", ["F1", "F2", "F3", "F4"], copy_board)

    assert copy_board != board
    assert copy_board["G"]["G2"] == "space 27.4"
    assert copy_board["F"]["F5"] == "space 27.4"
    assert copy_board["H"]["H2"] == ""

# IsReadyToPlayMixin


