import uuid

from datetime import datetime
from channels.db import database_sync_to_async

from .. import models
from ...user import models as user_models


@database_sync_to_async
def get_board(board_id: int, column_name_list: list) -> models.Board:
    """Get enemy board"""

    query = models.Board.objects.values(*column_name_list).get(id=board_id)
    return query


@database_sync_to_async
def update_board(board_id: int, board: dict) -> None:
    """Get board for update"""

    models.Board.objects.filter(id=board_id).update(**board)


@database_sync_to_async
def update_board_is_ready(board_id: int, is_ready: bool) -> None:
    """Update a board is ready field"""

    models.Board.objects.filter(id=board_id).update(is_ready=is_ready)


@database_sync_to_async
def get_ships(board_id: int) -> list:
    """Get ships for the board"""

    query = models.Ship.objects.filter(board_id=board_id)
    return list(query)


@database_sync_to_async
def update_count_of_ship(ship_id: int, ship_count: int) -> None:
    """Update count of a ship"""

    models.Ship.objects.filter(id=ship_id).update(count=ship_count - 1)


@database_sync_to_async
def update_count_of_ships(ships: list, ship_count_tuple: tuple) -> None:
    """Update ships to database"""

    ships[0].count = ship_count_tuple[0]
    ships[1].count = ship_count_tuple[1]
    ships[2].count = ship_count_tuple[2]
    ships[3].count = ship_count_tuple[3]
    models.Ship.objects.bulk_update(ships, ["count"])


@database_sync_to_async
def clear_count_of_ships(board_id: int) -> None:
    """Update ships count field to database"""

    models.Ship.objects.filter(board_id=board_id).update(count=0)


@database_sync_to_async
def get_lobby_boards(lobby_slug: uuid) -> list:
    """Get lobby boards"""

    query = models.Board.objects.select_related("lobby_id").filter(lobby_id__slug=lobby_slug)
    return list(query)


@database_sync_to_async
def update_boards(bool_value: bool, my_board, enemy_board) -> list:
    """Update your_turn field of Boards model instances"""

    my_board.is_my_turn = bool_value
    enemy_board.is_my_turn = not bool_value
    models.Board.objects.bulk_update([my_board, enemy_board], ["is_my_turn"])


@database_sync_to_async
def get_lobby_by_slug(slug: uuid) -> models.Lobby:
    """Get the Lobby models instance"""

    query = models.Lobby.objects.get(slug=slug)
    return query


@database_sync_to_async
def set_winner_in_lobby(lobby_slug: uuid, username: str) -> None:
    """Set winner in a lobby"""

    models.Lobby.objects.filter(slug=lobby_slug).update(winner=username, finished_in=datetime.now())


@database_sync_to_async
def get_user(id: int) -> str:
    """Get user by ID and return his username"""

    query = user_models.User.objects.get(id=id)
    return query.username


@database_sync_to_async
def add_user_to_lobby(lobby: models.Lobby, user: models.User) -> None:
    """Add a second user to a lobby"""

    lobby.users.add(user)



@database_sync_to_async
def update_user_id_of_board(board_id: int, user_id: int) -> None:
    """Update a user_id field of a lobby model instance"""

    models.Board.objects.filter(id=board_id).update(user_id=user_id)


@database_sync_to_async
def create_message(lobby_id: int, username: str, message: str, is_bot: bool) -> None:
    """Create message model instance and return it"""

    query = models.Message.objects.create(message=message, owner=username, is_bot=is_bot, lobby_id_id=lobby_id)
    return query


@database_sync_to_async
def update_play_again_field(board_id: int, answer: bool) -> None:
    """Update play again field of Board model instance"""

    models.Board.objects.filter(id=board_id).update(is_play_again=answer)
