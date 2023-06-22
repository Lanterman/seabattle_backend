from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token

from src.user import models


class TestIsMyProfilePermission(APITestCase):
    """Testing IsMyProfile class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user_1 = models.User.objects.get(id=1)
        cls.user_2 = models.User.objects.get(id=2)
        cls.token_1 = Token.objects.create(user=cls.user_1)
        cls.token_2 = Token.objects.create(user=cls.user_2)

        cls.request = APIRequestFactory()
        cls.client = APIClient()
        cls.url = reverse('user-detail', kwargs={"username": cls.user_1.username})

    def test_has_object_permission(self):
        """Testing has_object_permission method"""

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_1.key)
        response_get = self.client.get(path=self.url)
        response_patch = self.client.patch(path=self.url, data={"first_name": "string"})
        assert response_get.status_code == 200, response_get.status_code
        assert response_patch.status_code == 200, response_patch.status_code

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_2.key)
        response_get = self.client.get(path=self.url)
        assert response_get.status_code == 200, response_get.status_code

        with self.assertLogs(level="WARNING"):
            response_patch = self.client.patch(path=self.url, data={"first_name": "string"})
        assert response_patch.status_code == 403, response_patch.status_code
