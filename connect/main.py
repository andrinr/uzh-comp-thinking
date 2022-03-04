import numpy as np

size0 = 7 # horizontal
size1 = 6 # vertical, 0 is bottom
compute_depth = 4

def gen_hash(x):
    hash = ''
    for i0, i1 in np.ndindex(x.shape):
        hash += str(int(x[i0, i1]))
    return hash


map = dict()

def player_move(board):
    if game_has_ended(board):
        return

    move = input("Enter your next move: ")
    move0 = int(move[0])
    move1 = int(move[1])

    next_board = np.copy(board)
    next_board[move0, move1] = -1

    bot_move(next_board)

def bot_move(board):
    if game_has_ended(board):
        return

    hash = gen_hash(board)

    if hash in map:
        move0, move1, rating = map[has]
    else:
        first_zero(board, 1)

    next_board = np.copy(board)
    next_board[move0, move1] = -1

    bot_move(next_board)

    
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

    

def compute_strategy(board):

    placable = first_zero(board, 1)

    for pos0 in range(size0):
        pos1 = placable[pos0]
        if pos1 == -1 : continue

        #for off0 in range(max(0, pos0-3), min(pos0)):

    
    return 0

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
        print(np.roll(mask_player[i0,:], i0))
        if 4 in sum_player:
            return -1

    return 0

# Rates the state of the board
def rating(board):
    mask_bot_pad = board != -1
    mask_player_pad = board != 1

    sum_bot = np.zeros(size0)
    sum_player = np.zeros(size0)

    total_rating = 0

    # Axis 0
    for i1 in range(size1):
        sum_bot *= mask_bot_pad[:,i1]
        sum_bot += board[mask_bot_pad][:,i1]
    
        sum_player *= mask_player_pad[:,i1]
        sum_player += board[mask_player_pad][:,i1]
        
        total_rating += sum(sum_bot)
        total_rating += sum(sum_player)


    sum_bot = np.zeros(size1)
    sum_player = np.zeros(size1)

    # Axis 1
    for i0 in range(size0):
        sum_bot *= mask_bot_pad[i0,:]
        sum_bot += board[mask_bot_pad][i0,:]

        sum_player *= mask_player_pad[i0,:]
        sum_player += board[mask_player_pad][i0,:]
        
        total_rating += sum(sum_bot)
        total_rating += sum(sum_player)

    mask_bot_pad = np.pad(board == 1, ((0,0), (size0, size0)), 'constant', constant_values=False)
    mask_player_pad = np.pad(board == -1, ((0,0), (size0, size0)), 'constant', constant_values=False)
    sum_bot = np.zeros(size0)
    sum_player = np.zeros(size0)

    # Diagonals along 0, +1
    for i0 in range(size0):
        rolled_mask = mask_bot_pad[i0,size0+i0:2*size0+i0]
        sum_bot *= mask_bot_pad[i0,size0+i0:2*size0+i0]
        sum_bot += mask_bot_pad[i0,size0+i0:2*size0+i0]

        rolled_mask = mask_player_pad[i0,size0+i0:2*size0+i0]
        sum_player *= rolled_mask
        sum_player += rolled_mask
        
        total_rating += sum(sum_bot)
        total_rating += sum(sum_player)

    sum_bot = np.zeros(size0)
    sum_player = np.zeros(size0)

    # Diagonals along 0, +1
    for i0 in range(size0):
        rolled_mask = mask_bot_pad[i0,size0-i0:2*size0-i0]
        sum_bot *= rolled_mask
        sum_bot += rolled_mask

        rolled_mask = mask_player_pad[i0,size0-i0:2*size0-i0]
        sum_player *= rolled_mask
        sum_player += rolled_mask

        total_rating += sum(sum_bot)
        total_rating += sum(sum_player)
       
    return total_rating


def first_zero(arr, axis):
    mask = arr == 0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), -1)


# start
init_board = np.zeros((size0,size1))
init_board[3,0] = -1
init_board[2,1] = -1
init_board[1,2] = -1
init_board[0,3] = -1

compute_strategy(init_board)



print(np.roll(mask_player[i0,:], i0))