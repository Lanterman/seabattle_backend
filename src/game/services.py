column_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def clear_enemy_board(user, boards) -> tuple:
    """Сlears the enemy table from ships and the space around them"""

    index, enemy_board = (1, boards[1]) if boards[0]["user_id"] == user.id else (0, boards[0])

    for key, value in enemy_board.items():
        if key in column_name_list:
            for column_name, column_value in value.items():
                if column_value not in ("", "hit", "miss"):
                    enemy_board[key][column_name] = ""

    return index, enemy_board
