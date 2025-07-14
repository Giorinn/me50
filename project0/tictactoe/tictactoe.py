"""
Tic Tac Toe Player
"""

import math
from email.policy import EmailPolicy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num = 0
    for row in board:
        for item in row:
            if item == X:
                num += 1
            elif item == O:
                num -= 1

    return X if num == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception("the action is not valid")
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("the cell is not empty")

    new_board = [row.copy() for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O

    for col in range(3):
        col_values = [board[0][col], board[1][col], board[2][col]]
        if col_values.count(X) == 3:
            return X
        elif col_values.count(O) == 3:
            return O

    dia1 = [board[i][i] for i in range(3)]
    dia2 = [board[i][2 - i] for i in range(3)]
    if dia1.count(X) == 3 or dia2.count(X) == 3:
        return X
    elif dia1.count(O) == 3 or dia2.count(O) == 3:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return True if winner(board) or all(item != EMPTY for row in board for item in row) else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win_player = winner(board)
    if win_player == X:
        return 1
    elif win_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) is True:
        return None

    cur_player = player(board)
    opt_action = None

    if cur_player == X:
        opt_value = -math.inf

        for action in actions(board):
            cur_board = result(board, action)
            cur_value = max_value(cur_board)
            if cur_value > opt_value:
                opt_action = action
                opt_value = cur_value

    else:
        opt_value = math.inf

        for action in actions(board):
            cur_board = result(board, action)
            cur_value = min_value(cur_board)
            if cur_value < opt_value:
                opt_action = action
                opt_value = cur_value

    return opt_action



def max_value(board):
    if terminal(board):
        return utility(board)
    else:
        return max(min_value(result(board, action)) for action in actions(board))


def min_value(board):
    if terminal(board):
        return utility(board)
    else:
        return min(max_value(result(board, action)) for action in actions(board))
