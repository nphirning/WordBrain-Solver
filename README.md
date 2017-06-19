# WordBrain-Solver

This repo solves problems of the form introduced in the app WordBrain.

## Instructions

This project is not intended to be easy to use. There is no GUI. That being said, if you want to use it (maybe, like me, you want to win a competition against a family member in the app WordBrain), then you better follow these instructions.

* Inside `src/solver.py` you will see some global constants (e.g., `BOARD_STRING`). Each of these constants has a meaning and can be used to customize the behavior of the code. These constants are described below.
  * `ADDED_WORDS` -- a Python list of words that do not show up in the dictionary, but should. It's fine if you add words that do show up in the dictionary (e.g., if you switch to a different dictionary). 
  * `BOARD_DIM` -- dimension of the board (e.g., 4 means you're dealing with a 4-by-4 board).
  * `WORD_LENGTHS` -- lengths of the words we're looking for.
  * `BOARD_STRING` -- the starting position of the board read in horizontal lines from top left to bottom right. 
  * `ADVANCED` -- true if you want to use the internal Mac word list; false uses the 100k Wiki word list. 
* The Python script must be invoked from the root directory of the repo (lame, I know, but I don't feel like updating it). 

## Problem Definition 
WordBrain puzzles consist of a N by N grid of letters (like Boggle). The player is given the word lengths and can connect words as in Boggle (start at any letter and move to any adjacent tile --- even diagonally --- that has yet to be used). When a word is "correct" then it disappears, the letters fall vertically downward, and you continue. The goal is to find the solution sequence of words that empties the board. 

## Word Dictionaries 
To check if words are valid, I will use either the internal word list (for my MacBook this is located at /usr/share/dict/words) or a corpus of 100k common English words taken from https://gist.github.com/h3xx/1976236.
