class Base:
    """Base class for extensios"""

    def add_space_to_first_field(self, space_name: str, first_elem: str, board: dict) -> None:
        """Add space above a ship"""

        if int(first_elem[1:]) > 1:
            board[first_elem[0]][f"{first_elem[0]}{int(first_elem[1:]) - 1}"] += space_name

    def add_space_to_last_field(self, space_name: str, last_elem: str, board: dict) -> None:
        """Add space under a ship"""

        if int(last_elem[1:]) < 10:
            board[last_elem[0]][f"{last_elem[0]}{int(last_elem[1:]) + 1}"] += space_name


class AddSpaceAroundShipHorizontally(Base):
    """Add space for a horizontal ship"""

    def __init__(self, space_name: str, field_name_list: list, column_name_list: list, board: dict) -> None:
        self.insert_space_around_ship(space_name, field_name_list, column_name_list, board)

    def add_space_at_top(self, space_name: str, field_name_list: list, board: dict) -> None:
        """Add space at top"""

        top_string_number = int(field_name_list[0][1:]) - 1
        
        if top_string_number >= 1:
            for field_name in field_name_list:
                board[field_name[0]][f"{field_name[0]}{top_string_number}"] += space_name
    
    def add_space_to_right(self, space_name: str, field_name_list: list, column_name_list: list, board: dict) -> None:
        """Add space to right"""

        right_column_index = column_name_list.index(field_name_list[-1][0]) + 1
        
        if right_column_index <= 9:
            field_name = f"{column_name_list[right_column_index]}{field_name_list[0][1:]}"

            self.add_space_to_first_field(space_name, field_name, board)
            self.add_space_to_last_field(space_name, f"{field_name[0]}{int(field_name[1:]) - 1}", board)
            self.add_space_to_last_field(space_name, field_name, board)
    
    def add_space_at_bottom(self, space_name: str, field_name_list: list, board: dict) -> None:
        """Add space at bottom"""

        bottom_string_number = int(field_name_list[0][1:]) + 1

        if bottom_string_number <= 10:
            for field_name in field_name_list:
                board[field_name[0]][f"{field_name[0]}{bottom_string_number}"] += space_name

    def add_space_to_left(self, space_name: str, first_elem: str, column_name_list: list, board: dict) -> None:
        """Add space to left"""

        left_column_index = column_name_list.index(first_elem[0]) - 1

        if int(left_column_index) >= 0:
            field_name = f"{column_name_list[left_column_index]}{first_elem[1:]}"

            self.add_space_to_first_field(space_name, field_name, board)
            self.add_space_to_last_field(space_name, f"{field_name[0]}{int(field_name[1:]) - 1}", board)
            self.add_space_to_last_field(space_name, field_name, board)

    def insert_space_around_ship(
            self, space_name: str, field_name_list: list, column_name_list: list, board: dict
    ) -> None:
        """Add space around horizontal ship"""

        field_name_list.sort()
        self.add_space_at_top(space_name, field_name_list, board)
        self.add_space_to_right(space_name, field_name_list, column_name_list, board)
        self.add_space_at_bottom(space_name, field_name_list, board)
        self.add_space_to_left(space_name, field_name_list[0], column_name_list, board)


class AddSpaceAroundShipVertically(Base):
    """Add space for a vertical ship"""

    def __init__(self, space_name: str, field_name_list: list, column_name_list: list, board: dict) -> None:
        self.insert_space_around_ship(space_name, field_name_list, column_name_list, board)
    
    def add_space_at_top(self, space_name: str, first_elem: str, board: dict) -> None:
        """Add space at top"""

        self.add_space_to_first_field(space_name, first_elem, board)
    
    def add_space_to_right(self, space_name: str, field_name_list: list, column_name_list: list, board: dict) -> None:
        """Add space to right"""

        right_column_index = column_name_list.index(field_name_list[0][0]) + 1

        if right_column_index < 10:
            column_name = column_name_list[right_column_index]

            for field_name in field_name_list:
                board[column_name][f"{column_name}{field_name[1:]}"] += space_name

            self.add_space_to_first_field(space_name, f"{column_name}{field_name_list[0][1:]}", board)
            self.add_space_to_last_field(space_name, f"{column_name}{field_name_list[-1][1:]}", board)
    
    def add_space_at_bottom(self, space_name: str, last_elem: str, board: dict) -> None:
        """Add space at bottom"""

        self.add_space_to_last_field(space_name, last_elem, board)

    def add_space_to_left(self, space_name: str, field_name_list: list, column_name_list: list, board: dict) -> None:
        """Add space to left"""

        left_column_index = column_name_list.index(field_name_list[0][0]) - 1

        if int(left_column_index) >= 0:
            column_name = column_name_list[left_column_index]

            for field_name in field_name_list:
                board[column_name][f"{column_name}{field_name[1:]}"] += space_name

            self.add_space_to_first_field(space_name, f"{column_name}{field_name_list[0][1:]}", board)
            self.add_space_to_last_field(space_name, f"{column_name}{field_name_list[-1][1:]}", board)
    
    def insert_space_around_ship(
            self, space_name: str, field_name_list: list, column_name_list: list, board: dict
    ) -> None:
        """Add space around vertical ship"""

        field_name_list.sort(key=lambda x: int(x[1:]))
        self.add_space_at_top(space_name, field_name_list[0], board)
        self.add_space_to_right(space_name, field_name_list, column_name_list, board)
        self.add_space_at_bottom(space_name, field_name_list[-1], board)
        self.add_space_to_left(space_name, field_name_list, column_name_list, board)
