import logging
import json


def confert_to_json(board: dict) -> None:
    """Convert board to json format"""

    for key, value in board.items():
        board[key] = json.loads(value.replace("'", '"'))


def clear_board(board_columns: dict) -> dict:
    """Clear board"""

    for column_name, column_value in board_columns.items():
        for field_name, field_value in column_value.items():
            if field_value:
                board_columns[column_name][field_name] = ""


def determine_number_of_enemy_ships(board: dict) -> int:
        """Determine number of living enemy ships"""

        enemy_ships_list = []

        for _, column_value in board.items():
            for _, value in column_value.items():
                if value not in enemy_ships_list and type(value) == float:
                    enemy_ships_list.append(value)
        
        return len(enemy_ships_list)


def determine_winner_and_loser(winner: str, users) -> tuple:
    """Determine winner and loser users"""

    if users[0].username == winner:
        return users
    else :
        return users[1], users[0]
