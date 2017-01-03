# WORDBRAIN SOLVER
# ----------------

import copy
import sys
import fileinput

ADDED_WORDS = ['tv', 'haystack', 'crab', 'scooter', 'snowman', 'elk', 'chimney', 'cabin', 'biscuit', 'mince']
BOARD_DIM = 4
WORD_LENGTHS = [4,6,6]
BOARD_STRING = 'raweebtlmturtins'
ADVANCED = False

################# TRIE FUNCTIONS #################

# Adapted from http://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python

def make_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict['_end_'] = '_end_'
    return root

def in_trie(trie, word):
    current_dict = trie
    for letter in word:
        if letter in current_dict:
            current_dict = current_dict[letter]
        else:
            return 0
    else:
        if '_end_' in current_dict:
            return 1
        else:
            return 2 #Prefix is in trie

########################################################

def generate_new_board(grid, word_data):
    """ Given a board and a chosen word (with sequence of coords.)
        generate a new board (simulating letters falling)

    grid:       the current grid as a list of row-strings
    word_data:  tuple of (word, array of coordinates for choosing the letters from grid)

    Returns new board
    """
    new_board = []
    temp = '?' * len(grid[0])
    for i in range(len(grid)):
        new_board.append(temp)

    for col in range(len(grid[0])):
        counter = len(grid)
        for j in range(len(grid)):
            row = len(grid) - j - 1
            if (row, col) not in word_data[1] and grid[row][col] != '?':
                counter -= 1
                new_board[counter] = new_board[counter][:col] + grid[row][col] + new_board[counter][col+1:]
    return new_board 

def find_valid_words(grid, row, col, valid_lengths, word_list):
    """
    Given a grid and a (row, col) to search from, as well as a word list
    of valid words and a list of valid lengths, return a list of the valid words
    """
    explored = []
    for i in range(len(grid)):
        temp = []
        for j in range(len(grid[0])):
            temp.append(False)
        explored.append(temp)

    words = find_valid_words_helper(grid, row, col, ['',[]], explored, valid_lengths, [], word_list, max(valid_lengths))
    if words == None: return []
    return words

def find_valid_words_helper(grid, row, col, current_string, explored_grid, valid_lengths, valid_words, word_list, max_length):

    if row >= len(grid) or row < 0:
        return None
    if col >= len(grid[0]) or col < 0:
        return None
    if explored_grid[row][col]:
        return None
    if len(current_string[0]) + 1 > max_length:
        return None

    current_string[0] += grid[row][col]
    current_string[1].append((row, col))

    if in_trie(word_list, current_string[0]) == 0:
        current_string[0] = current_string[0][:-1]
        del current_string[1][-1]
        return None
    if in_trie(word_list, current_string[0]) == 1 and len(current_string[0]) in valid_lengths:
        valid_words.append(copy.deepcopy(current_string))

    explored_grid[row][col] = True

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0: continue
            words_found = find_valid_words_helper(grid, row + i, col + j, current_string, explored_grid, valid_lengths, valid_words, word_list, max_length)
            if words_found != None: valid_words = words_found

    current_string[0] = current_string[0][:-1]
    del current_string[1][-1]

    explored_grid[row][col] = False
    return valid_words

def grid_is_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != '?':
                return False
    return True

def grid_is_full(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '?':
                return False
    return True

def solve_wb(grid_arrays, valid_lengths, solutions, word_list, print_):
    # Solves wordbrain
    for row in range(len(grid_arrays[-1][0])):
        for col in range(len(grid_arrays[-1][0][0])):

            remaining_valid_lengths = [valid_lengths[i][0] for i in range(len(valid_lengths)) if valid_lengths[i][1]]
            valid_words = find_valid_words(grid_arrays[-1][0], row, col, remaining_valid_lengths, word_list)
            """if grid_is_full(grid_arrays[-1][0]):
                print "****************"
                print row, col
                print valid_words
                print grid_arrays[-1][0]"""

            for word_data in valid_words:
                new_grid = generate_new_board(grid_arrays[-1][0], word_data)
                grid_arrays.append([new_grid, word_data])
                
                """if grid_is_full(grid_arrays[-1][0]):
                    print "LOOKING AT ", word_data
                    print new_grid"""

                for i in range(len(valid_lengths)):
                    if valid_lengths[i][0] == len(word_data[0]) and valid_lengths[i][1] == True:
                        valid_lengths[i][1] = False
                        break
                

                if grid_is_empty(new_grid):
                    solutions.append(copy.deepcopy(grid_arrays))
                    if print_: print [x[1][0] for x in grid_arrays if x[1] != None]
                else:
                    solve_wb(grid_arrays, valid_lengths, solutions, word_list, print_)

                for i in range(len(valid_lengths)):
                    if valid_lengths[i][0] == len(word_data[0]) and valid_lengths[i][1] == False:
                        valid_lengths[i][1] = True
                        break
                


                del grid_arrays[-1]
    return solutions

def main(advanced_dict, added_words, word_lengths, board_dim, board_string, print_):

    if print_: print "Constructing word dictionary from word list"
    if advanced_dict:
        f = open('/usr/share/dict/words', 'r')
    else:
        f = open('word_lists/wiki-100k.txt', 'r')
    word_dict = [word.lower() for word in f.read().split()]
    word_dict += added_words
    wst = make_trie(word_dict)

    numbers = word_lengths
    boards = []
    prev = 0
    original_board = []
    for i in range(board_dim, len(board_string) + 1, board_dim):
        original_board.append(board_string[prev:i])
        prev = i

    solutions = []
    boards.append([original_board, None])
    valid_lengths_dict = []
    for length in numbers:
        valid_lengths_dict.append([length, True])

    solve_wb(boards, valid_lengths_dict, solutions, wst, print_)

    solution_words = []
    for gridarrays in solutions:
        solution_words.append([x[1][0] for x in gridarrays if x[1] != None])
    return solution_words






if __name__ == '__main__':
    main(ADVANCED, ADDED_WORDS, WORD_LENGTHS, BOARD_DIM, BOARD_STRING, True)