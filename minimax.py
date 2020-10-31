"""
This is the file which will process a given board and return a 'ideal' move based on
the depth provided and some board. There are 2 main parts to minimax, the algorithm itself,
and more importantly - evaluation. The evaluation I will use is quite simply a piece square table,
which will give some value to a piece based on its position on the board. I will also use a hashtable
this will improve performance - but clearly I cant hash and precalculate *all* of the values (10^43),
and as such I will calculate the first few thousand first, and then add based on moves as they are calculated.

NOTE: AI player is hardcoded to white
"""

# This will be used to store the hashtable
import pickle
# This is used to get possible moves
from validation import possible_move
# For the weightings
from config import *
# To make copies of the list with different pointers, could've been done with [*list] but this is a little more readable
from copy import deepcopy
# Used for the testing function - and timing
import time

# The original hashtable - incase one cant be un-pickled
hashtable = {}

# A counter for counting paths evaluated - has to be global
counter = 0

def start_game() -> dict:
    """Loads the hashtable
    :return Dict: """
    try:
        with open('minimax_hashtable.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}


def end_game(hash_table: dict) -> None:
    """
    Saves the hashtable
    :param hash_table:
    :return None:
    """
    with open('minimax_hashtable.pkl', 'wb') as file:
        pickle.dump(hash_table, file)


def check_terminal_node(board: list) -> bool:
    """
    If there is a king on the board then its not a terminal node - so it returns 0
    Could be a better idea to also check for possible moves
    :param board: 
    :return bool: 
    """
    return False if 'K' in str(board) else True


def all_possible_moves(board: list, color: str) -> dict:
    """
    This is a function to return all possible moves for a given color in a given board
    :param board:
    :param color:
    :return dict of possible moves:
    """
    possible_moves = {}
    for x, row in enumerate(board):
        for y, piece in enumerate(row):
            if piece[1] == color:
                possible_moves[(x, y)] = possible_move(y, x, piece.lower(), board)
    return possible_moves


def all_possible_move_count(board: list, color: str) -> int:
    """
    This return the number of possible moves for a given color - used in the 'mobility' score
    :param board:
    :param color:
    :return int of possible moves:
    """
    count = 0
    for x, row in enumerate(board):
        for y, piece in enumerate(row):
            if piece[1] == color:
                moves = possible_move(x, y, piece, board)
                if moves:
                    count += len(moves)
    return count


def get_mobility_score(board):
    """
    A mobility score used for eval - essentially a count of all possible moves for a given colour
    :param board: 
    :return mobility score: 
    """
    return MOBILITY_WEIGHT*(all_possible_move_count(board, '2') - all_possible_move_count(board, '1'))


def get_piece_count(board: list, piece: str) -> int:
    """
    simply takes a board and returns the number of any piece
    :param board: 
    :param piece: 
    :return int: 
    """
    return str(board).count(piece)


def material_eval(board: list) -> int:
    """
    Takes a board abd return the eval of material - player 1 is the AI
    :param board:
    :return material score:
    """
    piece_counts = [get_piece_count(board, piece) for piece in
                    ('K1', 'K2', 'Q1', 'Q2', 'R1', 'R2', 'B1', 'B2', 'N1', 'N2', 'P1', 'P2')]
    king1, king2, queen1, queen2, rook1, rook2, bishop1, bishop2, knight1, knight2, pawn1, pawn2 = piece_counts
    return KING_WEIGHT*(king2 - king1) + QUEEN_WEIGHT*(queen2 - queen1) + ROOK_WEIGHT*(rook2 - rook1) + \
        BISHOP_WEIGHT*(bishop2 - bishop1 + knight2 - knight1) + PAWN_WEIGHT*(pawn2 - pawn1)


# These ended up unused - might be used in a future revision i suppose
'''def pawn_blocked(board: list) -> int:
    """
    A blocked pawn is one that cannot move - this doesnt *exactly* do that - but itll be fine for minimax
    :param board:
    :return:
    """
    pawn_count = 0
    for y, row in enumerate(board):
        for x, piece in enumerate(row):
            if piece[0] == 'P':
                if board[y-1][x][0] == 'P' or board[y-1][x][0] == 'P':
                    pawn_count += 1
    return pawn_count'''


'''def pawn_isolated(board: list, color: str) -> int:
    """
    This gives a count of isolated pawns
    :param board:
    :param color:
    :return:
    """
    pawn_count = 0
    pawn_string = f"P{color}"
    for y, row in enumerate(board):
        for x, piece in enumerate(row):
            if piece == pawn_string:
                resultxpro, resultxneg, resultypro, resultyneg = x+1, x-1, y+1, y-1
                eval_expression = 'board[y + 1][x] != pawn_string and board[y - 1][x] != pawn_string ' \
                                  'and board[y][x + 1] != pawn_string and board[y][x - 1] != pawn_string ' \
                                  'and board[y - 1][x - 1] != pawn_string and board[y + 1][x - 1] != pawn_string ' \
                                  'and board[y - 1][x + 1] != pawn_string and board[y - 1][x + 1] != pawn_string'
                if resultxpro == 8:
                    eval_expression.replace('board[y][x + 1] != pawn_string', 'False')
                    eval_expression.replace('board[y - 1][x + 1] != pawn_string', 'False')
                    eval_expression.replace('board[y + 1][x + 1] != pawn_string', 'False')
                if resultxneg == -1:
                    eval_expression.replace('board[y][x - 1] != pawn_string', 'False')
                    eval_expression.replace('board[y - 1][x - 1] != pawn_string', 'False')
                    eval_expression.replace('board[y + 1][x - 1] != pawn_string', 'False')
                if resultypro == 8:
                    print('edge')
                    eval_expression.replace('board[y + 1][x] != pawn_string ', 'False')
                    eval_expression.replace('board[y + 1][x + 1] != pawn_string', 'False')
                    eval_expression.replace('board[y + 1][x - 1] != pawn_string', 'False')
                if resultyneg == -1:
                    eval_expression.replace('board[y - 1][x] != pawn_string ', 'False')
                    eval_expression.replace('board[y - 1][x + 1] != pawn_string', 'False')
                    eval_expression.replace('board[y - 1][x - 1] != pawn_string', 'False')
                print(eval_expression)
                if not (eval(eval_expression)):

                    pawn_count += 1
    return pawn_count'''


'''def pawn_doubled(board: list, color: str) -> int:
    pawn_count = 0
    pawn_string = f"P{color}"
    for y, row in enumerate(board):
        for x, piece in enumerate(row):
            if piece == pawn_string:
                if not (board[y + 1][x] != pawn_string and board[y - 1][x] != pawn_string):
                    pawn_count += 1
    return pawn_count'''


'''def pawn_eval(board: list) -> int:
    blocked = pawn_blocked(board)
    #isolated1 = pawn_isolated(board, '1')
    #isolated2 = pawn_isolated(board, '2')
    doubled1 = pawn_doubled(board, '1')
    doubled2 = pawn_doubled(board, '2')
    return PAWN_EVAL_WEIGHT * (doubled1 - doubled2 + 2*blocked) # + isolated1 - isolated2)'''


# Back to functions that *are* needed
def evaluate_board(board: list) -> int:
    """
    Evalutes some board based on both its material and mobility
    :param board:
    :return evaluated board:
    """
    global hashtable
    if hashtable.get(hash(str(board))):
        return hashtable[hash(str(board))]
    eval = material_eval(board) + get_mobility_score(board)
    hashtable[hash(str(board))] = eval
    return eval


def minimax_ab(depth: int, board: list, alpha: int, beta: int, maximising_player: bool) -> tuple:
    """
    A minimax with alpha beta pruning - works great and sees a decrease of up to 20 times less paths evaluated compared
    to without the alpha beta. It is a shockingly simple change - adding only a few lines of code.
    :param depth:
    :param board:
    :param alpha:
    :param beta:
    :param maximising_player:
    :return heuristic, original square, destination square :
    """
    global counter
    if depth == 0 or check_terminal_node(board):
        counter = counter + 1
        return evaluate_board(board), 0, 0
    if maximising_player:
        value = -999999999
        possible_moves = all_possible_moves(board, '2')
        for playable_piece in possible_moves.keys():
            for playable_move in (possible_moves[playable_piece] if possible_moves[playable_piece] else []):
                new_board = deepcopy(board)
                new_board[playable_move[1]][playable_move[0]] = new_board[playable_piece[0]][playable_piece[1]]
                new_board[playable_piece[0]][playable_piece[1]] = 'e0'
                toeval, y, x = minimax_ab(depth-1, new_board, alpha, beta, False)
                if toeval > value:
                    value = toeval
                    dest = playable_move
                    orig = playable_piece
                alpha = max([alpha, value])
                if alpha >= beta:
                    break

        return value, dest, orig
    else:
        value = 999999999
        possible_moves = all_possible_moves(board, '1')
        for playable_piece in possible_moves.keys():
            for playable_move in (possible_moves[playable_piece] if possible_moves[playable_piece] else []):
                new_board = deepcopy(board)
                new_board[playable_move[0]][playable_move[1]] = new_board[playable_piece[0]][playable_piece[1]]
                new_board[playable_piece[0]][playable_piece[1]] = 'e0'
                toeval, y, x = minimax_ab(depth-1, new_board, alpha, beta, True)
                if toeval < value:
                    value = toeval
                    dest = playable_move
                    orig = playable_piece
                beta = min([beta, value])
                if beta <= alpha:
                    break
        return value, dest, orig


def minimax(depth: int, board: list, maximising_player: bool) -> tuple:
    """
    A minimax without alpha beta pruning - and its terrible, slow and inefficient
    This should never really be run - but as i did this before the above/improved version - so might as well
    leave it as an option I suppose.
    :param depth:
    :param board:
    :param maximising_player:
    :return heuristic, original square, destination square:
    """
    global counter
    if depth == 0 or check_terminal_node(board):
        counter = counter + 1
        return evaluate_board(board), 0, 0

    if maximising_player:
        value = -999999999
        possible_moves = all_possible_moves(board, '2')
        for playable_piece in possible_moves.keys():
            for playable_move in (possible_moves[playable_piece] if possible_moves[playable_piece] else []):
                new_board = deepcopy(board)
                new_board[playable_move[1]][playable_move[0]] = new_board[playable_piece[0]][playable_piece[1]]
                new_board[playable_piece[0]][playable_piece[1]] = 'e0'
                toeval, y, x = minimax(depth-1, new_board, False)
                if toeval > value:
                    value = toeval
                    dest = playable_move
                    orig = playable_piece
        return value, dest, orig
    else:
        value = 999999999
        possible_moves = all_possible_moves(board, '1')
        for playable_piece in possible_moves.keys():
            for playable_move in (possible_moves[playable_piece] if possible_moves[playable_piece] else []):
                new_board = deepcopy(board)
                new_board[playable_move[0]][playable_move[1]] = new_board[playable_piece[0]][playable_piece[1]]
                new_board[playable_piece[0]][playable_piece[1]] = 'e0'
                toeval, y, x = minimax(depth-1, new_board, True)
                if toeval < value:
                    value = toeval
                    dest = playable_move
                    orig = playable_piece
        return value, dest, orig


def call_main_minimax(board: list, depth: int) -> tuple:
    """
    The main function called as a wrap for minimax - without AB.
    It is also used to give some data on the processing - which is printed too.
    This also loads in the hashtable from storage
    :param board:
    :param depth:
    :return heuristic, counter, time, original square, destination square:
    """
    global counter, hashtable
    start_game()
    counter = 0
    start_time = time.time()
    max_heruristic, dest, orig = minimax(depth, board, True)
    execution_time = (time.time() - start_time)
    print(f"Evaluated {counter} paths in {str(execution_time)} seconds.")
    end_game(hashtable)
    return max_heruristic, counter, execution_time, orig, dest


def call_main_ab(board: list, depth: int) -> tuple:
    """
    The main function called as a wrap for minimax with AB.
    It is also used to give some data on the processing - which is printed too.
    This also loads in the hashtable from storage
    :param board:
    :param depth:
    :return max_heruristic, counter, execution_time, orig, dest:
    """
    global counter, hashtable
    start_game()
    counter = 0
    start_time = time.time()
    max_heruristic, dest, orig = minimax_ab(depth, board, -999999999, 999999999, True)
    execution_time = (time.time() - start_time)
    print(f"Evaluated {counter} paths in {str(execution_time)} seconds.")
    end_game(hashtable)
    return max_heruristic, counter, execution_time, orig, dest


def graph_time_for_execute(max_depth: int, type: str) -> None:
    """
    This is used to graph the execution time - it was mostly used in the testing of the program.
    :param max_depth:
    :param type:
    :return:
    """
    from matplotlib import pyplot as plt
    board_to_test = [
        ['R1', 'N1', 'B1', 'Q1', 'K1', 'B1', 'N1', 'R1'],
        ['P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1'],
        ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
        ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
        ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
        ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
        ['P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2'],
        ['R2', 'N2', 'B2', 'K2', 'Q2', 'B2', 'N2', 'R2']
    ]
    to_graph_time = []
    to_graph_counter = []
    for x in range(1,max_depth):
        if type == 'ab':
            _, counter, time, _, _ = call_main_minimax(board_to_test, x)
        else:
            _, counter, time, _, _ = call_main_ab(board_to_test, x)
        to_graph_time.append(time)
        to_graph_counter.append(counter)
    plt.plot(range(1,max_depth), to_graph_time)
    plt.show()
    plt.plot(range(1, max_depth), to_graph_counter)
    plt.show()
