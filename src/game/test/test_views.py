import logging

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from src.user.models import User
from src.game import models, serializers
from config.utilities import redis_instance


class TestDetailLobbyView(APITestCase):
    """Testing DetailLobbyView view"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        logging.warning(f"Number of keys in Redis database before running tests: {len(redis_instance.keys())}")

        cls.user = User.objects.get(username="admin")
        cls.third_user = User.objects.get(username='user')
        cls.user_token = Token.objects.create(user=cls.user)
        cls.third_user_token = Token.objects.create(user=cls.third_user)
        cls.lobby = models.Lobby.objects.get(id=1)

        cls.client = APIClient()
        cls.url = reverse('lobby-detail', kwargs={"slug": cls.lobby.slug})

    @classmethod
    def tearDownClass(cls) -> None:
        logging.warning(f"Number of keys in Redis database before closing: {len(redis_instance.keys())}")
        redis_instance.flushall()
        super().tearDownClass()

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
