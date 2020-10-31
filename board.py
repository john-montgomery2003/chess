from tkinter import Tk, Canvas, PhotoImage, messagebox
from validation import *
from random import choice
from config import *
from helper import *
from minimax import call_main_minimax, call_main_ab
from sys import argv


class Game:
    """
    This is a class for the chess game - it handles not only the GUI/tkinter side but also the board
    """
    board_color_1, board_color_2 = choice(BOARD_COLORS)
    currentBoard = [
        ['R1', 'N1', 'B1', 'Q1', 'K1', 'B1', 'N1', 'R1'],
        ['P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1'],
        ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
        ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
        ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
        ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
        ['P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2'],
        ['R2', 'N2', 'B2', 'Q2', 'K2', 'B2', 'N2', 'R2']
    ]
    highlight = None
    highlighted = []
    main_focus = ''
    images = {}
    player = '2'

    def __init__(self, parent, minimax, minimax_trash, online):
        if minimax or minimax_trash:
            self.currentBoard = [
                    ['R1', 'N1', 'B1', 'Q1', 'K1', 'B1', 'N1', 'R1'],
                    ['P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1'],
                    ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
                    ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
                    ['e0', 'e0', 'e0', 'e0', 'P2', 'e0', 'e0', 'e0'],
                    ['e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0', 'e0'],
                    ['P2', 'P2', 'P2', 'P2', 'e0', 'P2', 'P2', 'P2'],
                    ['R2', 'N2', 'B2', 'Q2', 'K2', 'B2', 'N2', 'R2']
                ]
            self.player = '1'
            depth = input("Enter Depth for MiniMax - (recommended 3) ")
            while True:
                try:
                    self.depth = int(depth)
                    break
                except ValueError:
                    depth = input("Enter Depth for MiniMax - (recommended 3) ")
        self.minimax = minimax
        self.minimax_trash = minimax_trash
        self.code = online
        self.parent = parent
        canvas_width = 8 * 64
        canvas_height = 8 * 64
        self.canvas = Canvas(
            self.parent, width=canvas_width, height=canvas_height, cursor='dot', bd=-2)
        self.canvas.pack(padx=8, pady=8)
        self.create_chess_base()
        self.canvas.bind("<Button-1>", self.on_square_clicked)

    def create_chess_base(self):
        self.draw_board()
        self.draw_all_pieces()

    def draw_single_piece(self, x, y, piece):
        piece = piece[0:2]
        piece += 'M' if (EMOJI and piece[1] == '1') else ''
        if piece != 'e0':
            filename = f"images/{piece}.png"
            if filename not in self.images:
                self.images[filename] = PhotoImage(file=filename)
            x0, y0 = calculate_piece_coordinate(x, y)
            self.canvas.create_image(x0, y0, image=self.images[filename], tags="occupied", anchor="c")

    def draw_all_pieces(self):
        for x, row in enumerate(self.currentBoard):
            for y, piece in enumerate(row):
                self.draw_single_piece(y, x, piece)

    def draw_board(self):
        current_color = self.board_color_1
        for row in range(8):
            current_color = self.get_alternate_color(current_color)
            for col in range(8):
                x1, y1 = get_x_y_coordinate(row, col)
                x2, y2 = x1 + 64, y1 + 64
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=current_color)
                current_color = self.get_alternate_color(current_color)

    def get_alternate_color(self, current_color):
        if current_color == self.board_color_2:
            next_color = self.board_color_1
        else:
            next_color = self.board_color_2
        return next_color

    def make_move(self, x1, y1, x2, y2):
        self.currentBoard[x2][y2] = self.currentBoard[y1][x1]
        self.currentBoard[y1][x1] = 'e0'
        self.canvas.delete('occupied')
        self.draw_all_pieces()
        self.canvas.delete('highlight1')
        self.canvas.delete('highlight2')
        self.canvas.delete('blocked')
        self.highlighted = []
        self.player = '2' if self.player == '1' else '1'
        check_for_king = check_for_kings(self.currentBoard)
        if check_for_king == 'W':
            messagebox.showinfo("Game Over", "Black Wins!")
            self.parent.destroy()
        if check_for_king == 'B':
            messagebox.showinfo("Game Over", "White Wins!")
            self.parent.destroy()
        if self.minimax and self.player == '2':
            _, _, _, orig, dest = call_main_ab(self.currentBoard, self.depth)
            print(orig, dest)
            self.make_move(orig[1], orig[0], dest[1], dest[0])
        elif self.minimax_trash and self.player == '2':
            _, _, _, orig, dest = call_main_minimax(self.currentBoard, self.depth)
            print(orig, dest)
            self.make_move(orig[1], orig[0], dest[1], dest[0])

    def on_square_clicked(self, event):
        clicked_row, clicked_column = get_clicked_row_column(event)
        if [clicked_column, clicked_row] in self.highlighted:
            orig_x, orig_y = self.main_focus
            self.make_move(orig_x, orig_y, clicked_row, clicked_column)
        elif - 1 < clicked_column < 8 and -1 < clicked_row < 8:
            if self.currentBoard[clicked_row][clicked_column] != 'e0' and \
                    self.currentBoard[clicked_row][clicked_column][1] == self.player:
                self.canvas.delete('highlight1')
                self.canvas.delete('highlight2')
                self.canvas.delete('blocked')
                self.highlighted = []
                x1, y1 = get_x_y_coordinate(clicked_row, clicked_column)
                x2, y2 = x1 + 64, y1 + 64
                self.canvas.create_rectangle(
                    x1 + 2, y1 + 2, x2 - 2, y2 - 2, width=5, outline='#00F', tag='highlight1')
                moves = possible_move(clicked_column, clicked_row,
                                      self.currentBoard[clicked_row][clicked_column].lower(), self.currentBoard)

                self.main_focus = [clicked_column, clicked_row]
                for square in moves:
                    y1, x1 = square
                    temp_board = list(list(row) for row in self.currentBoard)
                    temp_board[x1][y1] = temp_board[clicked_row][clicked_column]
                    temp_board[clicked_row][clicked_column] = 'e0'
                    if check_for_check(temp_board, self.player):
                        color = '#F00'
                        tag = 'blocked'
                    else:
                        color = '#0F0'
                        tag = 'highlight2'
                        self.highlighted.append(square)
                    x1, y1 = get_x_y_coordinate(x1, y1)
                    x2, y2 = x1 + 64, y1 + 64
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2, width=3, outline=color, tag=tag)


def main_1v1():
    root = Tk()
    root.title("Chess")
    Game(root, False, False, None)
    root.mainloop()


def main_minimax_trash():
    root = Tk()
    root.title("Chess")
    Game(root, False, True, None)
    root.mainloop()


def main_minimax():
    root = Tk()
    root.title("Chess")
    Game(root, True, False, None)
    root.mainloop()


if __name__ == "__main__":
    if len(argv) == 1:
        main_1v1()
    else:
        if argv[1] == 'minimax':
            main_minimax()
        else:
            main_minimax_trash()
