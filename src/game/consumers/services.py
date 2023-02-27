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
