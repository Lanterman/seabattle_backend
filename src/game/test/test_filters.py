from rest_framework.test import APITestCase

from src.game import models, filters


class TestLobbyFilter(APITestCase):
    """Testing LobbyFilter filter"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.lobby_list = models.Lobby.objects.all()

        cls.instance = filters.LobbyFilter()
    
    def test_filter_name(self):
        """Testing filter_name method"""
        
        filtered_queryset = self.instance.filter_name(self.lobby_list, "name", "ring")
        assert len(filtered_queryset) == 2, filtered_queryset

        filtered_queryset = self.instance.filter_name(self.lobby_list, "name", "1")
        assert len(filtered_queryset) == 1, filtered_queryset

        filtered_queryset = self.instance.filter_name(self.lobby_list, "name", "strign")
        assert len(filtered_queryset) == 0, filtered_queryset
    
    def test_filter_is_private(self):
        """Testing filter_is_private method"""
        
        filtered_queryset = self.instance.filter_is_private(self.lobby_list, "is_private", True)
        assert len(filtered_queryset) == 1, filtered_queryset
        assert filtered_queryset[0].name == "string", filtered_queryset

        filtered_queryset = self.instance.filter_is_private(self.lobby_list, "is_private", False)
        assert len(filtered_queryset) == 1, filtered_queryset
        assert filtered_queryset[0].name == "string1", filtered_queryset