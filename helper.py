def calculate_piece_coordinate(row: int, col: int) -> tuple:
    """
    A helper function to return the coordinates for the center of some square on the canvas
    :param row:
    :param col:
    :return coords:
    """
    x0 = (row * 64) + 32
    y0 = ((7 - col) * 64) + 32
    return x0, y0


def get_color(numcol: str) -> str:
    """
    Simply converts the number code of a color to its string equivalent
    :param numcol:
    :return:
    """
    return 'White' if numcol == '2' else 'Black'


def check_for_kings(board: list) -> str:
    """
    This checks for the pressence of a king on the board, returning the king not on the board
    :param board:
    :return:
    """
    king1_check = []
    king2_check = []
    for row in board:
        king1_check.append(False if 'K1' not in row else True)
        king2_check.append(False if 'K2' not in row else True)
    if not any(king2_check):
        return 'W'
    if not any(king1_check):
        return 'B'

def get_clicked_row_column(event) -> tuple:
    """
    This is used to check the coords of a given click
    :param event:
    :return:
    """
    col_size = row_size = 64
    clicked_column = event.x // col_size
    clicked_row = 7 - (event.y // row_size)
    return clicked_row, clicked_column


def get_x_y_coordinate(row, col):
    """
    This gives x, y of a given piece
    :param row:
    :param col:
    :return:
    """
    x = (col * 64)
    y = ((7 - row) * 64)
    return x, y
