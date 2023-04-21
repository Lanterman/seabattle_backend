from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from src.user.models import User
from src.game import models, services, serializers


class TestDetailLobbyView(APITestCase):
    """Testing DetailLobbyView view"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.row = "{'A1': '', 'A2': 'qwe', 'A3': '', 'A4': '', 'A5': '12', 'A6': '', 'A7': 'qwe', 'A8': '', 'A9': '', 'A10': ''}"

        cls.user = User.objects.create_user(username='user', password='password', email="user@mail.ru")
        cls.token = Token.objects.create(user=cls.user)
        cls.second_user = User.objects.create_user(username='user1', password='password', email="user1@mail.ru")
        cls.first_lobby = models.Lobby.objects.create(name="test", bet=10, time_to_move=30, time_to_placement=30)
        cls.first_board = models.Board.objects.create(lobby_id_id=cls.first_lobby.id, user_id_id=cls.user.id, 
                                                       A=cls.row)
        cls.second_board = models.Board.objects.create(lobby_id_id=cls.first_lobby.id, user_id_id=cls.second_user.id,
                                                        A=cls.row)
        cls.first_lobby.users.add(cls.user, cls.second_user)

        cls.second_lobby = models.Lobby.objects.create(name="test", bet=10, time_to_move=30, time_to_placement=30)
        cls.thirty_board = models.Board.objects.create(lobby_id_id=cls.second_lobby.id, A=cls.row)
        cls.forty_board = models.Board.objects.create(lobby_id_id=cls.second_lobby.id, A=cls.row, user_id=cls.user)
        cls.second_lobby.users.add(cls.user)

        cls.client = APIClient()
    
    def test_first_lobby(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        serializer_1 = serializers.BoardSerializer(self.first_board).data
        serializer_2 = serializers.BoardSerializer(self.second_board).data
        _, enemy_board = services.clear_enemy_board(self.user, (serializer_1, serializer_2))
        assert self.row != enemy_board["A"], enemy_board["A"]
        assert enemy_board["user_id"] != self.first_board.user_id, enemy_board["user_id"]
        assert enemy_board["user_id"] == self.second_board.user_id.id, enemy_board["user_id"]
    
    def test_second_lobby(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        serializer_1 = serializers.BoardSerializer(self.thirty_board).data
        serializer_2 = serializers.BoardSerializer(self.forty_board).data
        _, enemy_board = services.clear_enemy_board(self.user, (serializer_1, serializer_2))
        assert self.row != enemy_board["A"], enemy_board["A"]
        assert enemy_board["user_id"] == self.thirty_board.user_id, enemy_board["user_id"]
        assert enemy_board["user_id"] != self.forty_board.user_id.id, enemy_board["user_id"]