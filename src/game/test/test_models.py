from rest_framework.test import APITestCase

from src.game import models


class TestLobbyModel(APITestCase):
    """Testing Lobby model"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.lobby_1 = models.Lobby.objects.get(id=1)
        cls.lobby_2 = models.Lobby.objects.get(id=2)
    
    def test__str__method(self):
        """Testing __str__ method"""

        response = self.lobby_1.__str__()
        assert response == "lobby string", response

        response = self.lobby_2.__str__()
        assert response == "lobby string1", response
    
    def test_get_absolute_url_method(self):
        """Testing get_absolute_url method"""

        response = self.lobby_1.get_absolute_url()
        assert response == "/api/v1/lobbies/acf08b23-eed2-4fbf-9d60-53062500aff3/", response

        response = self.lobby_2.get_absolute_url()
        assert response == "/api/v1/lobbies/15505266-28a3-4620-b616-a1cfbe6ce300/", response


class TestBoardModel(APITestCase):
    """Testing Board model"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.board_1 = models.Board.objects.get(id=1)
        cls.board_2 = models.Board.objects.get(id=2)
        cls.board_3 = models.Board.objects.get(id=3)

    def test__str__method(self):
        """Testing __str__ method"""

        response = self.board_1.__str__()
        assert response == "board 1: lobby string", response

        response = self.board_2.__str__()
        assert response == "board 2: lobby string", response

        response = self.board_3.__str__()
        assert response == "board 3: lobby string1", response


class TestShipModel(APITestCase):
    """Testing Ship model"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.ship_1 = models.Ship.objects.get(id=1)
        cls.ship_2 = models.Ship.objects.get(id=5)
        cls.ship_3 = models.Ship.objects.get(id=9)
        cls.ship_4 = models.Ship.objects.get(id=13)

    def test__str__method(self):
        """Testing __str__ method"""

        response = self.ship_1.__str__()
        assert response == "1 - name: fourdeck", response

        response = self.ship_2.__str__()
        assert response == "5 - name: tripledeck", response

        response = self.ship_3.__str__()
        assert response == "9 - name: doubledeck", response

        response = self.ship_4.__str__()
        assert response == "13 - name: singledeck", response


class TestMessageModel(APITestCase):
    """Testing Message model"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.message_1 = models.Message.objects.get(id=1)
        cls.message_2 = models.Message.objects.get(id=2)
    
    def test__str__method(self):
        """Testing __str__ method"""

        response = self.message_1.__str__()
        assert response == "Chat message 1", response

        response = self.message_2.__str__()
        assert response == "Chat message 2", response
