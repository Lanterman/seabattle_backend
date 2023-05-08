import uuid

from ..models import Lobby, Board


def determine_winner_at_preparation_stage(lobby_slug: uuid) -> None:
    """Determine the winner at the preparation stage"""

    lobby = Lobby.objects.get(slug=lobby_slug)
    Board.objects.filter(lobby_id=lobby.id).update(is_play_again=False)
    boards = Board.objects.filter(lobby_id=lobby.id, is_ready=True)
    if len(boards) == 1:
        Lobby.objects.filter(slug=lobby_slug).update(winner=boards[0].user_id.username)
    else:
        Lobby.objects.filter(slug=lobby_slug).update(winner="Both lose!")


def determine_winner_at_shot_stage(lobby_slug: uuid) -> None:
    """Determine the winner at the shot stage"""

    lobby = Lobby.objects.get(slug=lobby_slug)
    if not lobby.winner:
        Board.objects.filter(lobby_id=lobby.id).update(is_play_again=False)
        username = Board.objects.get(lobby_id=lobby.id, is_my_turn=False).user_id.username
        lobby.winner = username
        lobby.save()