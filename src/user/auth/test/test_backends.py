from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.exceptions import AuthenticationFailed
from oauth2_provider.models import AccessToken

from config import settings
from src.user import services as user_services, models as user_models
from src.user.auth import backends, models as auth_models


class TestJWTTokenAuthBackend(APITestCase):
    """Testing JWTTokenAuthBackend class methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = user_models.User.objects.get(id=1)
        cls.token = user_services.create_jwttoken(user_id=1)
        cls.token_to_db = auth_models.JWTToken.objects.get(user_id=3)
        cls.oauth_token = AccessToken.objects.get(user_id=2)

        cls.request = APIRequestFactory()
        cls.url = reverse('user-detail', kwargs={"username": cls.user.username})
        cls.instance = backends.JWTTokenAuthBackend()
        
        cls.type_token = settings.JWT_SETTINGS["AUTH_HEADER_TYPES"]
    

    def test_get_model(self):
        """Testing get_model method"""

        model = self.instance.get_model()
        assert "JWTToken" == model.__name__, model.__name__

        models = self.instance.get_model(is_oauth=True)
        assert tuple == type(models), type(models)
        assert 2 == len(models), models
        assert "AccessToken" == models[0].__name__, models[0].__name__
        assert "RefreshToken" == models[1].__name__, models[1].__name__
    
    def test_authenticate(self):
        """Testing authenticate method"""

        request_1 = self.request.get(self.url)
        resposne_1 = self.instance.authenticate(request_1)
        assert None == resposne_1, resposne_1

        request_2 = self.request.get(self.url, headers={"Authorization": f"{self.type_token}"})
        raise_msg = 'Invalid token header. No credentials provided.'
        with self.assertRaisesMessage(AuthenticationFailed, raise_msg):
            self.instance.authenticate(request_2)
        
        request_3 = self.request.get(
            self.url, 
            headers={"Authorization": f"{self.type_token} {self.type_token} {self.token.access_token}"}
        )
        raise_msg = 'Invalid token header. Token string should not contain spaces.'
        with self.assertRaisesMessage(AuthenticationFailed, raise_msg):
            self.instance.authenticate(request_3)
        
        request_4 = self.request.get(
            self.url, 
            headers={"Authorization": f"{self.type_token} {self.token.access_token}1"}
        )
        raise_msg = 'Invalid token.'
        with self.assertRaisesMessage(AuthenticationFailed, raise_msg):
            self.instance.authenticate(request_4)
        
        request_5 = self.request.get(
            self.url, 
            headers={"Authorization": f"{self.type_token} {self.oauth_token.token}.oauth"}
        )
        resposne_5 = self.instance.authenticate(request_5)
        assert tuple == type(resposne_5), resposne_5
        assert 2 == len(resposne_5), resposne_5
        assert "lanterman" == resposne_5[0].username, resposne_5[0]
        assert "AccessToken" == resposne_5[1].__class__.__name__, resposne_5[1].__class__.__name__
        assert self.oauth_token.token == resposne_5[1].token, resposne_5[1].token

        request_6 = self.request.get(
            self.url, 
            headers={"Authorization": f"{self.type_token} {self.token.access_token}"}
        )
        resposne_6 = self.instance.authenticate(request_6)
        assert tuple == type(resposne_6), resposne_6
        assert 2 == len(resposne_6), resposne_6
        assert "admin" == resposne_6[0].username, resposne_6[0]
        assert "JWTToken" == resposne_6[1].__class__.__name__, resposne_6[1].__class__.__name__
        assert self.token.access_token == resposne_6[1].access_token, resposne_6[1].access_token

    def test_social_oauthenticate_credentials(self):
        """Testing social_oauthenticate_credentials method"""

        raise_msg = 'Invalid token.'
        with self.assertRaisesMessage(AuthenticationFailed, raise_msg):
            self.instance.social_oauthenticate_credentials(f"{self.oauth_token}1")

        response_2 = self.instance.social_oauthenticate_credentials(f"{self.oauth_token}")
        assert tuple == type(response_2), response_2
        assert 2 == len(response_2), response_2
        assert "lanterman" == response_2[0].username, response_2[0]
        assert "AccessToken" == response_2[1].__class__.__name__, response_2[1].__class__.__name__
        assert self.oauth_token.token == response_2[1].token, response_2[1].token
    
    def test_authenticate_credentials(self):
        """Testing authenticate_credentials method"""

        raise_msg = 'Invalid token.'
        with self.assertRaisesMessage(AuthenticationFailed, raise_msg):
            self.instance.authenticate_credentials(f"{self.token}1")

        response_2 = self.instance.authenticate_credentials(self.token_to_db.access_token)
        assert tuple == type(response_2), response_2
        assert 2 == len(response_2), response_2
        assert "user" == response_2[0].username, response_2[0]
        assert "JWTToken" == response_2[1].__class__.__name__, response_2[1].__class__.__name__
        assert self.token_to_db.access_token == response_2[1].access_token, response_2[1].access_token

        raise_msg = 'User inactive or deleted.'
        user_models.User.objects.filter(id=3).update(is_active=False)
        with self.assertRaisesMessage(AuthenticationFailed, raise_msg):
            self.instance.authenticate_credentials(self.token_to_db.access_token)


        
