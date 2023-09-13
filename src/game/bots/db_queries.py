import uuid

from channels.db import database_sync_to_async

from .. import models
from src.user.models import User


@database_sync_to_async
def create_lobby(name: str, bet: int, time_to_move: int, time_to_placement: int, user: User) -> tuple[int, uuid.uuid4]:
    """Create lobby"""

    query = models.Lobby.objects.create(
        name=name, bet=bet, time_to_move=time_to_move, time_to_placement=time_to_placement, is_play_with_a_bot=True
    )
    query.users.add(user)
    return query.id, query.slug
