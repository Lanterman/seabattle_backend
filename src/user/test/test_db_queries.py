from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


from src.user import db_queries, models


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
        cls.token_1 = Token.objects.create(user=cls.user_1)

    def test_existing_token(self):
        token_1 = Token.objects.get(user=self.user_1)
        self.assertTrue(token_1, token_1)

        response = db_queries.create_user_token(self.user_1)
        self.assertTrue(response, response)
        assert token_1 == response, response
    
    def test_non_existent_token(self):
        token_2 = Token.objects.filter(user=self.user_2).exists()
        self.assertFalse(token_2, token_2)

        response = db_queries.create_user_token(self.user_2)
        token_2 = Token.objects.get(user=self.user_2)
        self.assertTrue(response, response)
        self.assertTrue(token_2, token_2)
        assert token_2 == response, response
