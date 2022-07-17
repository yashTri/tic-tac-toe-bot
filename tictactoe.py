"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


# create an exception for invalid action
class InvalidActionError(Exception):
    pass



def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


# returns the current player
def player(board):
    x = 0
    o = 0
    for i in board:
        for j in i:
            if j == X:
                x += 1
            if j == O:
                o += 1

    if x == o:
        return X
    return O


# returns a set of all the possible actions
def actions(board):
    possible = set()
    for i in range(3):
        for j in range(3):

            # if this place is empty, it is possible to draw an X or an O here
            if board[i][j] == EMPTY:
                possible.add((i, j))
    return possible
    

# returns the board 
def result(board, action):
    # if the action is invalid, raise InvalidActionException
    if board[action[0]][action[1]] != EMPTY:
        raise InvalidActionError 
    # create a deep copy, as the old one shouldn't be maximised
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

# returns X if X is the winner, O if O is the winner, and None if none of them is the winner
def winner(board):
    # check the rows
    for i in board:
        if i[0] == i[1] and i[1] == i[2] and i[0] != EMPTY:
            return i[0]
    
    # check the columns
    for i in range(3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    # check the diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[1][1] != EMPTY:
        return board[1][1]
    
    # if there is no winner, return None
    return None


def terminal(board):
    # If somenone has won, the game has ended
    if winner(board) != None:
        return True
    
    # If someone has not won and a move is possible, the game has not ended
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    
    # If no move is possible, the game has ended 
    return True

# returns 1 if X has won, -1 if O has won, 0 otherwise
def utility(board):
    a = winner(board)
    if a == None:
        return 0 
    if a == X:
        return 1
    return -1


# returns a tuple of max-value for this state with the corresponding action (for X)
def maxaction(board):
    # if the game has ended, return the utility of the board
    if terminal(board):
        return (utility(board), tuple())
    pos = actions(board)
    ans = (-2, tuple())
    for i in pos:
        # ans is the max of ans and the min that O can achieve for this action
        ans = max(ans, (minaction(result(board, i))[0], i))
        # if the value for an action is equal to 1, we do not need to look further
        if ans[0] == 1:
            return ans
    return ans

# returns a tuple of min-value for this state with the corresponding action (for O)
def minaction(board):
    # if the game has ended, return the utility of the board
    if terminal(board):
        return (utility(board), tuple())
    pos = actions(board)
    ans = (2, tuple())
    for i in pos:
        # ans is the min of ans and the max that X can achieve for this action
        ans = min(ans, (maxaction(result(board, i))[0], i))
        # if the value for an action is equal to -1, we do not need to look further
        if ans[0] == -1:
            return ans
    return ans

# function that uses the minimax algorithm to
# return the optimal action for the current player
def minimax(board):
    plyr = player(board)
    if plyr == X:
        return maxaction(board)[1]
    else: 
        return minaction(board)[1]

