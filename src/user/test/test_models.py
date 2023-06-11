from rest_framework.test import APITestCase

from src.user import models


class TestUserModel(APITestCase):
    """Testing User model"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user_1 = models.User.objects.get(id=1)
        cls.user_2 = models.User.objects.get(id=2)
            
    def test__str__method(self):
        """Testing __str__ method"""

        resposne = self.user_1.__str__()
        assert resposne == "admin", resposne

        resposne = self.user_2.__str__()
        assert resposne == "lanterman", resposne
    
    def test_get_absolute_url_method(self):
        """Testing get_absolute_url method"""

        response = self.user_1.get_absolute_url()
        assert response == "/api/v1/auth/profile/admin/", response

        response = self.user_2.get_absolute_url()
        assert response == "/api/v1/auth/profile/lanterman/", response
