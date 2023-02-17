import logging

from channels.db import database_sync_to_async

from .. import models


def create_column_dict(column_name_list: list, board: list) -> dict:
    """Create dictionary of columns from list board of columns"""

    column_dict = {column_name: board[index] for index, column_name in enumerate(column_name_list)}
    return column_dict


@database_sync_to_async
def get_board(board_id: int) -> models.Board:
    """Get enemy board"""

    query = models.Board.objects.get(id=board_id)
    return query


@database_sync_to_async
def update_board(board_id: int, column_dict: dict) -> None:
    """Get board for update"""

    models.Board.objects.filter(id=board_id).update(**column_dict)


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
