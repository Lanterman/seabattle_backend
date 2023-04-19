import logging

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from src.user.models import User
from src.game import models, serializers
from config.utilities import redis_instance


class TestDetailLobbyView(APITestCase):
    """Testing DetailLobbyView view"""

    @classmethod
    def setUpTestData(cls) -> None:
        logging.warning(f"Number of keys in Redis database before running tests: {len(redis_instance.keys())}")
        
        cls.user = User.objects.create_user(username='user', password='password', email="user@mail.ru")
        cls.second_user = User.objects.create_user(username='second_user', password='password', 
                                                    email="second_user@mail.ru")
        cls.third_user = User.objects.create_user(username='third_user', password='password')
        cls.user_token = Token.objects.create(user=cls.user)
        cls.third_user_token = Token.objects.create(user=cls.third_user)
        cls.lobby = models.Lobby.objects.create(name="test", bet=10, time_to_move=30, time_to_placement=30)
        cls.lobby.users.add(cls.user, cls.second_user)
        cls.first_board = models.Board.objects.create(lobby_id_id=cls.lobby.id, user_id_id=cls.user.id)
        cls.second_board = models.Board.objects.create(lobby_id_id=cls.lobby.id, user_id_id=cls.second_user.id)
        models.Ship.objects.create(name="singledeck", size=1, count=4, board_id_id=cls.first_board.id)
        models.Ship.objects.create(name="singledeck", size=1, count=4, board_id_id=cls.second_board.id)
        models.Message.objects.create(message="Hi, tester!", owner=cls.user.username, lobby_id_id=cls.lobby.id)
        models.Message.objects.create(message="I'm a bot!", owner=cls.user.username, is_bot=True, lobby_id_id=cls.lobby.id)

        cls.client = APIClient()
        cls.url = reverse('lobby-detail', kwargs={"slug": cls.lobby.slug})
    
    @classmethod
    def tearDownClass(cls) -> None:
        logging.warning(f"Number of keys in Redis database before closing: {len(redis_instance.keys())}")
        redis_instance.flushall()
    
    def test_url_of_unauthenticated_user(self):
        response = self.client.get(path=self.url)
        assert response.status_code == 401, response.status_code
    
    def test_url_of_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get(path=self.url)
        assert response.status_code == 200, response.status_code
    
    def test_output_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get(path=self.url)
        assert response.status_code == 200, response.status_code
        serializer_data = serializers.RetrieveLobbySerializer(self.lobby).data
        assert serializer_data["id"] == response.data["id"], (serializer_data["id"], response.data["id"])
        assert len(serializer_data["boards"]) == len(response.data["boards"]), len(serializer_data["boards"])

    def test_is_lobby_not_free(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.third_user_token.key)
        response = self.client.get(path=self.url)
        assert response.status_code == 403, response.status_code
    
    def test_is_lobby_free(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get(path=self.url)
        assert response.status_code == 200, response.status_code
    
    def test_if_not_exists_winner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get(path=self.url)
        assert response.status_code == 200, response.status_code
        assert response.data["time_left"] == 30, response.data["time_left"]
