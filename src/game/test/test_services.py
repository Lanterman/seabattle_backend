from rest_framework.test import APITestCase

from src.user.models import User
from src.game import models, services, serializers


class TestDetailLobbyView(APITestCase):
    """Testing DetailLobbyView view"""

    def setUp(self) -> None:
        self.row = "{'A1': '', 'A2': 'qwe', 'A3': '', 'A4': '', 'A5': '12', 'A6': '', 'A7': 'qwe', 'A8': '', 'A9': '', 'A10': ''}"

        self.user = User.objects.create_user(username='user', password='password', email="user@mail.ru")
        self.second_user = User.objects.create_user(username='user1', password='password', email="user1@mail.ru")
        self.first_lobby = models.Lobby.objects.create(name="test", bet=10, time_to_move=30, time_to_placement=30)
        self.first_board = models.Board.objects.create(lobby_id_id=self.first_lobby.id, user_id_id=self.user.id, 
                                                       A=self.row)
        self.second_board = models.Board.objects.create(lobby_id_id=self.first_lobby.id, user_id_id=self.second_user.id,
                                                        A=self.row)
        self.first_lobby.users.add(self.user, self.second_user)

        self.second_lobby = models.Lobby.objects.create(name="test", bet=10, time_to_move=30, time_to_placement=30)
        self.thirty_board = models.Board.objects.create(lobby_id_id=self.second_lobby.id, user_id_id=self.user.id,
                                                        A=self.row)
        self.forty_board = models.Board.objects.create(lobby_id_id=self.second_lobby.id, A=self.row)
        self.second_lobby.users.add(self.user)
    
    def test_first_lobby(self): ##
        serializer_1 = serializers.BoardSerializer(self.first_board)
        serializer_2 = serializers.BoardSerializer(self.second_board)
        index, enemy_board = services.clear_enemy_board(self.user, (serializer_1, serializer_2))
        assert self.first_board.A != enemy_board["A"], enemy_board["A"]
        # assert self.second_board.A != self.row, self.second_board.A
    
    def test_second_lobby(self):
        assert self.thirty_board.A == self.row, self.thirty_board.A
        assert self.forty_board.A != self.row, (type(self.forty_board.A), type(self.row))