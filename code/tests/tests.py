"""
tests.py

Script for testing various functionality

author: Sanuel Kachuck
date: 2016-01-19
"""

import sys
sys.path.append('../')

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
#board.placeall(ys, xs, ss)
# NOTE: I removed placeall so that I could test passing in a custom
#       board through kwarg!
#       It passed!
b = (ys, xs, ss)

print('Testing board properties')
print(board.show(board=b))

print('Board selects correct tile at (3,0): {}'.format(board.check(0,3,
                                                                   board=b)=='e'))
print('Empty tile at (0,0) is empty string: {}'.format(board.check(0,0,
                                                                   board=b) is ''))

# Test anchor identify

print('Board finds proper anchor in line 0: {}'.format(board.find_anchors(0,
                                                                          board=b)==set([2])))


# Test word option generation with free left
rack = ['d', 'r', 'o', 'n', 'a', 't', 'e', 'd', 'a']
B = bg.Bananagrams(G, board=board)

# Test cross-check location identify

# Test cross-check letter identify
def getwords(line, coord, rack, transpose=False, **kwargs):
    return B.get_words(line, coord, rack, 
                       board.cross_checks(line, transpose, **kwargs),
                       transpose, **kwargs)

def anchorat(line, coord, rack, transpose=False, **kwargs):
    if transpose:
        direction = "down"
        x, y = line, coord
    else:
        direction = "across"
        y, x = line, coord
    msg = "(y, x)=({}, {}) {} words = ".format(y, x, direction)
    print(msg + '\n\t'.join(map(str, getwords(line, coord, 
                                           rack, transpose,
                                           **kwargs))))

anchorat(0, 2, rack, board=b)  # passed 
anchorat(1, 2, rack, board=b)  # passed
anchorat(1, 1, rack, True, board=b)  # passed
#B.board.placeall([1, 3, 4], [1, 1, 1], ['r','a','d'])
ys += [1, 3, 4]
xs += [1, 1, 1]
ss += ['r','a','d']
for l in 'rad':
    rack.remove(l)

print(B.board.show(board=b))
#
anchorat(1, 2, rack, board=b)  # passed
anchorat(1, 0, rack, board=b)  # passed 
anchorat(0, 2, rack, board=b)  # passed
# Test word option generation with preplaced prefix



