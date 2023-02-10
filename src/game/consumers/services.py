from channels.db import database_sync_to_async

from .. import models


def create_column_dict(column_name_list: list, board: list) -> dict:
    """Create dictionary of columns from list board of columns"""

    column_dict = {column_name: board[index] for index, column_name in enumerate(column_name_list)}
    return column_dict



@database_sync_to_async
def get_map(board_id: int, column_dict: dict) -> None:
    """Get map for update"""

    models.Map.objects.filter(id=board_id).update(**column_dict)
