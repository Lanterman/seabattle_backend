from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from src.game import serializers


class TestCreateLobbySerializer(APITestCase):
    """Testing CreateLobbySerializer filter"""
    
    def test_validate_name(self):
        """Testing validate_name method"""
        
        instance = serializers.CreateLobbySerializer()
        filtered_queryset = instance.validate_name("string ")
        assert filtered_queryset == "string", filtered_queryset

        filtered_queryset = instance.validate_name(" string1 ")
        assert filtered_queryset == "string1", filtered_queryset

        with self.assertRaises(ValidationError):
            filtered_queryset = instance.validate_name("str!ing")

        with self.assertRaises(ValidationError):
            filtered_queryset = instance.validate_name("1string")
