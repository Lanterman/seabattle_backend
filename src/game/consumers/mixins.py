class RefreshBoardMixin:

    async def refresh_board(self, board: list) -> tuple:
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


class DropShipOnBoardMixin:
    """Drop ship on board"""

    async def put_ship_on_board(self, field_name_list: list, ship_name:str, column_name_list: list, board: list):
        """Put ship on board"""

        for field_name in field_name_list:
            board[column_name_list.index(field_name[0])][field_name] = ship_name

        return board


class DropShipAddSpaceMixin(DropShipOnBoardMixin):
    """Drop ship on board and add space around ship"""

    pass