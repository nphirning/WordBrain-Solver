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


def main():

    print "Constructing word dictionary from word list"
    if ADVANCED:
        f = open('/usr/share/dict/words', 'r')
    else:
        f = open('word_lists/wiki-100k.txt', 'r')
    word_dict = [word.lower() for word in f.read().split()]
    word_dict += ADDED_WORDS
    wst = make_trie(word_dict)

    






if __name__ == '__main__':
    main()