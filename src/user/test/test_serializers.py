from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from src.user import serializers


class TestUpdateUserPhotoSerializer(APITestCase):
    """Testing UpdateUserPhotoSerializer methods"""

    class Photo:
        """Photo test plug"""

        def __init__(self, name) -> None:
            self.name = name

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.instance = serializers.UpdateUserPhotoSerializer()
    
    def test_validate_photo(self):
        """Testing validate_photo method"""
        
        photo = self.Photo(name="string.jpg")
        response = self.instance.validate_photo(photo)
        assert response.name == "string.jpg", response.name

        photo = self.Photo(name="photo.png")
        response = self.instance.validate_photo(photo)
        assert response.name == "photo.png", response.name

        photo = self.Photo(name="string.py")
        with self.assertRaises(ValidationError):
            response = self.instance.validate_photo(photo)


class TestUpdateUserInfoSerializer(APITestCase):
    """Testing UpdateUserInfoSerializer methods"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.instance = serializers.UpdateUserInfoSerializer()
    
    def test_validate_first_name(self):
        """Testing validate_first_name method"""
        
        response = self.instance.validate_first_name("  string ")
        assert response == "string", response

        with self.assertRaises(ValidationError):
            response = self.instance.validate_first_name("1stri ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_first_name("str1 ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_first_name("str`")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_first_name("  stringstrings stringstringstringstring  ")
    
    def test_validate_last_name(self):
        """Testing validate_last_name method"""
        
        response = self.instance.validate_last_name("  string ")
        assert response == "string", response

        with self.assertRaises(ValidationError):
            response = self.instance.validate_last_name("1stri ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_last_name("str1 ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_last_name("str`")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_last_name("  stringstrings stringstringstringstring  ")
    
    def test_validate_email(self):
        """Testing validate_last_name method"""
        
        response = self.instance.validate_email("  string@gmail.com ")
        assert response == "string@gmail.com", response

        response = self.instance.validate_email("str123ing@gmail.com")
        assert response == "str123ing@gmail.com", response

        response = self.instance.validate_email("email_123@gmail.com")
        assert response == "email_123@gmail.com", response

        with self.assertRaises(ValidationError):
            response = self.instance.validate_email(" stqqqr`@gmail.com ")

        with self.assertRaises(ValidationError):
            response = self.instance.validate_email("1stri@gmail.com ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_email("  stringstrings stringstringstringstring@gmail.com  ")
    
    def test_validate_mobile_number(self):
        """Testing validate_mobile_number method"""
        
        response = self.instance.validate_mobile_number("  1234567891011 ")
        assert response == "1234567891011", response

        response = self.instance.validate_mobile_number("  12345678910112312313 ")
        assert response == "12345678910112312313", response

        with self.assertRaises(ValidationError):
            response = self.instance.validate_mobile_number("+312313131313133 ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_mobile_number("1234567890123456789011")


class TestSignUpSerializer(APITestCase):
    """Testing SignUpSerializer methods"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.instance = serializers.SignUpSerializer()
    
    def test_validate_username(self):
        """Testing validate_username method"""
        
        response = self.instance.validate_username("  string ")
        assert response == "string", response

        response = self.instance.validate_username("str123ing")
        assert response == "str123ing", response

        response = self.instance.validate_username(" stqqqr ")
        assert response == "stqqqr", response

        with self.assertRaises(ValidationError):
            response = self.instance.validate_username("stri")

        with self.assertRaises(ValidationError):
            response = self.instance.validate_username("1stri")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_username("1stri@gmail.com ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_username("  stringstrings stringstringstringstring@gmail.com  ")
    
    def test_validate_first_name(self):
        """Testing validate_first_name method"""
        
        response = self.instance.validate_first_name("  string ")
        assert response == "string", response

        with self.assertRaises(ValidationError):
            response = self.instance.validate_first_name("1stri ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_first_name("str1 ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_first_name("str`")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_first_name("  stringstrings stringstringstringstring  ")
    
    def test_validate_last_name(self):
        """Testing validate_last_name method"""
        
        response = self.instance.validate_last_name("  string ")
        assert response == "string", response

        with self.assertRaises(ValidationError):
            response = self.instance.validate_last_name("1stri ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_last_name("str1 ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_last_name("str`")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_last_name("  stringstrings stringstringstringstring  ")
    
    def test_validate_email(self):
        """Testing validate_last_name method"""
        
        response = self.instance.validate_email("  string@gmail.com ")
        assert response == "string@gmail.com", response

        response = self.instance.validate_email("str123ing@gmail.com")
        assert response == "str123ing@gmail.com", response

        response = self.instance.validate_email("email_123@gmail.com")
        assert response == "email_123@gmail.com", response

        with self.assertRaises(ValidationError):
            response = self.instance.validate_email(" stqqqr`@gmail.com ")

        with self.assertRaises(ValidationError):
            response = self.instance.validate_email("1stri@gmail.com ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_email(" 1ema@gmail.com ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_email("  stringstrings stringstringstringstring@gmail.com  ")
    
    def test_validate_mobile_number(self):
        """Testing validate_mobile_number method"""
        
        response = self.instance.validate_mobile_number("  1234567891011 ")
        assert response == "1234567891011", response

        response = self.instance.validate_mobile_number("  12345678910112312313 ")
        assert response == "12345678910112312313", response

        with self.assertRaises(ValidationError):
            response = self.instance.validate_mobile_number("+312313131313133 ")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_mobile_number("1234567890123456789011")
    
    def test_validate_password1(self):
        """Testing validate_password1 method"""

        response = self.instance.validate_password1("  qwe123qwesd123_qwe1 ")
        assert response == "qwe123qwesd123_qwe1", response

        response = self.instance.validate_password1("  qwe12 11_123 ")
        assert response == "qwe12 11_123", response

        with self.assertRaises(ValidationError):
            response = self.instance.validate_password1(" qwe1+we")
        
        with self.assertRaises(ValidationError):
            response = self.instance.validate_password1("  stringstrings stringstringstringstring@gmail.comqqq  ")
