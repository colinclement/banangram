"""
tests.py

Script for testing various functionality

author: Sanuel Kachuck
date: 2016-01-19
"""


from graph import DirectedGraph, trie_to_dawg
from board import Board
#from bananagram import Bananagrams
import bananagram as bg

print('Testing lexicon and DAWG properties')
lex = "dad at car cars cat cats do dog dogs done ear"
lex += "ears eat eats deed ate as read area"
# Test DAWG
G = DirectedGraph()
G.parselex(lex)
trie_to_dawg(G)

print('DAWG.downto works: {}'.format(G.downto('dad') is not None))
print('DAWG structure works: {}'.format(G.top['dad'] is G.top['area']))

# Test Board
board = Board()
ys = [0, 1, 2, 2, 2, 2, 3]
xs = [3, 3, 0, 1, 2, 3, 2]
ss = [s for s in 'easeatt']
board.placeall(ys, xs, ss)

print('Testing board properties')
print(board)

print('Board selects correct tile at (3,0): {}'.format(board.check(0,3)=='e'))
print('Empty tile at (0,0) is empty string: {}'.format(board.check(0,0) is ''))

# Test anchor identify

print('Board finds proper anchor in line 0: {}'.format(board.find_anchors(0)==set([2])))


# Test word option generation with free left
rack = ['d', 'r', 'o', 'n', 'a', 't', 'e', 'd', 'a']
B = bg.Bananagrams(G, board=board)
print B.get_words(0, 2, rack)  # passed 


# Test cross-check location identify

# Test cross-check letter identify
print(B.get_words(1, 2, rack, B.board.cross_checks(1)))  # passed
print(B.get_words(1, 1, rack, B.board.cross_checks(1, True), transpose=True))  # passed
B.board.placeall([1, 3, 4], [1, 1, 1], ['r','a','d'])
for l in 'rad':
    rack.remove(l)

print(B.board)
#
print(B.get_words(1, 2, rack, B.board.cross_checks(1)))  # passed
print(B.get_words(1, 0, rack, B.board.cross_checks(1)))  # passed
print(B.get_words(0, 2, rack, B.board.cross_checks(0)))  # passed
# Test word option generation with preplaced prefix



