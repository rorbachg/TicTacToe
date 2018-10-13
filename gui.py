import sys
import numpy as np
import subprocess
from Move import Move
from copy import copy
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 500
        self.init_ui()
        self.human = 1
        self.ai = 2
        self.size = 3
        self.board_game = self.generate_board_game(self.size, False)
        self.player = 1
        self.button_list = [self.b, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9]
        self.max_depth = 8

    def init_ui(self):
        self.b = QtWidgets.QPushButton('')
        self.b2 = QtWidgets.QPushButton('')
        self.b3 = QtWidgets.QPushButton('')
        self.b4 = QtWidgets.QPushButton('')
        self.b5 = QtWidgets.QPushButton('')
        self.b6 = QtWidgets.QPushButton('')
        self.b7 = QtWidgets.QPushButton('')
        self.b8 = QtWidgets.QPushButton('')
        self.b9 = QtWidgets.QPushButton('')


        self.b.setProperty('index', (0, 0))
        self.b2.setProperty('index', (0, 1))
        self.b3.setProperty('index', (0, 2))
        self.b4.setProperty('index', (1, 0))
        self.b5.setProperty('index', (1, 1))
        self.b6.setProperty('index', (1, 2))
        self.b7.setProperty('index', (2, 0))
        self.b8.setProperty('index', (2, 1))
        self.b9.setProperty('index', (2, 2))


        self.b.setFixedSize(100, 100)
        self.b2.setFixedSize(100, 100)
        self.b3.setFixedSize(100, 100)
        self.b4.setFixedSize(100, 100)
        self.b5.setFixedSize(100, 100)
        self.b6.setFixedSize(100, 100)
        self.b7.setFixedSize(100, 100)
        self.b8.setFixedSize(100, 100)
        self.b9.setFixedSize(100, 100)


        self.setGeometry(self.left, self.top, self.width, self.height)

        grid = QtWidgets.QGridLayout()

        grid.addWidget(self.b, 0, 0)
        grid.addWidget(self.b2, 0, 1)
        grid.addWidget(self.b3, 0, 2)
        grid.addWidget(self.b4, 1, 0)
        grid.addWidget(self.b5, 1, 1)
        grid.addWidget(self.b6, 1, 2)
        grid.addWidget(self.b7, 2, 0)
        grid.addWidget(self.b8, 2, 1)
        grid.addWidget(self.b9, 2, 2)



        self.setLayout(grid)
        self.setWindowTitle('PyQt5 Lesson 5')

        self.b.clicked.connect(self.btn_click)
        self.b2.clicked.connect(self.btn_click)
        self.b3.clicked.connect(self.btn_click)
        self.b4.clicked.connect(self.btn_click)
        self.b5.clicked.connect(self.btn_click)
        self.b6.clicked.connect(self.btn_click)
        self.b7.clicked.connect(self.btn_click)
        self.b8.clicked.connect(self.btn_click)
        self.b9.clicked.connect(self.btn_click)
        self.center()
        self.show()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def btn_click(self):
        sender = self.sender()
        move = sender.property('index')
        self.player = self.human
        if self.board_game[int(move[0])][int(move[1])] == 0:
            self.board_game[int(move[0])][int(move[1])] = self.player
            sender.setText("O")
            sender.setStyleSheet('QPushButton {color: blue; font-size: 26pt; font-weight: bold}')
            print(self.board_game)
            if not self.check_result():
                self.player = self.ai
                depth = 0
                moves = self.minimax(self.board_game, self.player, depth)
                print(moves)
                but_idx = [button.property('index') for button in self.button_list].index(moves.index)
                print(but_idx)

                print('AI moves to {}'.format(moves.index))
                self.board_game[moves.index[0]][moves.index[1]] = self.ai
                self.button_list[but_idx].setText("X")
                self.button_list[but_idx].setStyleSheet('QPushButton {color: red; font-size: 26pt; font-weight: bold}')
                print(self.board_game)
            self.check_result()

    def check_result(self):
        players = {self.human: "Human", self.ai: "AI"}
        if self.win(self.board_game, self.player) is True:
            print("Player {} wins!".format(self.player))
            QtWidgets.QMessageBox.about(self, "Result", "{} wins!".format(players[self.player]))
            self.close()
            self.__init__()

            return True

        if len(self.available_moves(self.board_game)) == 0:
            print('It\'s tie!')
            QtWidgets.QMessageBox.about(self, "Result", 'It\'s tie!'.format(self.player))
            self.close()
            self.__init__()
            return True
        return False


    def generate_board_game(self, size, test=False):
        board = np.zeros((size, size))
        if test:
            # #CASE
            # board[0][0] = 1
            # board[0][2] = 2
            # board[1][0] = 2
            # board[1][2] = 2
            # board[2][1] = 1
            # board[2][2] = 1

            # #CASE
            # board[0][0] = 2
            # board[1][0] = 1
            # board[1][1] = 1

            # #CASE
            board[0][0] = 2
            board[0][1] = 1
            board[0][2] = 2
            board[1][0] = 1
            board[1][1] = 1
            board[1][2] = 2
            board[2][0] = 1
        return board

    def available_moves(self, board):
        x, y = np.where(board == 0)
        return list(zip(x, y))

    def win(self, board, player):
        if ((board[0] == player).all() or
                (board[1] == player).all() or
                (board[2] == player).all() or
                (board[:, 0] == player).all() or
                (board[:, 1] == player).all() or
                (board[:, 2] == player).all() or
                (board.diagonal() == player).all() or
                (np.fliplr(board).diagonal() == player).all()):
            return True
        return False

    def minimax(self, board, player, depth):
        depth += 1
        # print(depth)
        avail_moves = self.available_moves(board)

        if self.win(board, self.human):
            return -10
        elif self.win(board, self.ai):
            return 10
        elif len(avail_moves) == 0 or depth == self.max_depth:
            return 0

        moves = []

        for index in avail_moves:
            move = Move()
            move.index = index
            board[index[0]][index[1]] = player

            new_board = copy(board)
            new_depth = copy(depth)
            if player == self.ai:
                result = self.minimax(new_board, self.human, depth)
                move.score = result.score if isinstance(result, Move) else result
            elif player == self.human:
                result = self.minimax (new_board, self.ai, depth)
                move.score = result.score if isinstance(result, Move) else result

            board[index[0]][index[1]] = 0
            moves.append(move)

        scores = np.array([move.score for move in moves])
        #best_score_ind = scores.argmax() if player == self.ai else scores.argmin()
        best_score_ind = np.random.choice(np.flatnonzero(scores == scores.max() if player == self.ai else scores == scores.min()))
        return moves[best_score_ind]


if __name__== "__main__":
    app = QtWidgets.QApplication(sys.argv)
    a_window = Window()
    sys.exit(app.exec_())
