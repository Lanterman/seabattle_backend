class Base:
    """Base class for extensios"""

    def add_space_to_first_field(self, first_elem, column_name_list, board):
        """Add space above a ship"""

        if int(first_elem[1:]) > 1:
            board[column_name_list.index(first_elem[0])][f"{first_elem[0]}{int(first_elem[1:]) - 1}"] = "space"

    def add_space_to_last_field(self, last_elem, column_name_list, board):
        """Add space under a ship"""

        if int(last_elem[1:]) < 10:
            board[column_name_list.index(last_elem[0])][f"{last_elem[0]}{int(last_elem[1:]) + 1}"] = "space"


class AddSpaceAroundShipHorizontally(Base):
    """Add space for a horizontal ship"""

    def __init__(self, field_name_list, column_name_list, board) -> None:
        self.insert_space_around_ship(field_name_list, column_name_list, board)

    def add_space_at_top(self, field_name_list, column_name_list, board):
        """Add space at top"""

        top_string_number = int(field_name_list[0][1:]) - 1
        
        if top_string_number >= 1:
            for field_name in field_name_list:
                board[column_name_list.index(field_name[0])][f"{field_name[0]}{top_string_number}"] = "space"
    
    def add_space_to_right(self, field_name_list, column_name_list, board):
        """Add space to right"""

        right_column_index = column_name_list.index(field_name_list[-1][0]) + 1
        
        if right_column_index <= 9:
            elem = f"{column_name_list[right_column_index]}{field_name_list[0][1:]}"

            self.add_space_to_first_field(elem, column_name_list, board)
            self.add_space_to_last_field(f"{elem[0]}{int(elem[1:]) - 1}", column_name_list, board)
            self.add_space_to_last_field(elem, column_name_list, board)
    
    def add_space_at_bottom(self, field_name_list, column_name_list, board):
        """Add space at bottom"""

        bottom_string_number = int(field_name_list[0][1:]) + 1

        if bottom_string_number <= 10:
            for field_name in field_name_list:
                board[column_name_list.index(field_name[0])][f"{field_name[0]}{bottom_string_number}"] = "space"

    def add_space_to_left(self, first_elem, column_name_list, board):
        """Add space to left"""

        left_column_index = column_name_list.index(first_elem[0]) - 1

        if int(left_column_index) >= 0:
            elem = f"{column_name_list[left_column_index]}{first_elem[1:]}"

            self.add_space_to_first_field(elem, column_name_list, board)
            self.add_space_to_last_field(f"{elem[0]}{int(elem[1:]) - 1}", column_name_list, board)
            self.add_space_to_last_field(elem, column_name_list, board)

    def insert_space_around_ship(self, field_name_list, column_name_list, board):
        """Add space around horizontal ship"""

        field_name_list.sort()
        self.add_space_at_top(field_name_list, column_name_list, board)
        self.add_space_to_right(field_name_list, column_name_list, board)
        self.add_space_at_bottom(field_name_list, column_name_list, board)
        self.add_space_to_left(field_name_list[0], column_name_list, board)


class AddSpaceAroundShipVertically(Base):
    """Add space for a vertical ship"""

    def __init__(self, field_name_list, column_name_list, board) -> None:
        self.insert_space_around_ship(field_name_list, column_name_list, board)
    
    def add_space_at_top(self, firstElem, column_name_list, board):
        """Add space at top"""

        self.add_space_to_first_field(firstElem, column_name_list, board)
    
    def add_space_to_right(self, field_name_list, column_name_list, board):
        """Add space to right"""

        right_column_index = column_name_list.index(field_name_list[0][0]) + 1
        
        if right_column_index < 10:
            column_name = column_name_list[right_column_index]

            for field_name in field_name_list:
                board[right_column_index][f"{column_name}{field_name[1:]}"] = "space"

            self.add_space_to_first_field(f"{column_name}{field_name_list[0][1:]}", column_name_list, board)
            self.add_space_to_last_field(f"{column_name}{field_name_list[-1][1:]}", column_name_list, board)
    
    def add_space_at_bottom(self, last_elem, column_name_list, board):
        """Add space at bottom"""

        self.add_space_to_last_field(last_elem, column_name_list, board)

    def add_space_to_left(self, field_name_list, column_name_list, board):
        """Add space to left"""

        left_column_index = column_name_list.index(field_name_list[0][0]) - 1

        if int(left_column_index) >= 0:
            elem = column_name_list[left_column_index]

            for field_name in field_name_list:
                board[left_column_index][f"{elem}{field_name[1:]}"] = "space"

            self.add_space_to_first_field(f"{elem}{field_name_list[0][1:]}", column_name_list, board)
            self.add_space_to_last_field(f"{elem}{field_name_list[-1][1:]}", column_name_list, board)
    
    def insert_space_around_ship(self, field_name_list, column_name_list, board):
        """Add space around vertical ship"""

        field_name_list.sort(key=lambda x: int(x[1:]))
        self.add_space_at_top(field_name_list[0], column_name_list, board)
        self.add_space_to_right(field_name_list, column_name_list, board)
        self.add_space_at_bottom(field_name_list[-1], column_name_list, board)
        self.add_space_to_left(field_name_list, column_name_list, board)
