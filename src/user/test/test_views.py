from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from src.user import models, services


class TestSignInView(APITestCase):
    """Testing the SignInView endpoint methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = models.User.objects.get(id=1)

        cls.client = APIClient()

        cls.path = reverse("sign-in")
    
    def test_get_method(self):
        with self.assertLogs(level="WARNING"):
            response = self.client.get(self.path)
        
        assert response.status_code == 405, response.status_code
    
    def test_post_method(self):
        valid_resposne = self.client.post(path=self.path, data={"username": "admin", "password": "karmavdele"})
        assert valid_resposne.status_code == 201, valid_resposne.status_code

        with self.assertLogs(level="WARNING"):
            invalid_resposne = self.client.post(path=self.path, data={"username": "admin1", "password": "karmavdele"})
        
        assert invalid_resposne.status_code == 400, invalid_resposne.status_code

        with self.assertLogs(level="WARNING"):
            invalid_resposne = self.client.post(path=self.path, data={"username": "admin", "password": "admin1"})
        
        assert invalid_resposne.status_code == 400, invalid_resposne.status_code

        self.user.is_active = False
        self.user.save()
        self.user.refresh_from_db()

        with self.assertLogs(level="WARNING"):
            invalid_resposne = self.client.post(path=self.path, data={"username": "admin", "password": "admin"})
        
        assert invalid_resposne.status_code == 400, invalid_resposne.status_code


class TestSignUpView(APITestCase):
    """Testing the SignUpView endpoint methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = models.User.objects.get(id=1)

        cls.client = APIClient()

        cls.path = reverse("sign-up")
    
    def test_get_method(self):
        with self.assertLogs(level="WARNING"):
            response = self.client.get(self.path)
        
        assert response.status_code == 405, response.status_code
    
    def test_post_method(self):
        valid_data = {
            "username": "username", 
            "first_name": "firstname", 
            "last_name": "lastname", 
            "email": "email_123@mail.com", 
            "mobile_number": 123456789123, 
            "password1": "password123", 
            "password2": "password123"
        }

        invalid_data = {
            "username": "user", 
            "first_name": "1name", 
            "last_name": "last!", 
            "email": "email_123!@mail.com", 
            "mobile_number": 12345678912, 
            "password1": "password", 
            "password2": "pswrd"
        }
        
        valid_resposne = self.client.post(path=self.path, data=valid_data)
        assert valid_resposne.status_code == 201, valid_resposne.status_code

        with self.assertLogs(level="WARNING"):
            invalid_resposne = self.client.post(path=self.path, data=invalid_data)
        
        assert invalid_resposne.status_code == 400, invalid_resposne.status_code


class TestProfileView(APITestCase):
    """Testing the ProfileView endpoint methods"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user_1 = models.User.objects.get(id=1)
        cls.user_2 = models.User.objects.get(id=2)
        cls.token = services.create_jwttoken(cls.user_1.id)

        cls.client = APIClient()

        cls.path_1 = reverse("user-detail", kwargs={"username": "admin"})
        cls.path_2 = reverse("user-detail", kwargs={"username": "lanterman"})

        cls.valid_data = {
            "first_name": "firstname", 
            "last_name": "lastname", 
            "email": "email_123@mail.ru", 
            "mobile_number": 123456789123
        }

        cls.invalid_data = {
            "first_name": "name", 
            "last_name": "name", 
            "email": "email_123!@mail.ru", 
            "mobile_number": 12345678912
        }
    
    def test_get_method_unauthorization(self):
        with self.assertLogs(level="WARNING"):
            response = self.client.get(self.path_1)
        
        assert response.status_code == 401, response.status_code
    
    def test_get_method_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.access_token)

        response_1 = self.client.get(self.path_1)
        response_2 = self.client.get(self.path_2)
        
        assert response_1.status_code == 200, response_1.status_code
        assert response_2.status_code == 200, response_2.status_code
    
    def test_post_method_unauthorization(self):
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path_1, data=self.valid_data)
        
        assert response.status_code == 401, response.status_code
    
    def test_patch_method_info(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.access_token)

        response_1 = self.client.patch(self.path_1, data=self.valid_data)
        assert response_1.status_code == 200, response_1.status_code

        with self.assertLogs(level="WARNING"):
            response_2 = self.client.patch(self.path_1, data=self.invalid_data)
        assert response_2.status_code == 400, response_2.status_code

        with self.assertLogs(level="WARNING"):
            response_2 = self.client.patch(self.path_2, data=self.valid_data)
        assert response_2.status_code == 403, response_2.status_code

    def test_patch_method_delete_photo(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.access_token)

        response_1 = self.client.patch(self.path_1, data={})
        assert response_1.status_code == 200, response_1.status_code

        with self.assertLogs(level="WARNING"):
            response_2 = self.client.patch(self.path_2, data={})
        assert response_2.status_code == 403, response_2.status_code
    
    def test_patch_method_photo(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.access_token)

        assert self.user_1.photo == "", self.user_1.photo
        assert self.user_2.photo == "", self.user_2.photo

        # valid
        with open("src/user/test/test_data/test_valid_image.jpg", 'rb') as f:
            response = self.client.patch(self.path_1, format='multipart', data={'photo': f})
            assert response.status_code == 200, response
        
        updated_user_1 = models.User.objects.get(id=1)
        assert updated_user_1.photo != self.user_1.photo, updated_user_1.photo

        # invalid format
        with open("src/user/test/test_data/test_invalid_data.mp4", 'rb') as f:
            with self.assertLogs(level="WARNING"):
                response = self.client.patch(self.path_1, format='multipart', data={'photo': f})
            
            assert response.status_code == 400, response
        
        updated_user_2 = models.User.objects.get(id=1)
        assert updated_user_2.photo != self.user_1.photo, updated_user_2.photo
        assert updated_user_2.photo == updated_user_1.photo, updated_user_2.photo

        # Forbidden
        with open("src/user/test/test_data/test_valid_image.jpg", 'rb') as f:
            with self.assertLogs(level="WARNING"):
                response = self.client.patch(self.path_2, format='multipart', data={'photo': f})
            
            assert response.status_code == 403, response
        
        updated_user_3 = models.User.objects.get(id=2)
        assert updated_user_3.photo == self.user_2.photo, updated_user_3.photo
