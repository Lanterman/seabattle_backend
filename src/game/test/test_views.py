import logging

from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework.reverse import reverse

from src.user import models as user_models, services as user_services
from src.game import models, serializers, views
from config.utilities import redis_instance
from config import settings


class TestLobbyListView(APITestCase):
    """Testing LobbyListView view"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = user_models.User.objects.get(id=2)
        cls.user_token = user_services.create_jwttoken(cls.user.id)
        cls.lobby = models.Lobby.objects.get(id=1)

        cls.instance = views.LobbyListView()
        cls.request = APIRequestFactory()
        cls.instance.request = cls.request
        cls.instance.user = cls.user
        
        cls.client = APIClient()
        cls.url = reverse('lobby-list')

        cls.type_token = settings.JWT_SETTINGS["AUTH_HEADER_TYPES"]
    
    def test_get_queryset(self):
        """Testing get_queryset method"""

        queryset = self.instance.get_queryset()
        assert len(queryset) == 1, queryset
        assert queryset[0].name == "string1", queryset
    
    def test_get_serializer_class(self):
        """Testing get_serializer_class method"""

        self.instance.request.method = "GET"
        queryset = self.instance.get_serializer_class()
        assert queryset.__doc__ == "List lobby serializer", queryset.__doc__

        self.instance.request.method = "POST"
        queryset = self.instance.get_serializer_class()
        assert queryset.__doc__ == "Create lobby serializer", queryset.__doc__


class TestDetailLobbyView(APITestCase):
    """Testing DetailLobbyView view"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        info = f"{cls.__name__}: Number of keys in Redis database before running tests: {len(redis_instance.keys())}"
        logging.info(info)

        cls.user = user_models.User.objects.get(username="admin")
        cls.third_user = user_models.User.objects.get(username='user')
        cls.user_token = user_services.create_jwttoken(cls.user.id)
        cls.third_user_token = user_services.create_jwttoken(cls.third_user.id)
        cls.lobby = models.Lobby.objects.get(id=1)

        cls.client = APIClient()
        cls.url = reverse('lobby-detail', kwargs={"slug": cls.lobby.slug})

        cls.type_token = settings.JWT_SETTINGS["AUTH_HEADER_TYPES"]

    @classmethod
    def tearDownClass(cls) -> None:
        info = f"{cls.__name__}: Number of keys in Redis database before closing: {len(redis_instance.keys())}"
        logging.info(info)
        redis_instance.delete(str(cls.lobby.slug))
        super().tearDownClass()

    def test_url_of_unauthenticated_user(self):
        with self.assertLogs(level="WARNING"):
            response = self.client.get(path=self.url)
        assert response.status_code == 401, response.status_code

    def test_url_of_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.user_token.access_token}')
        with self.assertNoLogs(level="WARNING"):
            response = self.client.get(path=self.url)
        assert response.status_code == 200, response.status_code

    def test_output_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.user_token.access_token}')
        response = self.client.get(path=self.url)
        assert response.status_code == 200, response.status_code
        serializer_data = serializers.RetrieveLobbySerializer(self.lobby).data
        assert serializer_data["id"] == response.data["id"], (serializer_data["id"], response.data["id"])
        assert len(serializer_data["boards"]) == len(response.data["boards"]), len(serializer_data["boards"])

    def test_is_lobby_not_free(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.third_user_token.access_token}')
        with self.assertLogs(level="WARNING"):
            response = self.client.get(path=self.url)
        assert response.status_code == 403, response.status_code

    def test_is_lobby_free(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.user_token.access_token}')
        with self.assertNoLogs(level="WARNING"):
            response = self.client.get(path=self.url)
        assert response.status_code == 200, response.status_code

    def test_if_not_exists_winner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.user_token.access_token}')
        response = self.client.get(path=self.url)
        assert response.status_code == 200, response.status_code
        assert response.data["time_left"] == 30, response.data["time_left"]
