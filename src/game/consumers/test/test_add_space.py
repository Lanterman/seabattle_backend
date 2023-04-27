import pytest

from copy import deepcopy

from .test_data import board
from ..addspace import add_space


@pytest.fixture
def copy_board():
    return deepcopy(board)


class TestBase:
    """Testing the Base class methods"""

    @pytest.fixture(autouse=True)
    def instance(self):
        _instance = add_space.Base()
        return _instance

    def test_add_space_to_first_field(self, copy_board: dict, instance: add_space.Base):
        """Testing the add_space_to_first_field method"""

        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["A"]["A7"] == "", copy_board["A"]["A7"]
        assert copy_board["A"]["A8"] == " space 33.3", copy_board["A"]["A8"]
        assert copy_board["J"]["J1"] == " space 27.1", copy_board["J"]["J1"]
        assert copy_board["J"]["J2"] == " space 27.1 space 33.1", copy_board["J"]["J2"]
        assert copy_board["B"]["B2"] == " space 27.3 space 27.4", copy_board["B"]["B2"]
        assert copy_board["B"]["B3"] == 27.3, copy_board["B"]["B3"]
        assert copy_board["B"]["B4"] == " space 27.3 space 45.2", copy_board["B"]["B4"]

        instance.add_space_to_first_field(" space 1.1", "A7", copy_board)
        assert copy_board["A"]["A6"] == " space 1.1", copy_board["A"]["A6"]
        assert copy_board["A"]["A7"] == "", copy_board["A"]["A7"]
        assert copy_board["A"]["A8"] == " space 33.3", copy_board["A"]["A8"]

        instance.add_space_to_first_field(" space 2.1", "J1", copy_board)
        assert copy_board["J"]["J1"] == " space 27.1", copy_board["J"]["J1"]
        assert copy_board["J"]["J2"] == " space 27.1 space 33.1", copy_board["J"]["J2"]

        instance.add_space_to_first_field(" space 3.2", "B3", copy_board)
        assert copy_board["B"]["B2"] == " space 27.3 space 27.4 space 3.2", copy_board["B"]["B2"]
        assert copy_board["B"]["B3"] == 27.3, copy_board["B"]["B3"]
        assert copy_board["B"]["B4"] == " space 27.3 space 45.2", copy_board["B"]["B4"]
    
    def test_add_space_to_last_field(self, copy_board: dict, instance: add_space.Base):
        """Testing the add_space_to_last_field method"""

        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["A"]["A7"] == "", copy_board["A"]["A7"]
        assert copy_board["A"]["A8"] == " space 33.3", copy_board["A"]["A8"]
        assert copy_board["B"]["B2"] == " space 27.3 space 27.4", copy_board["B"]["B2"]
        assert copy_board["B"]["B3"] == 27.3, copy_board["B"]["B3"]
        assert copy_board["B"]["B4"] == " space 27.3 space 45.2", copy_board["B"]["B4"]
        assert copy_board["J"]["J9"] == " space 33.2", copy_board["J"]["J9"]
        assert copy_board["J"]["J10"] == "", copy_board["J"]["J10"]
        
        instance.add_space_to_last_field(" space 1.1", "A7", copy_board)
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["A"]["A7"] == "", copy_board["A"]["A7"]
        assert copy_board["A"]["A8"] == " space 33.3 space 1.1", copy_board["A"]["A8"]

        instance.add_space_to_last_field(" space 2.1", "J10", copy_board)
        assert copy_board["J"]["J9"] == " space 33.2", copy_board["J"]["J9"]
        assert copy_board["J"]["J10"] == "", copy_board["J"]["J10"]

        instance.add_space_to_last_field(" space 3.2", "B3", copy_board)
        assert copy_board["B"]["B2"] == " space 27.3 space 27.4", copy_board["B"]["B2"]
        assert copy_board["B"]["B3"] == 27.3, copy_board["B"]["B3"]
        assert copy_board["B"]["B4"] == " space 27.3 space 45.2 space 3.2", copy_board["B"]["B4"]


class TestAddSpaceAroundShipHorizontally:
    """Testing the AddSpaceAroundShipHorizontally class methods"""

    def test_add_space_at_top(self):
        """Testing the add_space_at_top method"""
    
    def test_add_space_to_right(self):
        """Testing the add_space_to_right method"""
    
    def test_add_space_at_bottom(self):
        """Testing the add_space_at_bottom method"""
    
    def test_add_space_to_left(self):
        """Testing the add_space_to_left method"""

    def test_insert_space_around_ship(self):
        """Testing the insert_space_around_ship method"""


class TestAddSpaceAroundShipVertically:
    """Testing the AddSpaceAroundShipVertically class methods"""

    def test_add_space_at_top(self):
        """Testing the add_space_at_top method"""
    
    def test_add_space_to_right(self):
        """Testing the add_space_to_right method"""
    
    def test_add_space_at_bottom(self):
        """Testing the add_space_at_bottom method"""
    
    def test_add_space_to_left(self):
        """Testing the add_space_to_left method"""

    def test_insert_space_around_ship(self):
        """Testing the insert_space_around_ship method"""
