column_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
ship_count_dict = {
    "fourdeck": 1,
    "tripledeck": 2,
    "singledeck": 4,
    "doubledeck": 3    
}


def clear_enemy_board(user, boards) -> tuple:
    """Сlears the enemy table from ships and the space around them"""

    if boards[0]["user_id"]:
        if boards[0]["user_id"] == user.id:
            index, enemy_board = (1, boards[1])
        else:
            index, enemy_board = (0, boards[0])
    else:
        if boards[1]["user_id"] == user.id:
            index, enemy_board = (0, boards[0])
        else:
            index, enemy_board = (1, boards[1])

    for key, value in enemy_board.items():
        if key in column_name_list:
            for column_name, column_value in value.items():
                if column_value not in ("", "hit", "miss"):
                    enemy_board[key][column_name] = ""

    return index, enemy_board
