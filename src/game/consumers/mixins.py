import logging

from .addspace import add_space


class RefreshBoardMixin:
    """Refresh board and get list of filled field names"""

    def refresh_board(self, board: list) -> tuple:
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

    def drop_ship_on_board(
        self, field_name_list: list, ship_name:str, column_name_list: list, board: list
    ) -> list:
        """Put ship on board"""

        for field_name in field_name_list:
            board[column_name_list.index(field_name[0])][field_name] = ship_name

        return board


class AddSpaceAroundShipMixin:
    """Add space around ship"""

    def insert_space_around_ship(
        self, plane: str, field_name_list: list, column_name_list: list, board: list
    ) -> None:
        """Add space around ship"""

        if plane == "horizontal": 
            add_space.AddSpaceAroundShipHorizontally(field_name_list, column_name_list, board)
        else:
            add_space.AddSpaceAroundShipVertically(field_name_list, column_name_list, board)


class DropShipAddSpaceMixin(DropShipOnBoardMixin, AddSpaceAroundShipMixin):
    """Drop ship on board and add space around ship"""

    pass
