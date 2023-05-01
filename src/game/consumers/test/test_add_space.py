import pytest

from copy import deepcopy

from .test_data import board, column_name_list
from ..addspace import add_space
from src.game.consumers import services


@pytest.fixture
def copy_board():
    return deepcopy(board)


class TestBase:
    """Testing the Base class methods"""

    @pytest.fixture(autouse=True)
    def instance(self):
        return add_space.Base()

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

    @pytest.fixture(autouse=True)
    def instance(self):
        return add_space.AddSpaceAroundShipHorizontally(" space 3.2", ["A5", "B5", "C5"], column_name_list, deepcopy(board))

    def test_add_space_at_top(self, copy_board: dict, instance: add_space.AddSpaceAroundShipHorizontally):
        """Testing the add_space_at_top method"""

        assert copy_board == board, copy_board

        services.clear_board(copy_board)
        assert copy_board != board, copy_board

        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["D"]["D5"] == "", copy_board["D"]["D5"]
        
        instance.add_space_at_top(" space 1.1", ["A5", "B5", "C5"], copy_board)
        assert copy_board["A"]["A4"] == " space 1.1", copy_board["A"]["A4"]
        assert copy_board["A"]["A5"] == "", copy_board["A"]["A5"]
        assert copy_board["B"]["B4"] == " space 1.1", copy_board["B"]["B4"]
        assert copy_board["D"]["D4"] == "", copy_board["D"]["D4"]

        instance.add_space_at_top(" space 2.1", ["A1", "B1", "C1"], copy_board)
        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["B"]["B2"] == "", copy_board["B"]["B2"]
        assert copy_board["B"]["B4"] == " space 1.1", copy_board["B"]["B4"]
        assert copy_board["C"]["C1"] == "", copy_board["C"]["C1"]

        instance.add_space_at_top(" space 3.1", ["A2", "B2", "C2", "D2"], copy_board)
        assert copy_board["A"]["A1"] == " space 3.1", copy_board["A"]["A1"]
        assert copy_board["A"]["A2"] == "", copy_board["A"]["A2"]
        assert copy_board["A"]["A3"] == "", copy_board["A"]["A3"]
        assert copy_board["A"]["A4"] == " space 1.1", copy_board["A"]["A4"]
        assert copy_board["E"]["E2"] == "", copy_board["E"]["E2"]
    
    def test_add_space_to_right(self, copy_board: dict, instance: add_space.AddSpaceAroundShipHorizontally):
        """Testing the add_space_to_right method"""

        assert copy_board == board, copy_board

        services.clear_board(copy_board)
        assert copy_board != board, copy_board

        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["D"]["D5"] == "", copy_board["D"]["D5"]
        
        instance.add_space_to_right(" space 1.1", ["A5", "B5", "C5"], column_name_list, copy_board)
        assert copy_board["A"]["A4"] == "", copy_board["A"]["A4"]
        assert copy_board["C"]["C4"] == "", copy_board["C"]["C4"]
        assert copy_board["D"]["D4"] == " space 1.1", copy_board["D"]["D4"]
        assert copy_board["D"]["D5"] == " space 1.1", copy_board["D"]["D5"]
        assert copy_board["D"]["D6"] == " space 1.1", copy_board["D"]["D6"]
        assert copy_board["D"]["D7"] == "", copy_board["D"]["D7"]

        instance.add_space_to_right(" space 2.1", ["A1", "B1", "C1"], column_name_list, copy_board)
        assert copy_board["A"]["A2"] == "", copy_board["A"]["A2"]
        assert copy_board["C"]["C2"] == "", copy_board["C"]["C2"]
        assert copy_board["D"]["D1"] == " space 2.1", copy_board["D"]["D1"]
        assert copy_board["D"]["D2"] == " space 2.1", copy_board["D"]["D2"]
        assert copy_board["D"]["D3"] == "", copy_board["D"]["D3"]

        instance.add_space_to_right(" space 3.1", ["H3", "I3", "J3"], column_name_list, copy_board)
        assert copy_board["H"]["H2"] == "", copy_board["H"]["H2"]
        assert copy_board["J"]["J2"] == "", copy_board["J"]["J2"]
        assert copy_board["J"]["J3"] == "", copy_board["J"]["J3"]
        assert copy_board["J"]["J4"] == "", copy_board["J"]["J4"]
    
    def test_add_space_at_bottom(self, copy_board: dict, instance: add_space.AddSpaceAroundShipHorizontally):
        """Testing the add_space_at_bottom method"""

        assert copy_board == board, copy_board

        services.clear_board(copy_board)
        assert copy_board != board, copy_board

        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["D"]["D5"] == "", copy_board["D"]["D5"]

        instance.add_space_at_bottom(" space 1.1", ["A5", "B5", "C5"], copy_board)
        assert copy_board["A"]["A4"] == "", copy_board["A"]["A4"]
        assert copy_board["A"]["A5"] == "", copy_board["A"]["A5"]
        assert copy_board["B"]["B6"] == " space 1.1", copy_board["B"]["B6"]
        assert copy_board["C"]["C6"] == " space 1.1", copy_board["C"]["C6"]
        assert copy_board["D"]["D4"] == "", copy_board["D"]["D4"]

        instance.add_space_at_bottom(" space 2.1", ["A10", "B10", "C10"], copy_board)
        assert copy_board["A"]["A1"] == "", copy_board["A"]["A10"]
        assert copy_board["B"]["B9"] == "", copy_board["B"]["B9"]
        assert copy_board["B"]["B6"] == " space 1.1", copy_board["B"]["B6"]
        assert copy_board["C"]["C10"] == "", copy_board["C"]["C10"]

        instance.add_space_at_bottom(" space 3.1", ["A9", "B9", "C9", "D9"], copy_board)
        assert copy_board["A"]["A6"] == " space 1.1", copy_board["A"]["A6"]
        assert copy_board["A"]["A9"] == "", copy_board["A"]["A9"]
        assert copy_board["A"]["A10"] == " space 3.1", copy_board["A"]["A10"]
        assert copy_board["D"]["D9"] == "", copy_board["D"]["D9"]
        assert copy_board["D"]["D10"] == " space 3.1", copy_board["D"]["D10"]
        assert copy_board["E"]["E9"] == "", copy_board["E"]["E9"]
    
    def test_add_space_to_left(self, copy_board: dict, instance: add_space.AddSpaceAroundShipHorizontally):
        """Testing the add_space_to_left method"""

        assert copy_board == board, copy_board

        services.clear_board(copy_board)
        assert copy_board != board, copy_board

        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["D"]["D5"] == "", copy_board["D"]["D5"]
        
        instance.add_space_to_left(" space 1.1", "A5", column_name_list, copy_board)
        assert copy_board["A"]["A3"] == "", copy_board["A"]["A3"]
        assert copy_board["A"]["A4"] == "", copy_board["A"]["A4"]
        assert copy_board["A"]["A5"] == "", copy_board["A"]["A5"]
        assert copy_board["C"]["C4"] == "", copy_board["C"]["C4"]
        assert copy_board["D"]["D4"] == "", copy_board["D"]["D4"]

        instance.add_space_to_left(" space 2.1", "B2", column_name_list, copy_board)
        assert copy_board["A"]["A1"] == " space 2.1", copy_board["A"]["A1"]
        assert copy_board["A"]["A2"] == " space 2.1", copy_board["A"]["A2"]
        assert copy_board["A"]["A3"] == " space 2.1", copy_board["A"]["A3"]
        assert copy_board["A"]["A4"] == "", copy_board["A"]["A4"]
        assert copy_board["D"]["D1"] == "", copy_board["D"]["D1"]
        assert copy_board["D"]["D2"] == "", copy_board["D"]["D2"]

        instance.add_space_to_left(" space 3.1", "H3", column_name_list, copy_board)
        assert copy_board["G"]["G1"] == "", copy_board["G"]["G1"]
        assert copy_board["G"]["G2"] == " space 3.1", copy_board["G"]["G2"]
        assert copy_board["G"]["G3"] == " space 3.1", copy_board["G"]["G3"]
        assert copy_board["G"]["G4"] == " space 3.1", copy_board["G"]["G4"]
        assert copy_board["G"]["G5"] == "", copy_board["G"]["G5"]
        assert copy_board["I"]["I2"] == "", copy_board["I"]["I2"]
        assert copy_board["I"]["I3"] == "", copy_board["I"]["I3"]
        assert copy_board["I"]["I4"] == "", copy_board["I"]["I4"]

    def test_insert_space_around_ship(self, copy_board: dict, instance: add_space.AddSpaceAroundShipHorizontally):
        """Testing the insert_space_around_ship method"""

        assert copy_board == board, copy_board

        services.clear_board(copy_board)
        assert copy_board != board, copy_board

        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["D"]["D5"] == "", copy_board["D"]["D5"]
        
        instance.insert_space_around_ship(" space 1.1", ["A5", "B5", "C5"], column_name_list, copy_board)
        assert copy_board["A"]["A4"] == " space 1.1", copy_board["A"]["A4"]
        assert copy_board["A"]["A5"] == "", copy_board["A"]["A5"]
        assert copy_board["A"]["A6"] == " space 1.1", copy_board["A"]["A6"]
        assert copy_board["B"]["B4"] == " space 1.1", copy_board["B"]["B4"]
        assert copy_board["B"]["B6"] == " space 1.1", copy_board["B"]["B6"]
        assert copy_board["C"]["C4"] == " space 1.1", copy_board["C"]["C4"]
        assert copy_board["C"]["C6"] == " space 1.1", copy_board["C"]["C6"]
        assert copy_board["D"]["D5"] == " space 1.1", copy_board["D"]["D5"]
        assert copy_board["D"]["D6"] == " space 1.1", copy_board["D"]["D6"]
        assert copy_board["D"]["D7"] == "", copy_board["D"]["D7"]

        instance.insert_space_around_ship(" space 2.1", ["A1", "B1", "C1"], column_name_list, copy_board)
        assert copy_board["A"]["A2"] == " space 2.1", copy_board["A"]["A2"]
        assert copy_board["C"]["C2"] == " space 2.1", copy_board["C"]["C2"]
        assert copy_board["D"]["D1"] == " space 2.1", copy_board["D"]["D1"]
        assert copy_board["D"]["D2"] == " space 2.1", copy_board["D"]["D2"]
        assert copy_board["D"]["D3"] == "", copy_board["D"]["D3"]

        instance.insert_space_around_ship(" space 3.1", ["H3", "I3", "J3"], column_name_list, copy_board)
        assert copy_board["G"]["G2"] == " space 3.1", copy_board["G"]["G2"]
        assert copy_board["G"]["G4"] == " space 3.1", copy_board["G"]["G4"]
        assert copy_board["H"]["H2"] == " space 3.1", copy_board["H"]["H2"]
        assert copy_board["H"]["H4"] == " space 3.1", copy_board["H"]["H4"]
        assert copy_board["J"]["J2"] == " space 3.1", copy_board["J"]["J2"]
        assert copy_board["J"]["J3"] == "", copy_board["J"]["J3"]
        assert copy_board["J"]["J4"] == " space 3.1", copy_board["J"]["J4"]


class TestAddSpaceAroundShipVertically:
    """Testing the AddSpaceAroundShipVertically class methods"""

    @pytest.fixture(autouse=True)
    def instance(self): 
        return add_space.AddSpaceAroundShipVertically(" space 4.3", ["A5", "A6", "A7"], column_name_list, deepcopy(board))

    def test_add_space_at_top(self, copy_board: dict, instance: add_space.AddSpaceAroundShipVertically):
        """Testing the add_space_at_top method"""

        assert copy_board == board, copy_board

        services.clear_board(copy_board)
        assert copy_board != board, copy_board

        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["D"]["D5"] == "", copy_board["D"]["D5"]
        
        instance.add_space_at_top(" space 1.1", "A5", copy_board)
        assert copy_board["A"]["A4"] == " space 1.1", copy_board["A"]["A4"]
        assert copy_board["A"]["A5"] == "", copy_board["A"]["A5"]
        assert copy_board["A"]["A8"] == "", copy_board["A"]["A8"]
        assert copy_board["B"]["B4"] == "", copy_board["B"]["B4"]

        instance.add_space_at_top(" space 2.1", "A1", copy_board)
        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A4"] == " space 1.1", copy_board["A"]["A4"]
        assert copy_board["B"]["B2"] == "", copy_board["B"]["B2"]

        instance.add_space_at_top(" space 3.1", "A2", copy_board)
        assert copy_board["A"]["A1"] == " space 3.1", copy_board["A"]["A1"]
        assert copy_board["A"]["A2"] == "", copy_board["A"]["A2"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["B"]["B2"] == "", copy_board["B"]["B2"]
    
    def test_add_space_to_right(self, copy_board: dict, instance: add_space.AddSpaceAroundShipVertically):
        """Testing the add_space_to_right method"""

        assert copy_board == board, copy_board

        services.clear_board(copy_board)
        assert copy_board != board, copy_board

        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["D"]["D5"] == "", copy_board["D"]["D5"]
        
        instance.add_space_to_right(" space 1.1", ["A5", "A6", "A7"], column_name_list, copy_board)
        assert copy_board["A"]["A4"] == "", copy_board["A"]["A4"]
        assert copy_board["A"]["A8"] == "", copy_board["A"]["A8"]
        assert copy_board["B"]["B4"] == " space 1.1", copy_board["B"]["B4"]
        assert copy_board["B"]["B5"] == " space 1.1", copy_board["B"]["B5"]
        assert copy_board["B"]["B8"] == " space 1.1", copy_board["B"]["B8"]

        instance.add_space_to_right(" space 2.1", ["A1", "A2", "A3"], column_name_list, copy_board)
        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A4"] == "", copy_board["A"]["A4"]
        assert copy_board["B"]["B1"] == " space 2.1", copy_board["B"]["B1"]
        assert copy_board["B"]["B2"] == " space 2.1", copy_board["B"]["B2"]
        assert copy_board["B"]["B3"] == " space 2.1", copy_board["B"]["B3"]

        instance.add_space_to_right(" space 3.1", ["A2", "A3", "A4"], column_name_list, copy_board)
        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A5"] == "", copy_board["A"]["A5"]
        assert copy_board["B"]["B1"] == " space 2.1 space 3.1", copy_board["B"]["B1"]
        assert copy_board["B"]["B2"] == " space 2.1 space 3.1", copy_board["B"]["B2"]
        assert copy_board["B"]["B5"] == " space 1.1 space 3.1", copy_board["B"]["B5"]
        assert copy_board["B"]["B6"] == " space 1.1", copy_board["B"]["B6"]
    
    def test_add_space_at_bottom(self, copy_board: dict, instance: add_space.AddSpaceAroundShipVertically):
        """Testing the add_space_at_bottom method"""

        assert copy_board == board, copy_board

        services.clear_board(copy_board)
        assert copy_board != board, copy_board

        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["D"]["D5"] == "", copy_board["D"]["D5"]
        
        instance.add_space_at_bottom(" space 1.1", "A7", copy_board)
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["A"]["A8"] == " space 1.1", copy_board["A"]["A8"]
        assert copy_board["B"]["B8"] == "", copy_board["B"]["B8"]


        instance.add_space_at_bottom(" space 2.1", "A3", copy_board)
        assert copy_board["A"]["A2"] == "", copy_board["A"]["A2"]
        assert copy_board["A"]["A4"] == " space 2.1", copy_board["A"]["A4"]
        assert copy_board["B"]["B4"] == "", copy_board["B"]["B4"]

        instance.add_space_at_bottom(" space 3.1", "A10", copy_board)
        assert copy_board["A"]["A9"] == "", copy_board["A"]["A9"]
        assert copy_board["A"]["A10"] == "", copy_board["A"]["A10"]
        assert copy_board["B"]["B10"] == "", copy_board["B"]["B10"]
    
    def test_add_space_to_left(self, copy_board: dict, instance: add_space.AddSpaceAroundShipVertically):
        """Testing the add_space_to_left method"""

        assert copy_board == board, copy_board

        services.clear_board(copy_board)
        assert copy_board != board, copy_board

        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["D"]["D5"] == "", copy_board["D"]["D5"]
        
        instance.add_space_to_left(" space 1.1", ["B5", "B6", "B7"], column_name_list, copy_board)
        assert copy_board["A"]["A3"] == "", copy_board["A"]["A3"]
        assert copy_board["A"]["A4"] == " space 1.1", copy_board["A"]["A4"]
        assert copy_board["A"]["A5"] == " space 1.1", copy_board["A"]["A5"]
        assert copy_board["A"]["A8"] == " space 1.1", copy_board["A"]["A8"]
        assert copy_board["B"]["B4"] == "", copy_board["B"]["B4"]
        assert copy_board["B"]["B8"] == "", copy_board["B"]["B8"]

        instance.add_space_to_left(" space 2.1", ["A1", "A2", "A3"], column_name_list, copy_board)
        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A4"] == " space 1.1", copy_board["A"]["A4"]
        assert copy_board["B"]["B1"] == "", copy_board["B"]["B1"]
        assert copy_board["B"]["B3"] == "", copy_board["B"]["B4"]

        instance.add_space_to_left(" space 3.1", ["B1", "B2", "B3"], column_name_list, copy_board)
        assert copy_board["A"]["A1"] == " space 3.1", copy_board["A"]["A1"]
        assert copy_board["A"]["A2"] == " space 3.1", copy_board["A"]["A2"]
        assert copy_board["A"]["A4"] == " space 1.1 space 3.1", copy_board["A"]["A4"]
        assert copy_board["B"]["B1"] == "", copy_board["B"]["B1"]
        assert copy_board["B"]["B4"] == "", copy_board["B"]["B4"]

    def test_insert_space_around_ship(self, copy_board: dict, instance: add_space.AddSpaceAroundShipVertically):
        """Testing the insert_space_around_ship method"""

        assert copy_board == board, copy_board

        services.clear_board(copy_board)
        assert copy_board != board, copy_board

        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A6"] == "", copy_board["A"]["A6"]
        assert copy_board["D"]["D5"] == "", copy_board["D"]["D5"]
        
        instance.insert_space_around_ship(" space 1.1", ["C5", "C6", "C7"], column_name_list, copy_board)
        assert copy_board["B"]["B4"] == " space 1.1", copy_board["B"]["B4"]
        assert copy_board["B"]["B6"] == " space 1.1", copy_board["B"]["B6"]
        assert copy_board["B"]["B8"] == " space 1.1", copy_board["B"]["B8"]
        assert copy_board["C"]["C4"] == " space 1.1", copy_board["C"]["C4"]
        assert copy_board["C"]["C6"] == "", copy_board["C"]["C6"]
        assert copy_board["C"]["C8"] == " space 1.1", copy_board["C"]["C8"]


        instance.insert_space_around_ship(" space 2.1", ["A1", "A2", "A3"], column_name_list, copy_board)
        assert copy_board["A"]["A1"] == "", copy_board["A"]["A1"]
        assert copy_board["A"]["A4"] == " space 2.1", copy_board["A"]["A4"]
        assert copy_board["B"]["B1"] == " space 2.1", copy_board["B"]["B1"]
        assert copy_board["B"]["B4"] == " space 1.1 space 2.1", copy_board["B"]["B4"]

        instance.insert_space_around_ship(" space 3.1", ["J8", "J9", "J10"], column_name_list, copy_board)
        assert copy_board["J"]["J7"] == " space 3.1", copy_board["J"]["J7"]
        assert copy_board["J"]["J10"] == "", copy_board["J"]["J10"]
        assert copy_board["I"]["I7"] == " space 3.1", copy_board["I"]["I7"]
        assert copy_board["I"]["I9"] == " space 3.1", copy_board["I"]["I9"]
        assert copy_board["I"]["I10"] == " space 3.1", copy_board["I"]["I10"]
