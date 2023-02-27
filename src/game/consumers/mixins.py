import logging
import random
from . import services, db_queries
from .addspace import add_space
from .. import serializers


class RefreshBoardMixin:
    """Update a model instance"""

    @staticmethod
    def _clear_board(board: dict) -> tuple:
        """Refresh a board and get a list of filled field names"""

        field_name_list = []

        for column in board.values():
            for key in column:
                if column[key]:
                    if column[key] != "space":
                        field_name_list.append(key)
                    column[key] = ""

        return field_name_list
    
    async def clear_board(self, board_id: int, board: dict) -> list:
        field_name_list = self._clear_board(board)
        await self.perform_refresh_board(board_id, board)
        return field_name_list
    
    async def perform_refresh_board(self, board_id: int, board: dict) -> None:
        await db_queries.update_board(board_id, board)


class RefreshShipsMixin:
    """Update a model instances"""

    async def update_ships(self, board_id: int, ships: list) -> list:
        """"Refresh ships for a current board"""

        ship_from_bd = await db_queries.get_ships(board_id)
        await self.perform_ships_updates(ship_from_bd)
        return [ship | {"plane": "horizontal", "count": count} for ship, count in zip(ships, self.ship_count_tuple)]
    
    async def perform_ships_updates(self, ships: list) -> None:
        await db_queries.update_count_of_ships(ships, self.ship_count_tuple)


class DropShipOnBoardMixin:
    """Drop a ship on a board"""

    @staticmethod
    def drop_ship_on_board(ship_id: int, ship_count: int, field_name_list: list, board: dict) -> None:
        for field_name in field_name_list:
            board[field_name[0]][field_name] = float(f"{ship_id}.{ship_count}")


class AddSpaceAroundShipMixin:
    """Add spaces around a ship"""

    def insert_space_around_ship(self, space_name, ship_plane: str, field_name_list: list, board: dict) -> None:
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
    def _is_ship_has_sunk(field_value: float, board: dict) -> bool or None:
        """Check if the ship has sunk"""

        for _, column_value in board.items():
            for _, value in column_value.items():
                if field_value == value:
                    return False
        return True
    
    @staticmethod
    def _add_misses_around_sunken_ship(field_value: float, board: dict) -> None:
        """Add misses around the sunken ship"""

        for column_name, column_value in board.items():
            for field_name, value in column_value.items():
                if f"space {field_value}" in str(value):
                    board[column_name][field_name] = "miss"

    async def take_shot(self, board_id: int, field_name: str) -> None:
        board = await db_queries.get_board(board_id, self.column_name_list)
        services.confert_to_json(board)
        shot_type = self._get_type_shot(board, field_name)
        field_value = self._shot(board, field_name, shot_type)
        if type(field_value) == float and self._is_ship_has_sunk(field_value, board):
            self._add_misses_around_sunken_ship(field_value, board)

        await self.perform_update_board(board_id, board)
        return board
    
    async def perform_update_board(self, board_id: int, column_dictionary: dict) -> None:
        await db_queries.update_board(board_id, column_dictionary)


class IsReadyToPlayMixin:
    """Update a model instance"""

    async def ready_to_play(self, board_id: int, is_ready: bool) -> None:
        """Change ready to play field"""
        
        await db_queries.update_board_is_ready(board_id, is_ready)
        return is_ready


class ClearCountOfShipsMixin:
    """Update ship models instances"""

    @staticmethod
    def _clear_count_of_ships(ships: list) -> None:
        """Cleat count field of ships"""

        for ship in ships:
            ship["count"] = 0
    
    async def perform_clear_count_of_ships(self, board_id: int) -> None:
        await db_queries.clear_count_of_ships(board_id)


class RandomPlacementMixin(AddSpaceAroundShipMixin):
    """Update a board model instance"""

    @staticmethod
    def _is_put_on_board(field_list: list, board: dict) -> bool:
        """Check if a ship can be put on a board"""

        for field_name in field_list:
            if board[field_name[0]][field_name]:
                return False

        return True
    
    @staticmethod
    def _put_ship_on_board(ship_id: int, ship_number: int, field_list: list, board: dict) -> None:
        """Put a ship on a board"""

        for field_name in field_list:
            board[field_name[0]][field_name] = float(f"{ship_id}.{ship_number}")


    @staticmethod
    def get_field_list_horizontally(
        random_number: int, random_column_name: str, ship_size: int, column_name_list: list
    ) -> list:
        """Get list of field horizontally"""

        index = column_name_list.index(random_column_name)

        if index + ship_size <= 9:
            field_list = [f"{column_name_list[index + number]}{random_number}" for number in range(ship_size)]
        else: 
            field_list = [f"{column_name_list[index - number]}{random_number}" for number in range(ship_size)]
        
        return field_list
    
    @staticmethod
    def get_field_list_vertically(random_number: int, random_column_name: str, ship_size: int) -> list:
        """Get list of fields vertically"""

        if random_number + ship_size <= 10:
            field_list = [f"{random_column_name}{random_number + number}" for number in range(ship_size)]
        else: 
            field_list = [f"{random_column_name}{random_number - number}" for number in range(ship_size)]
        
        return field_list

    def get_field_list(self, plane: str, ship_size: int, board: dict) -> list:
        """Get a list of fields where a ship will a located"""

        is_put = False

        while not is_put:
            random_number = random.choice(self.string_number_list)
            random_column_name = random.choice(self.column_name_list)

            if plane == "vertical":
                field_list = self.get_field_list_vertically(random_number, random_column_name, ship_size)
            else:
                field_list = self.get_field_list_horizontally(
                    random_number, random_column_name, ship_size, self.column_name_list
                )

            if self._is_put_on_board(field_list, board):
                is_put = True
        
        return field_list

    async def random_placement(self, board: dict, ships: list) -> dict:
        """Random ships placement on a board"""

        services.clear_board(board)
        
        for ship, count in zip(ships, self.ship_count_tuple):
            for ship_number in range(1, count + 1):
                plane = random.choice(("horizontal", "vertical"))
                field_list = self.get_field_list(plane, ship["size"], board)
                self._put_ship_on_board(ship["id"], ship_number, field_list, board)
                self.insert_space_around_ship(f" space {ship['id']}.{ship_number}", plane, field_list, board)

        return board
    
    async def perform_update_board(self, board_id: int, column_dictionary: dict) -> None:
        await db_queries.update_board(board_id, column_dictionary)


class RandomPlacementClearShipsMixin(RandomPlacementMixin, ClearCountOfShipsMixin):
    """
    Concrete view for random placement ships on a board model instance and update ship model instances count field
    """

    async def random_placement_and_clear_ships(self, board_id: int, board: dict, ships: list) -> None:
        """Random placement ships on a board and update ships count field"""

        placed_board = await self.random_placement(board, ships)
        self._clear_count_of_ships(ships)

        await self.perform_update_board(board_id, placed_board)
        await self.perform_clear_count_of_ships(board_id)

        await self.send_json(content={"type": "random_replaced", "ships": ships, "board": placed_board})


class RefreshBoardShipsMixin(RefreshBoardMixin, RefreshShipsMixin):
    """Concrete view for refresh a board model instance and ship model instances"""

    async def refresh(self, board_id: int, ships: list, board: dict) -> None:
        """Refresh a board model instance and ship model instances"""

        field_name_list = await self.clear_board(board_id, board)
        updated_ships = await self.update_ships(board_id, ships)
        content = {
            "type": "clear_board", 
            "board": board, 
            "field_name_list": field_name_list, 
            "ships": updated_ships
        }

        await self.send_json(content=content)


class DropShipAddSpaceMixin(DropShipOnBoardMixin, AddSpaceAroundShipMixin):
    """Concrete view for drop a ship on a board and add spaces around a ship"""

    @staticmethod
    async def get_serialized_ships(board_id: int) -> list:
        """Get ships from DB and serialize them"""

        ship_list = await db_queries.get_ships(board_id)
        serializer = serializers.ShipSerializer(ship_list, many=True)
        return serializer.data

    async def drop_ship(
        self, ship_id: int, board_id: int, ship_plane: str, ship_count: int, field_name_list: list, board: dict
    ) -> None:
        """Drop a ship on a board and add spaces around a ship"""

        self.drop_ship_on_board(ship_id, ship_count, field_name_list, board)
        self.insert_space_around_ship(f" space {ship_id}.{ship_count}", ship_plane, field_name_list, board)

        await self.perform_update_board(board_id, board)
        await self.perform_ship_updates(ship_id, ship_count)
        ship_list = await self.get_serialized_ships(board_id)

        await self.send_json(content={"type": "drop_ship", "board": board, "ships": ship_list})
    
    async def perform_update_board(self, board_id: int, board: dict) -> None:
        await db_queries.update_board(board_id, board)
    
    async def perform_ship_updates(self, ship_id: int, ship_count: int) -> None:
        await db_queries.update_count_of_ship(ship_id, ship_count)
