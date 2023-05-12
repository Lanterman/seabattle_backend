import datetime
import uuid

from typing import Optional
from django.db import models
from django.urls.base import reverse
from config import settings, utilities


User = settings.AUTH_USER_MODEL


class Lobby(models.Model):
    """Lobby model"""

    name: str = models.CharField("lobby name", max_length=100, help_text="Required")
    slug: uuid.uuid4 = models.UUIDField(
        max_length=250, verbose_name="URL", default=uuid.uuid4, help_text="Required", db_index=True
        )
    created_in: datetime.datetime = models.DateTimeField(auto_now_add=True)
    finished_in: datetime.datetime = models.DateTimeField(blank=True, null=True)
    bet: int = models.IntegerField("game bet", choices=utilities.Bet.choices, help_text="Required")
    time_to_move: int = models.IntegerField(
        choices=utilities.ChooseTime.choices, default=utilities.ChooseTime.THIRTY_SECONDS
        )
    time_to_placement: int = models.IntegerField(
        choices=utilities.ChooseTime.choices, default=utilities.ChooseTime.THIRTY_SECONDS
        )
    password: str = models.CharField(max_length=100, blank=True)
    winner: str = models.CharField(max_length=150, blank=True)
    users: Optional[list[User]] = models.ManyToManyField(to=User, related_name="lobbies", help_text="Required")

    class Meta:
        verbose_name = "Lobby"
        verbose_name_plural = "Lobbies"
        ordering = ["bet", "created_in", "finished_in"]
        unique_together = ["slug"]

    def __str__(self):
        return f"lobby {self.name}"

    def get_absolute_url(self):
        return reverse('lobby-detail', kwargs={'slug': self.slug})


class Board(models.Model):
    """Game board model"""

    A: str = models.TextField("column A", default=utilities.column_generate("A"))
    B: str = models.TextField("column B", default=utilities.column_generate("B"))
    C: str = models.TextField("column C", default=utilities.column_generate("C"))
    D: str = models.TextField("column D", default=utilities.column_generate("D"))
    E: str = models.TextField("column E", default=utilities.column_generate("E"))
    F: str = models.TextField("column F", default=utilities.column_generate("F"))
    G: str = models.TextField("column G", default=utilities.column_generate("G"))
    H: str = models.TextField("column H", default=utilities.column_generate("H"))
    I: str = models.TextField("column I", default=utilities.column_generate("I"))
    J: str = models.TextField("column J", default=utilities.column_generate("J"))
    is_ready: bool = models.BooleanField("is ready", default=False)
    is_my_turn: bool = models.BooleanField("is my turn", default=False)
    is_play_again: bool = models.BooleanField("is play again", null=True)
    lobby_id: Lobby = models.ForeignKey(to=Lobby, verbose_name="lobby", on_delete=models.CASCADE, related_name="boards")
    user_id: User = models.ForeignKey(
        to=User, verbose_name="user", on_delete=models.CASCADE, related_name="board_set", blank=True, null=True
    )

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        ordering = ["id"]

    def __str__(self):
        return f"board {self.id}: {self.lobby_id}"


class Ship(models.Model):
    """Ship model"""

    name: str = models.CharField("name", max_length=20)
    plane: str = models.CharField("plane", max_length=10, default="horizontal")
    size: int = models.IntegerField("size")
    count: int = models.IntegerField("count")
    board_id: Board = models.ForeignKey(to=Board, verbose_name="map", on_delete=models.CASCADE, related_name="ships")

    class Meta:
        verbose_name = "Ship"
        verbose_name_plural = "Ships"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id} - name: {self.name}"


class Message(models.Model):
    """Message model"""

    message: str = models.TextField("message", max_length=300)
    owner: str = models.CharField("owner", max_length=150)
    is_bot: bool = models.BooleanField("is bot", default=False)
    created_in: datetime.datetime = models.DateTimeField(auto_now_add=True)
    lobby_id: Lobby = models.ForeignKey(to=Lobby, on_delete=models.CASCADE, related_name="messages", verbose_name="lobby")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-id"]
    
    def _str_(self):
        return f"Chat message {self.id}"
