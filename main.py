import numpy as np
from Move import Move
from copy import copy


def generate_board_game(test=False):
    board = np.zeros((3, 3))
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

def available_moves(board):
    x, y = np.where(board == 0)
    return list(zip(x, y))

def win(board, player):
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

def minimax(board, player):
    avail_moves = available_moves(board)

    if win(board, human):
        return -10
    elif win(board, ai):
        return 10
    elif len(avail_moves) == 0:
        return 0

    moves = []

    for index in avail_moves:
        move = Move()
        move.index = index
        board[index[0]][index[1]] = player

        new_board = copy(board)

        if player == ai:
            result = minimax(new_board, human)
            move.score = result.score if isinstance(result, Move) else result
        elif player == human:
            result = minimax(new_board, ai)
            move.score = result.score if isinstance(result, Move) else result

        board[index[0]][index[1]] = 0
        moves.append(move)

    scores = np.array([move.score for move in moves])
    best_score_ind = scores.argmax() if player == ai else scores.argmin()
    return moves[best_score_ind]


if __name__ == "__main__":
    global human
    human = 1
    global ai
    ai = 2
    board_game = generate_board_game(True)
    players = ['human', 'ai']

    player = ai
    while True:
        print(board_game)
        if player == human:
            correct = False
            while not correct:
                move = input("type your move")
                spot = board_game[int(move[0])][int(move[1])]
                if spot == 0:
                    correct = True
                else:
                    print("You can't move here!")
                    correct = False
            board_game[int(move[0])][int(move[1])] = player
        else:
            moves = minimax(board_game, player)
            print('AI moves to {}'.format(moves.index))
            board_game[moves.index[0]][moves.index[1]] = player
        if win(board_game, player) is True:
            print("Player {} wins!".format(player))
            print(board_game)

            break
        if len(available_moves(board_game)) == 0:
            print('It\'s tie!')
            print(board_game)
            break
        if player == human:
            player = ai
        else:
            player = human


