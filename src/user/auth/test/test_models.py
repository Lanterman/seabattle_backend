from rest_framework.test import APITestCase

from src.user.models import User
from src.user.auth import models as auth_models


class TestJWTToken(APITestCase):
    """Testing JWTToken class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = User.objects.get(id=3)
        cls.token = auth_models.JWTToken.objects.get(id=1)
    

    def test_str(self):
        """Testing __str__ method"""

        assert self.token.__str__() == f"JWT token to {self.user.username}", self.token.__str__()
