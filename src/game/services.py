column_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def clear_enemy_board(request, boards) -> tuple:
    """Сlears the enemy table from ships and the space around them"""

    index, enemy_board = (1, boards[1]) if boards[0]["user_id"] == request.user.id else (0, boards[0])

    for column_name in column_name_list:
        column = eval(enemy_board[column_name])
        for elem in column:
            if column[elem] not in ("", "hit", "miss"):
                column[elem] = ""
        enemy_board[column_name] = str(column)

    return index, enemy_board