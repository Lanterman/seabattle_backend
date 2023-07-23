import pytest

from rest_framework.test import APITestCase

from src.user import services, models
from src.user.auth import models as auth_models


@pytest.mark.parametrize("test_input, output", [(None, 12), (None, 12), (5, 5), (15, 15)])
def test_create_salt(test_input: int or None, output: int):
    """Testing the create_salt function"""

    if test_input is not None:
        response = services.create_salt(test_input)
    else:
        response = services.create_salt()
    assert output == len(response), response


@pytest.mark.parametrize(
    "password, salt", 
    [("password", "KtQrvyHOiHqweqwe"), ("password", "zebNbHEPCv123132"), ("karmavdele2", None), ("karmavdele", None)]
)
def test_password_hashing(password: str, salt: str):
    """Testing the password_hashing function"""

    if salt is not None:
        response = services.password_hashing(password, salt)
    else: 
        response = services.password_hashing(password)
    assert len(response) == 64, response
    assert type(response) == str, type(response)


@pytest.mark.parametrize(
    "test_input, output", 
    [
        (("password", "KtQrvyHOiHFU$b18f34385035abe98c305d63d2121ff72a8bca7385a7d217d1891a1c43d397ae"), False), 
        (("password", "zebNbHEPCvpn$e9cb2c4a1d0757f3fb38eeb67148370cfa70f5433101843c9eaa23d04b735b0f"), False), 
        (("karmavdele2", "iEmhsIVjCkVh$19b074e240f28205f2bb2304d1e72f3257334dd9e4879392f527d40a8e4db9cb"), True), 
        (("karmavdele", "KtQrvyHOiHFU$b18f34385035abe98c305d63d2121ff72a8bca7385a7d217d1891a1c43d397ae"), True), 
    ]
)
def test_validate_password(test_input: str, output: bool):
    """Testing the validate_password function"""

    response = services.validate_password(*test_input)
    assert response == output, response


@pytest.mark.parametrize("password", ["password", "Password", "test_password"])
def test_create_hashed_password(password: str):
    """Testing the create_hashed_password function"""

    response = services.create_hashed_password(password)
    assert "$" in response, response

    salt, hashed_password = response.split("$")
    assert 12 == len(salt), salt
    assert 64 == len(hashed_password)


class TestCreateUserSecretKeyFunction(APITestCase):
    """Testing the create_user_secret_key function"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user_1 = models.User.objects.get(id=1)
        cls.user_2 = models.User.objects.get(id=2)
        cls.user_3 = models.User.objects.get(id=3)

    def test_create_user_secret_key(self):
        count_secret_key_to_db = auth_models.SecretKey.objects.count()
        assert 3 == count_secret_key_to_db, count_secret_key_to_db

        # first user
        response = services.create_user_secret_key(self.user_1.id)
        updated_count_secret_key_to_db = auth_models.SecretKey.objects.count()
        assert 4 == updated_count_secret_key_to_db, updated_count_secret_key_to_db
        assert 64 == len(response), len(response)
        assert str == type(response), type(response)

        # second user
        response = services.create_user_secret_key(self.user_2.id)
        updated_count_secret_key_to_db = auth_models.SecretKey.objects.count()
        assert 4 == updated_count_secret_key_to_db, updated_count_secret_key_to_db
        assert 64 == len(response), len(response)
        assert str == type(response), type(response)

        # third user
        response = services.create_user_secret_key(self.user_3.id)
        updated_count_secret_key_to_db = auth_models.SecretKey.objects.count()
        assert 4 == updated_count_secret_key_to_db, updated_count_secret_key_to_db
        assert 64 == len(response), len(response)
        assert str == type(response), type(response)


class TestCreateJWTTokenFunction(APITestCase):
    """Testing the create_jwttoken function"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user_1 = models.User.objects.get(id=1)
        cls.user_2 = models.User.objects.get(id=2)
        cls.user_3 = models.User.objects.get(id=3)

    def test_create_jwttoken(self):
        count_secret_key_to_db = auth_models.SecretKey.objects.count()
        count_auth_token_to_db = auth_models.JWTToken.objects.count()
        assert 3 == count_secret_key_to_db, count_secret_key_to_db
        assert 2 == count_auth_token_to_db, count_auth_token_to_db

        # first user
        response = services.create_jwttoken(self.user_1.id)
        new_count_secret_key_to_db = auth_models.SecretKey.objects.count()
        new_count_auth_token_to_db = auth_models.JWTToken.objects.count()
        assert 4 == new_count_secret_key_to_db, new_count_secret_key_to_db
        assert 3 == new_count_auth_token_to_db, new_count_auth_token_to_db
        assert "JWTToken" == response.__class__.__name__, response.__class__.__name__
        assert 1 == response.user_id, response.user_id

        # second user
        response = services.create_jwttoken(self.user_2.id)
        new_count_secret_key_to_db = auth_models.SecretKey.objects.count()
        new_count_auth_token_to_db = auth_models.JWTToken.objects.count()
        assert 4 == new_count_secret_key_to_db, new_count_secret_key_to_db
        assert 4 == new_count_auth_token_to_db, new_count_auth_token_to_db
        assert "JWTToken" == response.__class__.__name__, response.__class__.__name__
        assert 2 == response.user_id, response.user_id

        # third user
        response = services.create_jwttoken(self.user_3.id, self.user_3.email)
        new_count_secret_key_to_db = auth_models.SecretKey.objects.count()
        new_count_auth_token_to_db = auth_models.JWTToken.objects.count()
        assert 4 == new_count_secret_key_to_db, new_count_secret_key_to_db
        assert 4 == new_count_auth_token_to_db, new_count_auth_token_to_db
        assert "JWTToken" == response.__class__.__name__, response.__class__.__name__
        assert 3 == response.user_id, response.user_id
