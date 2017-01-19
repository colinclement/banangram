"""
testing.py

author: Colin Clement
date: 2016-01-19

Testing script
"""

import sys
sys.path.append('../')

from graph import DirectedGraph, trie_to_dawg
from bananagram import Bananagrams

def testfunction(function, arguments, expectation):
    assert isinstance(arguments, tuple), "arguments must be tuple"
    result = function(*arguments)
    match = result == expectation
    if match:
        print("{}({}) PASSED".format(function.__func__.func_name, 
                                     ' ,'.join(map(str, arguments))))
    else:
        print("{}({}) PASSED".format(function.__func__.func_name, 
                                     ' ,'.join(map(str, arguments))))
    print("Result = {}".format(result))
    return result

testlex = ("at art army ban break bummer cat came car dad dog done den " + 
           "ear eatery met mark mean")
G = DirectedGraph()
G.parselex(testlex)
trie_to_dawg(G)

B = Bananagrams(G)

xs = [0, 1, 2, 3, 4, 5, 0, 0, 0, 0, 5, 5, 5]
ys = [1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 0, 2, 3]
ss = [s for s in 'bummerreakamy']

B.board.placeall(ys, xs, ss)
print(B)

rack = ['e', 'a', 't', 'r', 'd', 'b', 'm', 'o']
testfunction(B.get_words, (3, -1, rack, [], False), [(0, ['ear', 'eatery'])])

