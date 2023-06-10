from rest_framework.test import APITestCase, APIClient

from src.user.models import User
from src.game import models, services, serializers


class TestDetailLobbyView(APITestCase):
    """Testing DetailLobbyView view"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.clean_row_A = {'A1': '', 'A2': '', 'A3': '', 'A4': '', 'A5': '', 'A6': '', 'A7': '', 
                           'A8': '', 'A9': '', 'A10': ''}

        cls.user_1 = User.objects.get(username="admin")
        cls.user_2 = User.objects.get(username="lanterman")

        cls.first_board = models.Board.objects.get(id=1)
        cls.second_board = models.Board.objects.get(id=2)
        cls.thirty_board = models.Board.objects.get(id=3)
        cls.forty_board = models.Board.objects.get(id=4)

        cls.client = APIClient()
    
    def test_first_lobby(self):
        serializer_1 = serializers.BoardSerializer(self.first_board).data
        serializer_2 = serializers.BoardSerializer(self.second_board).data

        index, enemy_board = services.clear_enemy_board(self.user_1, (serializer_1, serializer_2))
        assert self.clean_row_A == enemy_board["A"], enemy_board["A"]
        assert index == 1, index
        assert enemy_board["user_id"] != self.first_board.user_id, enemy_board["user_id"]
        assert enemy_board["user_id"] == self.second_board.user_id.id, enemy_board["user_id"]

        index, enemy_board = services.clear_enemy_board(self.user_1, (serializer_2, serializer_1))
        assert self.clean_row_A == enemy_board["A"], enemy_board["A"]
        assert index == 0, index
        assert enemy_board["user_id"] != self.first_board.user_id, enemy_board["user_id"]
        assert enemy_board["user_id"] == self.second_board.user_id.id, enemy_board["user_id"]

        index, enemy_board = services.clear_enemy_board(self.user_2, (serializer_1, serializer_2))
        assert self.clean_row_A == enemy_board["A"], enemy_board["A"]
        assert index == 0, index
        assert enemy_board["user_id"] != self.thirty_board.user_id, enemy_board["user_id"]
        assert enemy_board["user_id"] != self.forty_board.user_id, enemy_board["user_id"]

        index, enemy_board = services.clear_enemy_board(self.user_2, (serializer_2, serializer_1))
        assert self.clean_row_A == enemy_board["A"], enemy_board["A"]
        assert index == 1, index
        assert enemy_board["user_id"] != self.thirty_board.user_id, enemy_board["user_id"]
        assert enemy_board["user_id"] != self.forty_board.user_id, enemy_board["user_id"]
    
    def test_second_lobby(self):
        serializer_1 = serializers.BoardSerializer(self.thirty_board).data
        serializer_2 = serializers.BoardSerializer(self.forty_board).data

        index, enemy_board = services.clear_enemy_board(self.user_1, (serializer_1, serializer_2))
        assert self.clean_row_A == enemy_board["A"], enemy_board["A"]
        assert index == 1, index
        assert enemy_board["user_id"] != self.thirty_board.user_id, enemy_board["user_id"]
        assert enemy_board["user_id"] == self.forty_board.user_id, enemy_board["user_id"]

        index, enemy_board = services.clear_enemy_board(self.user_1, (serializer_2, serializer_1))
        assert self.clean_row_A == enemy_board["A"], enemy_board["A"]
        assert index == 0, index
        assert enemy_board["user_id"] != self.thirty_board.user_id, enemy_board["user_id"]
        assert enemy_board["user_id"] == self.forty_board.user_id, enemy_board["user_id"]

        index, enemy_board = services.clear_enemy_board(self.user_2, (serializer_1, serializer_2))
        assert self.clean_row_A != enemy_board["A"], enemy_board["A"]
        assert index == 0, index
        assert enemy_board["user_id"] != self.thirty_board.user_id, enemy_board["user_id"]
        assert enemy_board["user_id"] != self.forty_board.user_id, enemy_board["user_id"]

        index, enemy_board = services.clear_enemy_board(self.user_2, (serializer_2, serializer_1))
        assert self.clean_row_A != enemy_board["A"], enemy_board["A"]
        assert index == 1, index
        assert enemy_board["user_id"] != self.thirty_board.user_id, enemy_board["user_id"]
        assert enemy_board["user_id"] != self.forty_board.user_id, enemy_board["user_id"]
