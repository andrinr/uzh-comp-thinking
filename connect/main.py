import numpy as np
from scipy.ndimage import convolve

size0 = 7 # horizontal, players have to choose a position in this axis
size1 = 6 # vertical, 0 is bottom
compute_depth = 3

def gen_hash(x):
    hash = ''
    for i0, i1 in np.ndindex(x.shape):
        hash += str(int(x[i0, i1]))
    return hash


map = dict()

def player_move(board):
    show_board(board)
    if game_has_ended(board):
        return

    move = input("Enter your next move: ")
    move0 = int(move)
    coords1 = first_zero(board, 1) 
    move1 = coords1[move0]
    next_board = np.copy(board)
    next_board[move0, move1] = -1

    bot_move(next_board)

def bot_move(board):
    if game_has_ended(board):
        return

    predict(board, 0, 1)

def predict(board, depth, player):
    state = win(board)
    if state != 0:
        return 1000 * state

    if depth < compute_depth:
        coords1 = first_zero(board, 1)

        next_board = np.copy(board)
        next_board[0, coords1[0]] = player

        optimal_board = next_board
        next_rating = predict(next_board, depth + 1, player - 2* player)
        optimal_rating = next_rating

        for i0 in range(1, len(coords1)):
            next_board = np.copy(board)
            next_board[i0, coords1[i0]] = player


            next_rating = predict(next_board, depth + 1, player - 2* player)

            if (player == 1 and next_rating > optimal_rating):
                optimal_rating = next_rating
                optimal_board = next_board

            if (player == -1 and next_rating < optimal_rating):
                optimal_rating = next_rating
                optimal_board = next_board
        
        if depth == 0:
            player_move(optimal_board)

        return optimal_rating

    else:
        return rating(board)


def game_has_ended(board):
    state = win(board)

    if state == -1:
        print("You have won the game!")
        return True

    if state == 1:
        print("You have lost the game...")
        return True
    
    if np.sum(np.sum(abs(board))) == size0 * size1:
        print("Stalemate")
        return True

    return False


# Returns -1 when human wins, 1 when bot wins and 0 for no win
def win(board):
    mask_bot = board == 1
    mask_player = board == -1

    sum_bot = np.zeros(size0)
    sum_player = np.zeros(size0)

    # Axis 0
    for i1 in range(size1):
        sum_bot *= mask_bot[:,i1]
        sum_bot += mask_bot[:,i1]
        if 4 in sum_bot:
            return 1

        sum_player *= mask_player[:,i1]
        sum_player += mask_player[:,i1]
        if 4 in sum_player:
            return -1

    sum_bot = np.zeros(size1)
    sum_player = np.zeros(size1)

    # Axis 1
    for i0 in range(size0):
        sum_bot *= mask_bot[i0,:]
        sum_bot += mask_bot[i0,:]
        if 4 in sum_bot:
            return 1

        sum_player *= mask_player[i0,:]
        sum_player += mask_player[i0,:]
        if 4 in sum_player:
            return -1

    mask_bot = np.pad(board == 1, ((0,0), (size0, size0)), 'constant', constant_values=False)
    mask_player = np.pad(board == -1, ((0,0), (size0, size0)), 'constant', constant_values=False)
    sum_bot = np.zeros(size0)
    sum_player = np.zeros(size0)

    # Diagonals along 0, +1
    for i0 in range(size0):
        rolled_mask = mask_bot[i0,size0+i0:2*size0+i0]
        sum_bot *= rolled_mask
        sum_bot += rolled_mask
        if 4 in sum_bot:
            return 1

        rolled_mask = mask_player[i0,size0+i0:2*size0+i0]
        sum_player *= rolled_mask
        sum_player += rolled_mask
        if 4 in sum_player:
            return -1

    sum_bot = np.zeros(size0)
    sum_player = np.zeros(size0)

    # Diagonals along 0, +1
    for i0 in range(size0):
        rolled_mask = mask_bot[i0,size0-i0:2*size0-i0]
        sum_bot *= rolled_mask
        sum_bot += rolled_mask
        if 4 in sum_bot:
            return 1

        rolled_mask = mask_player[i0,size0-i0:2*size0-i0]
        sum_player *= rolled_mask
        sum_player += rolled_mask
        if 4 in sum_player:
            return -1

    return 0

# Define Kernels
kernels = np.zeros((4,3,3))
# horizontal
kernels[0, :, 1] = 1
# vertical
kernels[1, 1,:] = 1
# diagonal
np.fill_diagonal(kernels[2,:,:], 1) 
# diagonal 2
np.fill_diagonal(kernels[3,:,:], 1) 
kernels[3,:,:] = np.flipud(kernels[3,:,:])

#kernels *= 1 / 3

# Rates the state of the board
def rating(board):

    mask_bot = board != -1
    mask_play = board != 1

    rating = 0
    ratings = np.zeros((size0, size1))
    for k in range(4):
        ratings_bot = np.zeros((size0, size1))
        ratings_bot[board == 1] = 1
        for i in range(5):
            ratings_bot = convolve(ratings_bot, kernels[k,:,:], mode='constant', cval=0)
            ratings_bot *= mask_bot
        ratings += ratings_bot

    for k in range(4):
        ratings_player = np.zeros((size0, size1))
        ratings_player[board == -1] = -2
        for i in range(5):
            ratings_player = convolve(ratings_player, kernels[k,:,:], mode='constant', cval=0)
            ratings_player *= mask_play
        ratings += ratings_player

    #show_board(ratings)
    return np.sum(ratings.flatten())


def first_zero(arr, axis):
    mask = arr == 0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), -1)

def show_board(board):
    print(" 0 1 2 3 4 5 6")
    for i1 in range(size1):
        line = '|'
        for i0 in range(size0):
            d = board[i0,size1-1-i1]
            if d == -1:
                line += 'X|'
            elif d == 1:
                line += 'O|'
            else:
                line += ' |'
        print(line)
                
    #print(board.T)

# start
init_board = np.zeros((size0,size1))

player_move(init_board)