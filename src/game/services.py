from django.db import models

column_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
ship_count_dict = {
    "fourdeck": 1,
    "tripledeck": 2,
    "singledeck": 4,
    "doubledeck": 3    
}


class Bet(models.IntegerChoices):
    """Choose a bet on the game"""

    FIVE = 5, "5$"
    TEN = 10, "10$"
    TWENTY_FIVE = 25, "25$"
    FIFTY = 50, "50$"
    ONE_HUNDRED = 100, "100$"
    TWO_HUNDRED_FIFTY = 250, "250$"
    FIVE_HUNDRED = 500, "500$"
    ONE_THOUSAND = 1000, "1000$"


class ChooseTime(models.IntegerChoices):
    """Choose time"""

    THIRTY_SECONDS = 30, "30 sec"
    SIXTY_SECONDS = 60, "60 sec"
    NINTY_SECONDS = 90, "90 sec"


class ChooseBotLevel(models.TextChoices):
    """Choose time"""

    EASY = "EASY", "EASY"
    MEDIUM = "MEDIUM", "MEDIUM"
    HIGH = "HIGH", "HIGH"


def clear_enemy_board(user, boards) -> tuple:
    """Сlears the enemy table from ships and the space around them"""

    if boards[0]["user_id"]:
        if boards[0]["user_id"] == user.id:
            index, enemy_board = (1, boards[1])
        else:
            index, enemy_board = (0, boards[0])
    else:
        if boards[1]["user_id"] == user.id:
            index, enemy_board = (0, boards[0])
        else:
            index, enemy_board = (1, boards[1])

    for key, value in enemy_board.items():
        if key in column_name_list:
            for column_name, column_value in value.items():
                if column_value not in ("", "hit", "miss"):
                    enemy_board[key][column_name] = ""

    return index, enemy_board
