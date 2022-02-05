# wordle solver

Yes, another one. In python. This one is trying to rank guesses by using words with high frequency characters in it.

Usage:

python3 wordle.py

The program will give you a suggestion to try in wordle. It will then ask for the result of the word. The format of that is:

XXXXX

where each X is either R, G, or Y. R for characters that are not in the word, Y for characters in the wrong position and G for characters in the right position.
