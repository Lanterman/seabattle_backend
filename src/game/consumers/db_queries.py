from channels.db import database_sync_to_async

from .. import models


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
def clear_count_of_ships(board_id) -> None:
    """Update ships count field to database"""

    models.Ship.objects.filter(board_id=board_id).update(count=0)