import json
import logging

from . import services
from .addspace import add_space
from .. import serializers


class RefreshBoardMixin:
    """Update a model instance"""

    @staticmethod
    def _clear_board(board: list) -> tuple:
        """Refresh a board and get a list of filled field names"""

        field_name_list = []

        for column in board:
            for key in column:
                if column[key]:
                    if column[key] != "space":
                        field_name_list.append(key)
                    column[key] = ""

        return field_name_list
    
    async def clear_board(self, board_id: int, board: list) -> list:
        field_name_list = self._clear_board(board)
        column_dictionary = services.create_column_dict(self.column_name_list, board)
        await self.perform_refresh_board(board_id, column_dictionary)
        return field_name_list, column_dictionary
    
    async def perform_refresh_board(self, board_id: int, column_dictionary: dict) -> None:
        await services.update_board(board_id, column_dictionary)


class RefreshShipsMixin:
    """Update a model instances"""

    async def update_ships(self, board_id: int, ships: list) -> list:
        """"Refresh ships for a current board"""

        ship_from_bd = await services.get_ships(board_id)
        await self.perform_ships_updates(ship_from_bd)
        return [ship | {"plane": "horizontal", "count": count} for ship, count in zip(ships, self.ship_count_tuple)]
    
    async def perform_ships_updates(self, ships: list) -> None:
        await services.update_count_of_ships(ships, self.ship_count_tuple)


class DropShipOnBoardMixin:
    """Drop a ship on a board"""

    def drop_ship_on_board(self, ship_id: int, ship_count: int, field_name_list: list, board: list) -> None:
        for field_name in field_name_list:
            board[self.column_name_list.index(field_name[0])][field_name] = float(f"{ship_id}.{ship_count}")


class AddSpaceAroundShipMixin:
    """Add spaces around a ship"""

    def insert_space_around_ship(self, space_name, ship_plane: str, field_name_list: list, board: list) -> None:
        if ship_plane == "horizontal": 
            add_space.AddSpaceAroundShipHorizontally(space_name, field_name_list, self.column_name_list, board)
        else:
            add_space.AddSpaceAroundShipVertically(space_name, field_name_list, self.column_name_list, board)


class TakeShotMixin:
    """Update a model instance"""

    @staticmethod
    def _get_type_shot(board, field_name) -> str:
        """Get type shot on field"""

        return "hit" if type(board[field_name[0]][field_name]) == float else "miss"

    @staticmethod
    def _shot(board: dict, field_name: str, shot_type: str) -> None:
        """Make a shoot"""

        field_value = board[field_name[0]][field_name]
        board[field_name[0]][field_name] = shot_type
        return field_value
    
    @staticmethod
    def _check_if_ship_has_sunk(field_value: float, board: dict) -> bool or None:
        """Check if the ship has sunk"""

        for _, column_value in board.items():
            for _, value in column_value.items():
                if field_value == value:
                    return True
    
    @staticmethod
    def _add_misses_around_sunken_ship(field_value: float, board: dict) -> None:
        """Add misses around the sunken ship"""

        for column_name, column_value in board.items():
            for field_name, value in column_value.items():
                if f"space {field_value}" in str(value):
                    board[column_name][field_name] = "miss"

    def _confert_to_json(self, board: dict) -> None:
        """Convert board to json format"""

        for key, value in board.items():
            board[key] = json.loads(value.replace("'", '"'))

    async def take_shot(self, board_id: int, field_name: str) -> None:
        board = await services.get_board(board_id, self.column_name_list)
        self._confert_to_json(board)
        shot_type = self._get_type_shot(board, field_name)
        field_value = self._shot(board, field_name, shot_type)
        
        if type(field_value) == float and not self._check_if_ship_has_sunk(field_value, board):
            self._add_misses_around_sunken_ship(field_value, board)

        await self.perform_update_board(board_id, board)
        return board
    
    async def perform_update_board(self, board_id: int, column_dictionary: dict) -> None:
        await services.update_board(board_id, column_dictionary)


class RefreshBoardShipsMixin(RefreshBoardMixin, RefreshShipsMixin):
    "Concrete view for refresh a board model instance and ship model instances"

    async def refresh(self, board_id: int, ships: list, board: list) -> None:
        """Refresh a board model instance and ship model instances"""

        field_name_list, column_dictionary = await self.clear_board(board_id, board)
        updated_ships = await self.update_ships(board_id, ships)
        content = {
            "type": "clear_board", 
            "board": column_dictionary, 
            "field_name_list": field_name_list, 
            "ships": updated_ships
        }

        await self.send_json(content=content)


class DropShipAddSpaceMixin(DropShipOnBoardMixin, AddSpaceAroundShipMixin):
    """Concrete view for drop a ship on a board and add spaces around a ship"""

    @staticmethod
    async def get_serialized_ships(board_id: int) -> list:
        """Get ships from DB and serialize them"""

        ship_list = await services.get_ships(board_id)
        serializer = serializers.ShipSerializer(ship_list, many=True)
        return serializer.data

    async def drop_ship(
        self, ship_id: int, board_id: int, ship_plane: str, ship_count: int, field_name_list: list, board: list
    ) -> None:
        """Drop a ship on a board and add spaces around a ship"""

        self.drop_ship_on_board(ship_id, ship_count, field_name_list, board)
        self.insert_space_around_ship(f" space {ship_id}.{ship_count}", ship_plane, field_name_list, board)
        column_dictionary = services.create_column_dict(self.column_name_list, board)
        await self.perform_update_board(board_id, column_dictionary)
        await self.perform_ship_updates(ship_id, ship_count)
        ship_list = await self.get_serialized_ships(board_id)

        await self.send_json(content={"type": "drop_ship", "board": column_dictionary, "ships": ship_list})
    
    async def perform_update_board(self, board_id: int, column_dictionary: dict) -> None:
        await services.update_board(board_id, column_dictionary)
    
    async def perform_ship_updates(self, ship_id: int, ship_count: int) -> None:
        await services.update_count_of_ship(ship_id, ship_count)
