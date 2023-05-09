from rest_framework.test import APITestCase

from src.game.celery_tasks.services import determine_winner_at_preparation_stage, determine_winner_at_shot_stage
from src.game.models import Lobby, Board


class TestAtPreparationStage(APITestCase):
    """Testing the determine_winner_at_preparation_stage function"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        cls.lobby_1 = Lobby.objects.get(id=1)
        cls.lobby_2 = Lobby.objects.get(id=2)

        cls.boards_lobby_1 = Board.objects.filter(lobby_id=cls.lobby_1.id)
        cls.boards_lobby_2 = Board.objects.filter(lobby_id=cls.lobby_2.id)

    def test_first_lobby(self):
        """Testing first lobby"""

        assert self.lobby_1.winner == "", self.lobby_1.winner
        assert self.boards_lobby_1[0].is_play_again == None, self.boards_lobby_1[0].is_play_again
        assert self.boards_lobby_1[1].is_play_again == None, self.boards_lobby_1[1].is_play_again

        determine_winner_at_preparation_stage(self.lobby_1.slug)
        self.lobby_1.refresh_from_db()

        assert self.lobby_1.winner == "Both lose!", self.lobby_1.winner
        assert self.boards_lobby_1[0].is_play_again == False, self.boards_lobby_1[0].is_play_again
        assert self.boards_lobby_1[1].is_play_again == False, self.boards_lobby_1[1].is_play_again
    
    def test_second_lobby(self):
        """Testing second lobby"""

        assert self.lobby_2.winner == "lanterman", self.lobby_2.winner
        assert self.boards_lobby_2[0].is_play_again == True, self.boards_lobby_2[0].is_play_again
        assert self.boards_lobby_2[1].is_play_again == False, self.boards_lobby_2[1].is_play_again

        determine_winner_at_preparation_stage(self.lobby_2.slug)
        self.lobby_2.refresh_from_db()
        
        assert self.lobby_2.winner == "Both lose!", self.lobby_2.winner
        assert self.boards_lobby_2[0].is_play_again == False, self.boards_lobby_2[0].is_play_again
        assert self.boards_lobby_2[1].is_play_again == False, self.boards_lobby_2[1].is_play_again

        
class TestAtShotStage(APITestCase):
    """Testing the determine_winner_at_shot_stage function"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        cls.lobby_1 = Lobby.objects.get(id=1)
        cls.lobby_2 = Lobby.objects.get(id=2)

        cls.boards_lobby_1 = Board.objects.filter(lobby_id=cls.lobby_1.id)
        cls.boards_lobby_2 = Board.objects.filter(lobby_id=cls.lobby_2.id)

    def test_first_lobby(self):
        """Testing first lobby"""

        assert self.lobby_1.winner == "", self.lobby_1.winner
        assert self.boards_lobby_1[0].is_play_again == None, self.boards_lobby_1[0].is_play_again
        assert self.boards_lobby_1[1].is_play_again == None, self.boards_lobby_1[1].is_play_again

        determine_winner_at_shot_stage(self.lobby_1.slug)
        self.lobby_1.refresh_from_db()

        assert self.lobby_1.winner == "admin", self.lobby_1.winner
        assert self.boards_lobby_1[0].is_play_again == False, self.boards_lobby_1[0].is_play_again
        assert self.boards_lobby_1[1].is_play_again == False, self.boards_lobby_1[1].is_play_again
    
    def test_second_lobby(self):
        """Testing second lobby"""

        assert self.lobby_2.winner == "lanterman", self.lobby_2.winner
        assert self.boards_lobby_2[0].is_play_again == True, self.boards_lobby_2[0].is_play_again
        assert self.boards_lobby_2[1].is_play_again == False, self.boards_lobby_2[1].is_play_again

        determine_winner_at_shot_stage(self.lobby_2.slug)
        self.lobby_2.refresh_from_db()
        
        assert self.lobby_2.winner == "lanterman", self.lobby_2.winner
        assert self.boards_lobby_2[0].is_play_again == True, self.boards_lobby_2[0].is_play_again
        assert self.boards_lobby_2[1].is_play_again == False, self.boards_lobby_2[1].is_play_again
