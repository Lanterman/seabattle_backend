from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from src.game.models import Lobby
from src.user import models, services
from config import settings


class TestIsLobbyFree(APITestCase):
    """Testing IsLobbyFree class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.lobby_1 = Lobby.objects.get(id=1)
        cls.lobby_2 = Lobby.objects.get(id=2)

        cls.user_1 = models.User.objects.get(id=1)
        cls.user_3 = models.User.objects.get(id=3)
        cls.token_1 = services.create_jwttoken(cls.user_1.id)
        cls.token_3 = services.create_jwttoken(cls.user_3.id)

        cls.request = APIRequestFactory()
        cls.client = APIClient()
        cls.url_1 = reverse('lobby-detail', kwargs={"slug": (cls.lobby_1.slug)})
        cls.url_2 = reverse('lobby-detail', kwargs={"slug": (cls.lobby_2.slug)})
        
        cls.type_token = settings.JWT_SETTINGS["AUTH_HEADER_TYPES"]

    def test_has_object_permission(self):
        """Testing has_object_permission method"""

        # first lobby
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_1.access_token}')
        response_get = self.client.get(path=self.url_1)
        assert response_get.status_code == 200, response_get.status_code

        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_3.access_token}')
        response_get = self.client.get(path=self.url_1)
        assert response_get.status_code == 403, response_get.status_code

        # second lobby
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_1.access_token}')
        response_get = self.client.get(path=self.url_2)
        assert response_get.status_code == 200, response_get.status_code

        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_3.access_token}')
        response_get = self.client.get(path=self.url_2)
        assert response_get.status_code == 200, response_get.status_code


class TestIsPlayWithBot(APITestCase):
    """Testing the IsPlayWithBot class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.lobby_1 = Lobby.objects.filter(id=1).first()
        cls.lobby_2 = Lobby.objects.filter(id=2).first()

        cls.user_1 = models.User.objects.get(id=1)
        cls.user_2 = models.User.objects.get(id=2)
        cls.token_1 = services.create_jwttoken(cls.user_1.id)
        cls.token_3 = services.create_jwttoken(cls.user_2.id)

        cls.request = APIRequestFactory()
        cls.client = APIClient()
        cls.url_1 = reverse('lobby-detail', kwargs={"slug": (cls.lobby_1.slug)})
        cls.url_2 = reverse('lobby-detail', kwargs={"slug": (cls.lobby_2.slug)})
        
        cls.type_token = settings.JWT_SETTINGS["AUTH_HEADER_TYPES"]
    
    def test_has_object_permission(self):
        """Testing has_object_permission method"""

        models.User.objects.filter(id=2).update(cash=100)
        Lobby.objects.filter(id=2).update(is_play_with_a_bot=True)

        # first lobby
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_1.access_token}')
        response_get = self.client.get(path=self.url_1)
        assert response_get.status_code == 200, response_get.status_code

        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_3.access_token}')
        response_get = self.client.get(path=self.url_1)
        assert response_get.status_code == 200, response_get.status_code

        # second lobby
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_1.access_token}')
        response_get = self.client.get(path=self.url_2)
        assert response_get.status_code == 200, response_get.status_code

        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_3.access_token}')
        response_get = self.client.get(path=self.url_2)
        assert response_get.status_code == 403, response_get.status_code


class TestIsEnoughMoney(APITestCase):
    """Testing IsEnoughMoney class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.lobby_1 = Lobby.objects.get(id=1)
        cls.lobby_2 = Lobby.objects.get(id=2)

        cls.user_1 = models.User.objects.get(id=1)
        cls.user_2 = models.User.objects.get(id=2)
        cls.token_1 = services.create_jwttoken(cls.user_1.id)
        cls.token_3 = services.create_jwttoken(cls.user_2.id)

        cls.request = APIRequestFactory()
        cls.client = APIClient()
        cls.url_1 = reverse('lobby-detail', kwargs={"slug": (cls.lobby_1.slug)})
        cls.url_2 = reverse('lobby-detail', kwargs={"slug": (cls.lobby_2.slug)})
        
        cls.type_token = settings.JWT_SETTINGS["AUTH_HEADER_TYPES"]

    def test_has_object_permission(self):
        """Testing has_object_permission method"""

        # first lobby
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_1.access_token}')
        response_get = self.client.get(path=self.url_1)
        assert response_get.status_code == 200, response_get.status_code

        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_3.access_token}')
        response_get = self.client.get(path=self.url_1)
        assert response_get.status_code == 403, response_get.status_code

        # second lobby
        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_1.access_token}')
        response_get = self.client.get(path=self.url_2)
        assert response_get.status_code == 200, response_get.status_code

        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_3.access_token}')
        response_get = self.client.get(path=self.url_2)
        assert response_get.status_code == 200, response_get.json()
