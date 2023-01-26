from django.db import models


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


class TimePerMove(models.IntegerChoices):
    """Time to move"""

    THIRTY_SECONDS = 30, "30 sec"
    SIXTY_SECONDS = 60, "60 sec"
    NINTY_SECONDS = 90, "90 sec"


def column_generate(column_name: str) -> str:
    """Generate a string as a dictionary"""

    return str({f"{column_name}{element}": "" for element in range(1, 11)})
