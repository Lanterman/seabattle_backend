import logging

from rest_framework.test import APITestCase

from src.game.celery_tasks import tasks
from src.game.models import Lobby, Board
from config.celery import debug_task
from config.utilities import redis_instance


class TestCountDownTask(APITestCase):
    """Testing the countdown task"""

    fixtures = ["./src/game/consumers/test/test_data.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        info = f"{cls.__name__}: Number of keys in Redis database before running tests: {len(redis_instance.keys())}"
        logging.info(info)

        cls.lobby_1 = Lobby.objects.get(id=1)
        cls.lobby_2 = Lobby.objects.get(id=2)

        cls.boards_lobby_1 = Board.objects.filter(lobby_id=cls.lobby_1.id)
        cls.boards_lobby_2 = Board.objects.filter(lobby_id=cls.lobby_2.id)

        cls.slug_lobby_1 = str(cls.lobby_1.slug)
        cls.slug_lobby_2 = str(cls.lobby_2.slug)

        redis_instance.hset(name=cls.slug_lobby_1, mapping={"current_turn": 1})
        redis_instance.hset(name=cls.slug_lobby_2, mapping={"current_turn": 0})
    
    @classmethod
    def tearDownClass(cls) -> None:
        info = f"{cls.__name__}: Number of keys in Redis database before closing: {len(redis_instance.keys())}"
        logging.info(info)
        redis_instance.delete(cls.slug_lobby_1, cls.slug_lobby_2)
        super().tearDownClass()
    
    def test_first_lobby_at_shot_stage_0(self):
        """Testing first lobby at shot stage with old turn 0"""

        assert self.lobby_1.winner == "", self.lobby_1.winner
        assert self.boards_lobby_1[0].is_play_again == None, self.boards_lobby_1[0].is_play_again
        assert self.boards_lobby_1[1].is_play_again == None, self.boards_lobby_1[1].is_play_again

        with self.assertLogs():
            tasks.countdown(self.slug_lobby_1, 1, "0")
        self.lobby_1.refresh_from_db()

        assert self.lobby_1.winner == "", self.lobby_1.winner
        assert self.boards_lobby_1[0].is_play_again == None, self.boards_lobby_1[0].is_play_again
        assert self.boards_lobby_1[1].is_play_again == None, self.boards_lobby_1[1].is_play_again

    def test_first_lobby_at_shot_stage_0_by_write_winner(self):
        """Testing first lobby at shot stage with old turn 0 with write winner"""

        assert self.lobby_1.winner == "", self.lobby_1.winner
        assert self.boards_lobby_1[0].is_play_again == None, self.boards_lobby_1[0].is_play_again
        assert self.boards_lobby_1[1].is_play_again == None, self.boards_lobby_1[1].is_play_again

        with self.assertLogs():
            tasks.countdown(self.slug_lobby_1, 0, "0")
        self.lobby_1.refresh_from_db()

        assert self.lobby_1.winner == "admin", self.lobby_1.winner
        assert self.boards_lobby_1[0].is_play_again == False, self.boards_lobby_1[0].is_play_again
        assert self.boards_lobby_1[1].is_play_again == False, self.boards_lobby_1[1].is_play_again
    
    def test_first_lobby_at_shot_stage_1(self):
        """Testing first lobby at shot stage with old turn 1"""

        assert self.lobby_1.winner == "", self.lobby_1.winner
        assert self.boards_lobby_1[0].is_play_again == None, self.boards_lobby_1[0].is_play_again
        assert self.boards_lobby_1[1].is_play_again == None, self.boards_lobby_1[1].is_play_again

        with self.assertLogs():
            tasks.countdown(self.slug_lobby_1, 1, "1")
        self.lobby_1.refresh_from_db()

        assert self.lobby_1.winner == "admin", self.lobby_1.winner
        assert self.boards_lobby_1[0].is_play_again == False, self.boards_lobby_1[0].is_play_again
        assert self.boards_lobby_1[1].is_play_again == False, self.boards_lobby_1[1].is_play_again
    
    def test_second_lobby_at_preparation_stage_0(self):
        """Testing second lobby at preparation stage with old turn 0"""

        assert self.lobby_2.winner == "lanterman", self.lobby_2.winner
        assert self.boards_lobby_2[0].is_play_again == True, self.boards_lobby_2[0].is_play_again
        assert self.boards_lobby_2[1].is_play_again == False, self.boards_lobby_2[1].is_play_again

        with self.assertLogs():
            tasks.countdown(self.slug_lobby_2, 1, "0")
        self.lobby_2.refresh_from_db()
        
        assert self.lobby_2.winner == "Both lose!", self.lobby_2.winner
        assert self.boards_lobby_2[0].is_play_again == False, self.boards_lobby_2[0].is_play_again
        assert self.boards_lobby_2[1].is_play_again == False, self.boards_lobby_2[1].is_play_again


class TestDebugTask(APITestCase):
    """Testing debug_task celery task"""

    def test_debug_task(self):
        with self.assertLogs(level="INFO"):
            response = debug_task()
        
        assert response == None, response
