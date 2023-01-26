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
    slug: uuid = models.UUIDField(max_length=250, verbose_name="URL", default=uuid.uuid4, help_text="Required")
    created_in: datetime.datetime = models.DateTimeField(auto_now_add=True)
    finished_in: datetime.datetime = models.DateTimeField(blank=True, null=True)
    bet: int = models.IntegerField("game bet", choices=utilities.Bet.choices, help_text="Required")
    time_to_move: int = models.IntegerField("time to move", choices=utilities.TimePerMove.choices, help_text="Required")
    password: str = models.CharField(max_length=100, blank=True)
    winner: str = models.CharField(max_length=150, blank=True)
    users: Optional[list[User]] = models.ManyToManyField(to=User, related_name="lobbies", help_text="Required")

    class Meta:
        verbose_name = "Lobby"
        verbose_name_plural = "Lobbies"
        ordering = ["bet", "created_in", "finished_in"]
        unique_together = ["slug"]

    def __str__(self):
        return f"{self.id} - name: {self.name}"

    def get_absolute_url(self):
        return reverse('lobby_detail', kwargs={'lobby_detail': self.slug})


class Map(models.Model):
    """Game map model"""

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
    lobby_id: Lobby = models.ForeignKey(to=Lobby, verbose_name="lobby", on_delete=models.CASCADE, related_name="maps")
    user_id: User = models.ForeignKey(to=User, verbose_name="user", on_delete=models.CASCADE, related_name="map_set", blank=True, null=True)

    class Meta:
        verbose_name = "Map"
        verbose_name_plural = "Maps"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id} - name: {self.lobby_id}"
