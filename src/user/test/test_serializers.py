from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from src.user import serializers


class TestValidateClass(APITestCase):
    """Testing ValidateClass class methods"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.instance = serializers.ValidateClass()
    
    def test_validate_first_character(self):
        """Testing validate_first_character method"""

        error_list = []
        detail_error = "First character of 'first_name' field can only contain characters!"

        self.instance.validate_first_character("1firstname", "first_name", error_list)
        assert len(error_list) == 1, error_list
        assert detail_error == error_list[0], error_list[0]

        self.instance.validate_first_character("@firstname", "first_name", error_list)
        assert len(error_list) == 2, error_list
        assert detail_error == error_list[1], error_list[1]

        self.instance.validate_first_character("firstname1", "first_name", error_list)
        assert len(error_list) == 2, error_list

        self.instance.validate_first_character("_first_name", "first_name", error_list)
        assert len(error_list) == 2, error_list

    def test_validate_only_numbers(self):
        """Testing validate_only_numbers method"""

        error_list = []
        detail_error = "'mobile_number' field can only numbers characters!"

        self.instance.validate_only_numbers("q12323", "mobile_number", error_list)
        assert len(error_list) == 1, error_list
        assert detail_error == error_list[0], error_list[0]

        self.instance.validate_only_numbers("123123q1", "mobile_number", error_list)
        assert len(error_list) == 2, error_list
        assert detail_error == error_list[1], error_list[1]

        self.instance.validate_only_numbers("123213q", "mobile_number", error_list)
        assert len(error_list) == 3, error_list
        assert detail_error == error_list[2], error_list[2]

        self.instance.validate_only_numbers("12312312312", "mobile_number", error_list)
        assert len(error_list) == 3, error_list
    
    def test_validate_only_numbers_contains_and_underscore(self):
        """Testing validate_only_numbers_contains_and_underscore method"""

        error_list = []
        detail_error = "'email' field can only numbers, letters and underscore!"

        self.instance.validate_only_numbers_contains_and_underscore("qwe123@", "email", error_list)
        assert len(error_list) == 1, error_list
        assert detail_error == error_list[0], error_list[0]

        self.instance.validate_only_numbers_contains_and_underscore("=qwe123", "email", error_list)
        assert len(error_list) == 2, error_list
        assert detail_error == error_list[1], error_list[1]

        self.instance.validate_only_numbers_contains_and_underscore("_qwe23qwe1/", "email", error_list)
        assert len(error_list) == 3, error_list
        assert detail_error == error_list[2], error_list[2]

        self.instance.validate_only_numbers_contains_and_underscore("_lqwewqe123", "email", error_list)
        assert len(error_list) == 3, error_list
    
    def test_validate_only_contains(self):
        """Testing validate_only_contains method"""

        error_list = []
        detail_error = "'first_name' field can only contain characters!"

        self.instance.validate_only_contains("1wqew", "first_name", error_list)
        assert len(error_list) == 1, error_list
        assert detail_error == error_list[0], error_list[0]

        self.instance.validate_only_contains("qweq_q1", "first_name", error_list)
        assert len(error_list) == 2, error_list
        assert detail_error == error_list[1], error_list[1]

        self.instance.validate_only_contains("wqeq1", "first_name", error_list)
        assert len(error_list) == 3, error_list
        assert detail_error == error_list[2], error_list[2]

        self.instance.validate_only_contains("_qweqweqweqe_", "first_name", error_list)
        assert len(error_list) == 3, error_list
    
    def test_validate_min_length(self):
        """Testing validate_min_length method"""

        error_list = []
        detail_error = "'first_name' field must be longer than or equal to 5 characters!"

        self.instance.validate_min_length("qwe1", "first_name", error_list)
        assert len(error_list) == 1, error_list
        assert detail_error == error_list[0], error_list[0]

        self.instance.validate_min_length("_@1e", "first_name", error_list)
        assert len(error_list) == 2, error_list
        assert detail_error == error_list[1], error_list[1]

        self.instance.validate_min_length("qwe/qwe13", "first_name", error_list, 10)
        assert len(error_list) == 3, error_list
        assert "'first_name' field must be longer than or equal to 10 characters!" == error_list[2], error_list[2]

        self.instance.validate_min_length("qwerq131qw", "first_name", error_list)
        assert len(error_list) == 3, error_list
    
    def test_validate_max_length(self):
        """Testing validate_max_length method"""

        error_list = []
        detail_error = "'first_name' field must be less than or equal to 30 characters!"

        self.instance.validate_max_length("qweqweqwe123123!@#qweq123123!@#", "first_name", error_list)
        assert len(error_list) == 1, error_list
        assert detail_error == error_list[0], error_list[0]

        self.instance.validate_max_length("qweqweqwe123123!@#qweq123123!@#qwe", "first_name", error_list)
        assert len(error_list) == 2, error_list
        assert detail_error == error_list[1], error_list[1]

        self.instance.validate_max_length("qweqweqwe123123!@#qweq123123!@", "first_name", error_list, 25)
        assert len(error_list) == 3, error_list
        assert "'first_name' field must be less than or equal to 25 characters!" == error_list[2], error_list[2]

        self.instance.validate_max_length("qwerq131qw", "first_name", error_list)
        assert len(error_list) == 3, error_list


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

        error_msg = "Only JPEG, PNG, ICO files are accepted!!"
        
        photo = self.Photo(name="string.jpg")
        response = self.instance.validate_photo(photo)
        assert response.name == "string.jpg", response.name

        photo = self.Photo(name="photo.png")
        response = self.instance.validate_photo(photo)
        assert response.name == "photo.png", response.name

        photo = self.Photo(name="string.py")
        with self.assertRaisesMessage(ValidationError, error_msg):
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

        error_msg = "'First name' field can only contain characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_first_name("1stri ")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_first_name("str1 ")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_first_name("str`")
        
        error_msg = "'First name' field must be less than or equal to 30 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_first_name("  stringstrings stringstringstringstring  ")
    
    def test_validate_last_name(self):
        """Testing validate_last_name method"""
        
        response = self.instance.validate_last_name("  string ")
        assert response == "string", response

        error_msg = "'Last name' field can only contain characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_last_name("1stri ")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_last_name("str1 ")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_last_name("str`")
        
        error_msg = "'Last name' field must be less than or equal to 30 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_last_name("  stringstringsst ringstringstringstring  ")
    
    def test_validate_email(self):
        """Testing validate_last_name method"""
        
        response = self.instance.validate_email("  string@gmail.com ")
        assert response == "string@gmail.com", response

        response = self.instance.validate_email("str123ing@gmail.com")
        assert response == "str123ing@gmail.com", response

        response = self.instance.validate_email("email_123@gmail.com")
        assert response == "email_123@gmail.com", response

        error_msg = "'Email' field can only numbers, letters and underscore!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_email(" stqqqr`@gmail.com ")

        error_msg = "First character of 'Email' field can only contain characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_email("1stri@gmail.com ")
        
        error_msg = "'Email' field must be less than or equal to 30 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_email("  stringstringsstringstringstringstring@gmail.com  ")
    
    def test_validate_mobile_number(self):
        """Testing validate_mobile_number method"""
        
        response = self.instance.validate_mobile_number("  1234567891011 ")
        assert response == "1234567891011", response

        response = self.instance.validate_mobile_number("  12345678910112312313 ")
        assert response == "12345678910112312313", response

        error_msg = "'mobile_number' field can only numbers characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_mobile_number("+312313131313133 ")
        
        error_msg = "'mobile_number' field must be less than or equal to 20 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_mobile_number("1234567890123456789011")


class TestSignUpSerializer(APITestCase):
    """Testing SignUpSerializer methods"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.instance = serializers.SignUpSerializer()
        cls.instance.initial_data = {"password1": "passwordPassword"}
    
    def test_validate_username(self):
        """Testing validate_username method"""
        
        response = self.instance.validate_username("  string ")
        assert response == "string", response

        response = self.instance.validate_username("str123ing")
        assert response == "str123ing", response

        response = self.instance.validate_username(" stqqqr ")
        assert response == "stqqqr", response

        error_msg = "'Username' field must be longer than or equal to 5 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_username("stri")

        error_msg = "First character of 'Username' field can only contain characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_username("1stri")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_username("1stri@gmail.com ")
        
        error_msg = "'Username' field can only numbers, letters and underscore!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_username("  stringstrings stringstringstringstring@gmail.com  ")
        
        error_msg = "'Username' field must be less than or equal to 30 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_username("  stringstrings stringstringstringstring@gmail.com  ")
    
    def test_validate_first_name(self):
        """Testing validate_first_name method"""
        
        response = self.instance.validate_first_name("  string ")
        assert response == "string", response

        error_msg = "'First name' field must be longer than or equal to 5 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_first_name("stri")

        error_msg = "'First name' field can only contain characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_first_name("1stri")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_first_name("1stri@gmail.com ")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_first_name("  stringstrings stringstringstringstring@gmail.com  ")
        
        error_msg = "'First name' field must be less than or equal to 30 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_first_name("  stringstrings stringstringstringstring@gmail.com  ")
    
    def test_validate_last_name(self):
        """Testing validate_last_name method"""
        
        response = self.instance.validate_last_name("  string ")
        assert response == "string", response

        error_msg = "'Last name' field must be longer than or equal to 5 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_last_name("stri")

        error_msg = "'Last name' field can only contain characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_last_name("1stri")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_last_name("1stri@gmail.com ")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_last_name("  stringstrings stringstringstringstring@gmail.com  ")
        
        error_msg = "'Last name' field must be less than or equal to 30 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_last_name("  stringstrings stringstringstringstring@gmail.com  ")
    
    def test_validate_email(self):
        """Testing validate_last_name method"""
        
        response = self.instance.validate_email("  string@gmail.com ")
        assert response == "string@gmail.com", response

        response = self.instance.validate_email("str123ing@gmail.com")
        assert response == "str123ing@gmail.com", response

        response = self.instance.validate_email("email_123@gmail.com")
        assert response == "email_123@gmail.com", response

        error_msg = "First character of 'Email' field can only contain characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_email("1stri@gmail.com ")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_email(" 1ema@gmail.com ")
        
        error_msg = "'Email' field can only numbers, letters and underscore!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_email(" stqqqr`@gmail.com ")
        
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_email("  stringstrings stringstringstringstring@gmail.com  ")
        
        error_msg = "'Email' field must be less than or equal to 30 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_email("  stringstringsstringstringstringstring@gmail.com  ")
    
    def test_validate_mobile_number(self):
        """Testing validate_mobile_number method"""
        
        response = self.instance.validate_mobile_number("  1234567891011 ")
        assert response == "1234567891011", response

        response = self.instance.validate_mobile_number("  12345678910112312313 ")
        assert response == "12345678910112312313", response

        error_msg = "'mobile_number' field can only numbers characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_mobile_number("+312313131313133 ")
        
        error_msg = "'mobile_number' field must be less than or equal to 20 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_mobile_number("1234567890123456789011")
    
    def test_validate_password1(self):
        """Testing validate_password1 method"""

        response = self.instance.validate_password1("  qwe123qwesd123_qwe1 ")
        assert response == "qwe123qwesd123_qwe1", response

        response = self.instance.validate_password1("  qwe12 11_123 ")
        assert response == "qwe12 11_123", response

        error_msg = "'Password' field must be longer than or equal to 10 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_password1(" qwe1+we")
        
        error_msg = "'Password' field must be less than or equal to 50 characters!"
        with self.assertRaisesMessage(ValidationError, error_msg):
            response = self.instance.validate_password1("  stringstrings stringstringstringstring@gmail.comqqq  ")
    

    def test_validate_password2(self):
        """Testing validate_password2 method"""

        with self.assertRaisesMessage(ValidationError, "Password mismatch!"):
            self.instance.validate_password2("password")

        with self.assertRaisesMessage(ValidationError, "Password mismatch!"):
            self.instance.validate_password2("passwordpassword")

        with self.assertRaisesMessage(ValidationError, "Password mismatch!"):
            self.instance.validate_password2("  passwordPassword  ")

        response = self.instance.validate_password2("passwordPassword")
        assert response == "passwordPassword", response


class TestResetPasswordSerializer(APITestCase):
    """Testing ResetPasswordSerializer class methods"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.instance = serializers.ResetPasswordSerializer()
        cls.instance.initial_data = {
            "old_password": "hight_password123",
            "new_password": "passwordPassword"
            }
    
    def test_validate_new_password(self):
        """Testing validate_new_password method"""

        with self.assertRaisesMessage(ValidationError, "'New password' field must be longer than or equal to 10 characters!"):
            self.instance.validate_new_password("password")
        
        with self.assertRaisesMessage(ValidationError, "'New password' field must be less than or equal to 50 characters!"):
            self.instance.validate_new_password("password" * 7)

        with self.assertRaisesMessage(ValidationError, "The new password cannot be similar to the old one."):
            self.instance.validate_new_password("  hight_password123  ")
        
        response = self.instance.validate_new_password("Hight_password123")
        assert response == "Hight_password123", response

        response = self.instance.validate_new_password("  passwordPassword  ")
        assert response == "passwordPassword", response
    
    def test_validate_confirm_password(self):
        """Testing validate_confirm_password method"""

        with self.assertRaisesMessage(ValidationError, "Password mismatch!"):
            self.instance.validate_confirm_password("password")

        with self.assertRaisesMessage(ValidationError, "Password mismatch!"):
            self.instance.validate_confirm_password("passwordpassword")

        with self.assertRaisesMessage(ValidationError, "Password mismatch!"):
            self.instance.validate_confirm_password("  passwordPassword  ")

        response = self.instance.validate_confirm_password("passwordPassword")
        assert response == "passwordPassword", response
