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


def main():

    print "Constructing word dictionary from word list"
    if ADVANCED:
        f = open('/usr/share/dict/words', 'r')
    else:
        f = open('word_lists/wiki-100k.txt', 'r')
    word_dict = [word.lower() for word in f.read().split()]

    added_words = ADDED_WORDS
    word_dict += added_words
    wst = make_trie(word_dict)

    






if __name__ == '__main__':
    main()