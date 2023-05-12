from . import models


def create_lobby_boards(lobby_id: int, first_user_id: int, second_user_id: int = None) -> tuple[int]:
    """Create lobby boards"""

    first_board, second_board = models.Board.objects.bulk_create([
        models.Board(lobby_id_id=lobby_id, user_id_id=first_user_id),
        models.Board(lobby_id_id=lobby_id, user_id_id=second_user_id)
    ])
    return first_board.id, second_board.id


def create_ships_for_boards(first_board_id: int, second_board_id: int) -> None:
    """Create shipf for boards"""

    models.Ship.objects.bulk_create([
        models.Ship(name="singledeck", size=1, count=4, board_id_id=first_board_id),
        models.Ship(name="doubledeck", size=2, count=3, board_id_id=first_board_id),
        models.Ship(name="tripledeck", size=3, count=2, board_id_id=first_board_id),
        models.Ship(name="fourdeck", size=4, count=1, board_id_id=first_board_id),
        models.Ship(name="singledeck", size=1, count=4, board_id_id=second_board_id),
        models.Ship(name="doubledeck", size=2, count=3, board_id_id=second_board_id),
        models.Ship(name="tripledeck", size=3, count=2, board_id_id=second_board_id),
        models.Ship(name="fourdeck", size=4, count=1, board_id_id=second_board_id),
    ])