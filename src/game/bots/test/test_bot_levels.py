from copy import deepcopy
from rest_framework.test import APITestCase

from src.game.bots import bot_levels
from src.game.consumers.test.test_data import board, ships, column_name_list


class TestGenericBot(APITestCase):
    """Testing GenericBot class"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.ship_dict_on_board = {27.4: 4, 27.3: 2, 33.3: 3, 45.2: 1, 39.1: 2, 
                                  27.1: 4, 27.2: 4, 33.1: 3, 39.2: 2, 45.1: 1, 33.2: 3}
        cls.ship_size_and_name_list = [(4, 27), (3, 33), (2, 39), (1, 45)]

        cls.instance = bot_levels.GenericBot()
    
    def test_bot_gets_ship_dict_on_the_board(self):
        """Testing bot_gets_ship_dict_on_the_board method"""
        
        ship_dict = self.instance.bot_gets_ship_dict_on_the_board(board)
        assert ship_dict == self.ship_dict_on_board, ship_dict

    def test_bot_gets_ship_size_and_name_list(self):
        """Testing bot_gets_ship_size_and_name_list method"""

        ship_size_and_name_list = self.instance.bot_gets_ship_size_and_name_list(ships)
        assert ship_size_and_name_list == self.ship_size_and_name_list, ship_size_and_name_list

    def test_bot_selects_target(self):
        """Testing bot_selects_target method"""

        max_index = self.instance.bot_selects_target(self.ship_dict_on_board, self.ship_size_and_name_list)
        assert max_index == 4, max_index

        max_index = self.instance.bot_selects_target(self.ship_dict_on_board, self.ship_size_and_name_list[1:])
        assert max_index == 3, max_index

        max_index = self.instance.bot_selects_target(self.ship_dict_on_board, self.ship_size_and_name_list[2:])
        assert max_index == 2, max_index

        max_index = self.instance.bot_selects_target(self.ship_dict_on_board, self.ship_size_and_name_list[:2])
        assert max_index == 4, max_index
    
    def test_bot_get_field_dict(self):
        """Testing bot_get_field_dict method"""

        field_dict_1 = self.instance.bot_get_field_dict(board, column_name_list, 4)
        assert len(field_dict_1) == 24, len(field_dict_1)

        field_dict_2 = self.instance.bot_get_field_dict(board, column_name_list, 2)
        assert len(field_dict_2) == 49, len(field_dict_2)

        copy_board = deepcopy(board)
        copy_board["H"]["H1"] = "hit"
        copy_board["E"]["E4"] = "miss"

        field_dict_1 = self.instance.bot_get_field_dict(copy_board, column_name_list, 4)
        assert len(field_dict_1) == 22, field_dict_1
    
    def test_bot_defines_plane(self):
        """Testing bot_defines_plane method"""

        copy_board = deepcopy(board)

        plane = self.instance.bot_defines_plane("B3", copy_board, column_name_list)
        assert plane == "horizontal", plane

        plane = self.instance.bot_defines_plane("F7", copy_board, column_name_list)
        assert plane == None, plane

        copy_board["F"]["F6"] = "hit"
        plane = self.instance.bot_defines_plane("F7", copy_board, column_name_list)
        assert plane == "vertical", plane
    
    def test_bot_gets_fields_around_hit(self):
        """Testing bot_gets_fields_around_hit method"""

        copy_board = deepcopy(board)

        field_dict = self.instance.bot_gets_fields_around_hit("B3", copy_board, column_name_list)
        test_data = {'A3': 27.3}
        assert field_dict == test_data, field_dict

        field_dict = self.instance.bot_gets_fields_around_hit("F7", copy_board, column_name_list)
        test_data = {'F6': 27.2, 'F8': 27.2, 'E7': ' space 27.2 space 39.1', 'G7': ' space 27.2 space 39.2'}
        assert field_dict == test_data, field_dict

        copy_board["F"]["F6"] = "hit"
        field_dict = self.instance.bot_gets_fields_around_hit("F7", copy_board, column_name_list)
        test_data = {'F8': 27.2, "F5": ' space 27.2'}
        assert field_dict == test_data, field_dict
    
    async def test_bot_passes_move_to_user(self):
        """Testing bot_passes_move_to_user method"""

        # Проверять записи в бд
    
    async def test_bot_there_are_no_ships(self):
        """Testing bot_there_are_no_ships method"""

        # Через обсерверы проверять отправку событий
    
    async def test_bot_missed(self):
        """Testing bot_missed method"""

        # Проверять записи в бд
    
    async def test_bot_take_shot(self):
        """Testing _bot_take_shot method"""

        # Проверять записи в бд
        # Через обсерверы проверять отправку событий
    