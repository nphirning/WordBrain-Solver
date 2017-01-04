# WordBrain-Solver

This repo solves problems of the form introduced in the app WordBrain. This is maintained by Nicholas Hirning.

### Problem Definition ###
WordBrain puzzles consist of a N by N grid of letters (like Boggle). The player is given the word lengths and can connect words as in Boggle (start at any letter and move to any adjacent tile --- even diagonally --- that has yet to be used). When a word is "correct" then it disappears, the letters fall vertically downward, and you continue. The goal is to find the solution sequence of words that empties the board. 

### Word Dictionaries ###
To check if words are valid, I will use either the internal word list (for my MacBook this is located at /usr/share/dict/words) or a corpus of 100k common English words taken from https://gist.github.com/h3xx/1976236.
