from rest_framework.test import APITestCase

from src.user import db_queries, models, services
from src.user.auth import models as auth_models


class TestGetOrNoneFunction(APITestCase):
    """Testing get_or_none function"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def test_existing_user(self):
        response = db_queries.get_or_none("admin")
        self.assertIsNotNone(response, response)
        assert response.__str__() == "admin", response.__str__()
        assert response.is_superuser == True, response.is_superuser
    
    def test_non_existent_user(self):
        response = db_queries.get_or_none("string")
        self.assertIsNone(response, response)


class TestGetUserByUsernameFunction(APITestCase):
    """Testing get_user_by_username function"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    def test_existing_user(self):
        response = db_queries.get_user_by_username("admin")
        self.assertIsNotNone(response, response)
        assert response.__str__() == "admin", response.__str__()
        assert response.is_superuser == True, response.is_superuser
    
    def test_non_existent_user(self):
        response = db_queries.get_user_by_username("string")
        self.assertIsNone(response, response)


class TestCreateUserTokenFunction(APITestCase):
    """Testing create_user_token function"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user_1 = models.User.objects.get(id=1)
        cls.user_2 = models.User.objects.get(id=2)
        cls.token_1 = services.create_jwttoken(cls.user_1.id)

    def test_existing_token(self):
        token_1 = auth_models.JWTToken.objects.get(user=self.user_1.id)
        self.assertTrue(token_1, token_1)

        response = services.create_jwttoken(self.user_1.id)
        self.assertTrue(response, response)
        assert token_1 == response, response
    
    def test_non_existent_token(self):
        token_2 = auth_models.JWTToken.objects.filter(user=self.user_2.id).exists()
        self.assertFalse(token_2, token_2)

        response = services.create_jwttoken(self.user_2.id)
        token_2 = auth_models.JWTToken.objects.get(user=self.user_2.id)
        self.assertTrue(response, response)
        self.assertTrue(token_2, token_2)
        assert token_2 == response, response
