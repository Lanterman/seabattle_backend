from channels.db import database_sync_to_async

from .. import models


class RefreshBoard:

    @database_sync_to_async
    def get_map(board_id: int) -> models.Map:
        """Get map for update"""

        query: models.Map = models.Map.objects.get(id=board_id) 
        return query

    async def refresh_board(self, board_id: int, board: list) -> tuple:
        """Refresh board and get list of filled field names"""

        cleared_board, field_name_list = [], []

        for column in board:
            for key in column:
                if column[key]:
                    if column[key] != "space":
                        field_name_list.append(key)
                    column[key] = ""
            cleared_board.append(column)
        
        return cleared_board, field_name_list