"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

# Initialize X, O, and EMPTY
X = 'X'
O = 'O'
EMPTY = None


def initial_state():
    """
    Returns the initial state of the board, being an EMPTY 2D numpy array.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns the player who has the next turn on a board.
    """
    x_counter = 0
    o_counter = 0

    # Loop through the board and increment the X/O counts if found
    for row in board:
        for item in row:
            if item == X:
                x_counter += 1
            if item == O:
                o_counter += 1

    # X is the initial player, therefore prioritized over O
    if x_counter <= o_counter:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    # Loop through all items in the board and retrieve all EMPTY spaces
    # This is done by tracking the current item in the loop through enumerate()
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            if item == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ActionError("The given action was invalid.")

    # Unpack 'action', make a deepcopy of the board, get the next player,
    # then assign the next player's value to our resulting action
    i, j = action
    result_board = deepcopy(board)
    next_player = player(board)
    result_board[i][j] = next_player
    
    return result_board


def winner(board):
    """
    Returns the winner of the game. Returns None if the game tied or is still in progress.
    """
    wins = [[(0, 0), (0, 1), (0, 2)], # Horizontal Top
            [(1, 0), (1, 1), (1, 2)], # Horizontal Middle
            [(2, 0), (2, 1), (2, 2)], # Horizontal Bottom
            [(0, 0), (1, 1), (2, 2)], # Diagonal
            [(0, 2), (1, 1), (2, 0)], # Diagonal
            [(0, 0), (1, 0), (2, 0)], # Vertical Left
            [(0, 1), (1, 1), (2, 1)], # Vertical Middle
            [(0, 2), (1, 2), (2, 2)]] # Vertical Right

    for win in wins:
        x_counter = 0
        o_counter = 0

        for i, j in win:
            if board[i][j] == X:
                x_counter += 1
            if board[i][j] == O:
                o_counter += 1

        if x_counter == 3:
            return X
        if o_counter == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Checks if any of the board's spots remain EMPTY or if the board has not yet crowned a winner
    if not actions(board) or winner(board) is not None:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)

    if game_winner == X:
        return 1
    if game_winner == O:
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the next player on the board.
    """
    if terminal(board):
        return None

    # Optimizing the AI to use the most optimal moves at the start
    if board[1][1] == EMPTY and player(board) == O:
        return 1, 1
    if board == initial_state():
        return 0, 0

    next_player = player(board)
    best_value = -2 if next_player == X else 2

    # Looping through all possible actions and
    # finding the most valuable (optimal) action
    for action in actions(board):
        new_value = find_value(result(board, action), best_value)

        if next_player == X:
            new_value = max(best_value, new_value)
        if next_player == O:
            new_value = min(best_value, new_value)

        if new_value != best_value:
            best_value = new_value
            optimal_action = action

    return optimal_action


def find_value(board, best_value):
    """
    Finds the best value for each recursive iteration. Optimized to use Alpha-Beta Pruning.
    """
    if terminal(board):
        return utility(board)

    next_player = player(board)
    value = -2 if next_player == X else 2

    # Loops through all possible actions and finds their corresponding value
    for action in actions(board):
        new_value = find_value(result(board, action), value)

        if next_player == X:
            if new_value > best_value:
                return new_value
            
            value = max(value, new_value)

        if next_player == O:
            if new_value < best_value:
                return new_value
            
            value = min(value, new_value)

    return value


class ActionError(Exception):
    """Raised when an action is None or returns an invalid value."""
    pass