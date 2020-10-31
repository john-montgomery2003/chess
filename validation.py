#This is the file which us used to verify and validate moves


def king_moves(x, y, color, board):
    """
    Takes the position, color and board and returns a list of the possible moves a king could make from said position.
    :param x:
    :param y:
    :param color:
    :param board:
    :return:
    """
    possible_moves = []
    if x + 1 <= 7:
        if board[y][x + 1][1] != color:
            possible_moves.append([x + 1, y])
    if x - 1 >= 0:
        if board[y][x - 1][1] != color:
            possible_moves.append([x - 1, y])
    if y + 1 <= 7:
        if board[y + 1][x][1] != color:
            possible_moves.append([x, y + 1])
    if y - 1 >= 0:
        if board[y - 1][x][1] != color:
            possible_moves.append([x, y - 1])
    if x + 1 <= 7 and y + 1 <= 7:
        if board[y + 1][x + 1][1] != color:
            possible_moves.append([x + 1, y + 1])
    if x + 1 <= 7 and y - 1 >= 0:
        if board[y - 1][x + 1][1] != color:
            possible_moves.append([x + 1, y - 1])
    if x - 1 >= 0 and y - 1 >= 0:
        if board[y - 1][x - 1][1] != color:
            possible_moves.append([x - 1, y - 1])
    if x - 1 >= 0 and y + 1 <= 7:
        if board[y + 1][x - 1][1] != color:
            possible_moves.append([x - 1, y + 1])
    return possible_moves


def queen_moves(x, y, color, board):
    """
    This is a function for getting the possible moves of a queen, which happens to be the same as the
    rooks moves and bishops moves for the same position
    :param x:
    :param y:
    :param color:
    :param board:
    :return:
    """
    return rook_moves(x, y, color, board) + bishop_moves(x, y, color, board)


def bishop_moves(x, y, color, board):
    """
    Takes the position, color and board and returns a list of the possible moves a bishop could make from said position.
    :param x:
    :param y:
    :param color:
    :param board:
    :return:
    """
    possible_moves = []
    if x < y:
        smaller = x
    else:
        smaller = y
    for change in range(1, smaller + 1):
        if board[y - change][x - change][1] != color:
            possible_moves.append([x - change, y - change])
            if board[y - change][x - change] != 'e0':
                break
        else:
            break

    if x < (7 - y):
        smaller = x
    else:
        smaller = (7 - y)
    for change in range(1, smaller + 1):
        if board[y + change][x - change][1] != color:
            possible_moves.append([x - change, y + change])
            if board[y + change][x - change] != 'e0':
                break
        else:
            break

    if (7 - x) < y:
        smaller = (7 - x)
    else:
        smaller = y
    for change in range(1, smaller + 1):
        if board[y - change][x + change][1] != color:
            possible_moves.append([x + change, y - change])
            if board[y - change][x + change] != 'e0':
                break
        else:
            break

    if (7 - x) < (7 - y):
        smaller = (7 - x)
    else:
        smaller = (7 - y)
    for change in range(1, smaller + 1):
        if board[y + change][x + change][1] != color:
            possible_moves.append([x + change, y + change])
            if board[y + change][x + change] != 'e0':
                break
        else:
            break
    return possible_moves


def rook_moves(x, y, color, board):
    """
    Takes the position, color and board and returns a list of the possible moves a rook could make from said position.
    :param x:
    :param y:
    :param color:
    :param board:
    :return:
    """
    possible_moves = []
    for change in range(1, x + 1):
        if board[y][x - change][1] != color:
            possible_moves.append([x - change, y])
            if board[y][x - change] != 'e0':
                break
        else:
            break

    for change in range(1, (7 - x) + 1):
        if board[y][x + change][1] != color:
            possible_moves.append([x + change, y])
            if board[y][x + change] != 'e0':
                break
        else:
            break

    for change in range(1, y + 1):
        if board[y - change][x][1] != color:
            possible_moves.append([x, y - change])
            if board[y - change][x] != 'e0':
                break
        else:
            break

    for change in range(1, (7 - y) + 1):
        if board[y + change][x][1] != color:
            possible_moves.append([x, y + change])
            if board[y + change][x] != 'e0':
                break
        else:
            break
    return possible_moves


def knight_moves(x, y, color, board):
    """
    Takes the position, color and board and returns a list of the possible moves a knight could make from said position.
    :param x:
    :param y:
    :param color:
    :param board:
    :return:
    """
    possible_moves = []
    if x + 2 <= 7 and y + 1 <= 7:
        if board[y + 1][x + 2][1] != color:
            possible_moves.append([x + 2, y + 1])
    if x - 2 >= 0 and y + 1 <= 7:
        if board[y + 1][x - 2][1] != color:
            possible_moves.append([x - 2, y + 1])
    if x + 2 <= 7 and y - 1 >= 0:
        if board[y - 1][x + 2][1] != color:
            possible_moves.append([x + 2, y - 1])
    if x - 2 >= 0 and y - 1 >= 0:
        if board[y - 1][x - 2][1] != color:
            possible_moves.append([x - 2, y - 1])
    if x + 1 <= 7 and y + 2 <= 7:
        if board[y + 2][x + 1][1] != color:
            possible_moves.append([x + 1, y + 2])
    if x - 1 >= 0 and y + 2 <= 7:
        if board[y + 2][x - 1][1] != color:
            possible_moves.append([x - 1, y + 2])
    if x + 1 <= 7 and y - 2 >= 0:
        if board[y - 2][x + 1][1] != color:
            possible_moves.append([x + 1, y - 2])
    if x - 1 >= 0 and y - 2 >= 0:
        if board[y - 2][x - 1][1] != color:
            possible_moves.append([x - 1, y - 2])
    return possible_moves


def pawn_moves(x, y, color, board):
    """
    Takes the position, color and board and returns a list of the possible moves a pawn could make from said position.
    :param x:
    :param y:
    :param color:
    :param board:
    :return:
    """
    possible_moves = []
    if color == '1':
        if y + 1 <= 7:
            if board[y + 1][x] == 'e0':
                possible_moves.append([x, y + 1])
                if y == 1:
                    if board[y + 2][x] == 'e0':
                        possible_moves.append([x, y + 2])
            if x - 1 >= 0:
                if board[y + 1][x - 1][1] == '2':
                    possible_moves.append([x - 1, y + 1])
            if x + 1 <= 7:
                if board[y + 1][x + 1][1] == '2':
                    possible_moves.append([x + 1, y + 1])

    if color == '2':
        if y + 1 <= 7:
            if board[y - 1][x] == 'e0':
                possible_moves.append([x, y - 1])
                if y == 6:
                    if board[y - 2][x] == 'e0':
                        possible_moves.append([x, y - 2])
            if x - 1 >= 0:
                if board[y - 1][x - 1][1] == '1':
                    possible_moves.append([x - 1, y - 1])
            if x + 1 <= 7:
                if board[y - 1][x + 1][1] == '1':
                    possible_moves.append([x + 1, y - 1])
    return possible_moves


def possible_move(x, y, piece, board):
    """
    This is the wrapper designed to call the other functions - it is used to simplify the callings
    It takes some coords, a piece value which (consisting of both type and color).
    :param x:
    :param y:
    :param piece:
    :param board:
    :return:
    """
    if piece[0] == 'k':
        return king_moves(x, y, piece[1], board)
    elif piece[0] == 'q':
        return queen_moves(x, y, piece[1], board)
    elif piece[0] == 'b':
        return bishop_moves(x, y, piece[1], board)
    elif piece[0] == 'r':
        return rook_moves(x, y, piece[1], board)
    elif piece[0] == 'n':
        return knight_moves(x, y, piece[1], board)
    elif piece[0] == 'p':
        return pawn_moves(x, y, piece[1], board)


def check_for_check(board, color):
    """
    This is used to check if the king given by color is in check - its used to stop players moving themselves into check
    :param board:
    :param color:
    :return:
    """
    opposite_color = '1' if color == '2' else '2'
    for inx, row in enumerate(board):
        if f"K{color}" in row:
            king_coords = [row.index(f"K{color}"), inx]
    for x, row in enumerate(board):
        for y, piece in enumerate(row):
            if piece[1] == opposite_color:
                if king_coords in possible_move(y, x, piece.lower(), board):
                    return True
    return False

