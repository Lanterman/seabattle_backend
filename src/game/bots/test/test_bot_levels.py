from copy import deepcopy
from channels.db import database_sync_to_async
from rest_framework.test import APITestCase, APITransactionTestCase

from src.user.models import User
from src.game import models as game_models
from src.game.bots import bot_levels
from src.game.consumers import db_queries as ws_db_queries, services as ws_services
from src.game.consumers.test.test_data import board, ships, column_name_list


class TestSyncGenericBot(APITestCase):
    """Sync testing GenericBot class"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.ship_dict_on_board = {27.4: 3, 27.3: 2, 33.3: 3, 45.2: 1, 39.1: 2, 
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
        assert len(field_dict_1) == 23, len(field_dict_1)

        field_dict_2 = self.instance.bot_get_field_dict(board, column_name_list, 2)
        assert len(field_dict_2) == 47, len(field_dict_2)

        copy_board = deepcopy(board)
        copy_board["H"]["H1"] = "hit"
        copy_board["E"]["E4"] = "miss"

        field_dict_1 = self.instance.bot_get_field_dict(copy_board, column_name_list, 4)
        assert len(field_dict_1) == 21, field_dict_1
    
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

        # horizontal hit < 9
        field_dict = self.instance.bot_gets_fields_around_hit("B3", copy_board, column_name_list)
        test_data = {'A3': 27.3}
        assert field_dict == test_data, field_dict

        copy_board["H"]["H1"] = "hit"
        field_dict = self.instance.bot_gets_fields_around_hit("I1", copy_board, column_name_list)
        test_data = {'J1': ' space 27.1', 'G1': 27.1}
        assert field_dict == test_data, field_dict

        # horizontal hit > 0
        field_dict = self.instance.bot_gets_fields_around_hit("C1", copy_board, column_name_list)
        test_data = {'A1': 27.4, 'D1': 27.4}
        assert field_dict == test_data, field_dict

        # horizontal hit > 0 - miss
        copy_board["G"]["G1"] = "hit"
        field_dict = self.instance.bot_gets_fields_around_hit("F1", copy_board, column_name_list)
        test_data = {'I1': 27.1}
        assert field_dict == test_data, field_dict

        # no plane
        field_dict = self.instance.bot_gets_fields_around_hit("F7", copy_board, column_name_list)
        test_data = {'F6': 27.2, 'F8': 27.2, 'E7': ' space 27.2 space 39.1', 'G7': ' space 27.2 space 39.2'}
        assert field_dict == test_data, field_dict

        # vertical hit 
        copy_board["F"]["F8"] = "hit"
        field_dict = self.instance.bot_gets_fields_around_hit("F9", copy_board, column_name_list)
        test_data = {'F7': 27.2}
        assert field_dict == test_data, field_dict

        # vertical hit 
        copy_board["H"]["H6"] = "hit"
        field_dict = self.instance.bot_gets_fields_around_hit("H7", copy_board, column_name_list)
        test_data = {"H8": " space 39.2"}
        assert field_dict == test_data, field_dict


class TestAsyncGenericBot(APITransactionTestCase):
    """Async testing GenericBot class"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @staticmethod
    async def perform_write_shot(board_id: int, column_dictionary: dict) -> None:
        await ws_db_queries.write_shot(board_id, column_dictionary)

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.get(pk=1)
        self.lobby = game_models.Lobby.objects.prefetch_related("boards").get(id=2)
        self.board_1 = game_models.Board.objects.get(id=3)
        self.board_2 = game_models.Board.objects.get(id=4)

        self.instance = bot_levels.GenericBot()
        self.instance.perform_write_shot = self.perform_write_shot
    
    async def test_bot_passes_move_to_user(self):
        """Testing bot_passes_move_to_user method"""

        assert self.board_1.is_my_turn == False, self.board_1.is_my_turn
        assert self.board_2.is_my_turn == False, self.board_2.is_my_turn

        await self.instance.bot_passes_move_to_user(self.lobby.slug, self.user)
        await database_sync_to_async(self.board_1.refresh_from_db)()
        await database_sync_to_async(self.board_2.refresh_from_db)()
        
        assert self.board_1.is_my_turn == True, self.board_1.is_my_turn
        assert self.board_2.is_my_turn == False, self.board_2.is_my_turn
    
    async def test_bot_missed(self):
        """Testing bot_missed method"""

        board = await ws_db_queries.get_board(self.board_1.id, column_name_list)
        ws_services.confert_to_json(board)

        assert self.board_1.is_my_turn == False, self.board_1.is_my_turn
        assert self.board_2.is_my_turn == False, self.board_2.is_my_turn

        await self.instance.bot_missed(self.user, self.board_1.id, str(self.lobby.slug), "A1", {}, board)
        await database_sync_to_async(self.board_1.refresh_from_db)()
        await database_sync_to_async(self.board_2.refresh_from_db)()
        
        assert self.board_1.is_my_turn == True, self.board_1.is_my_turn
        assert self.board_2.is_my_turn == False, self.board_2.is_my_turn


class TestHighBot(APITestCase):
    """Testing HighBot class methods"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.ship_dict_on_board = {27.4: 3, 27.3: 2, 33.3: 3, 45.2: 1, 39.1: 2, 
                                  27.1: 4, 27.2: 4, 33.1: 3, 39.2: 2, 45.1: 1, 33.2: 3}
        cls.ship_size_and_name_list = [(4, 27), (3, 33), (2, 39), (1, 45)]

        cls.instance = bot_levels.HighBot()

    def test_high_bot_gets_fields_around_hit(self):
        """Testing high_bot_gets_fields_around_hit method"""

        copy_board = deepcopy(board)

        # horizontal
        field_dict = self.instance.high_bot_gets_fields_around_hit("F7", copy_board, column_name_list)
        test_data = {"F6": 27.2, "F8": 27.2, "F9": 27.2}
        assert field_dict == test_data, field_dict

        copy_board["F"]["F6"] = "hit"
        copy_board["F"]["F9"] = "hit"
        field_dict = self.instance.high_bot_gets_fields_around_hit("F7", copy_board, column_name_list)
        test_data = {"F8": 27.2}
        assert field_dict == test_data, field_dict

        copy_board["F"]["F8"] = "hit"
        field_dict = self.instance.high_bot_gets_fields_around_hit("F7", copy_board, column_name_list)
        test_data = {}
        assert field_dict == test_data, field_dict

        # vertical
        field_dict = self.instance.high_bot_gets_fields_around_hit("H1", copy_board, column_name_list)
        test_data = {'F1': 27.1, 'G1': 27.1, 'I1': 27.1}
        assert field_dict == test_data, field_dict
