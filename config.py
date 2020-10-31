#This is the config file for the game

"""
A few pre - coded color options for the board - latter color is 'white' and first is 'black'
This could be dropped into a single list if only 1 option was wanted
"""
BOARD_COLORS = [
    ['#666', '#fff'],
    ['#550', '#ffc'],
    ['#a00', '#ffc']
]

"""
This activates the option to play as emoji - it was added at 11pm when i thought this would be funny
"""
EMOJI = False

"""
These are the AI weightings for the minimax algorithm - and are adjustable.
"""
KING_WEIGHT = 200
QUEEN_WEIGHT = 9
ROOK_WEIGHT = 5
BISHOP_WEIGHT = 3 #Bishop and knight have equal weightings
PAWN_WEIGHT = 1


PAWN_EVAL_WEIGHT = 0.5


MOBILITY_WEIGHT = 0.1


