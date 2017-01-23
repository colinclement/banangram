"""
checksolutions.py

author: Colin Clement
date: 2016-01-23

This script generates random tile-selections with the frequency of the 
Banangrams game, checking each solution found to ensure proper behavior
of the algorithm. Random tile selections are unlikely to produce solutions.
"""

import sys
sys.path.append('../')
import random

from graph import DirectedGraph, trie_to_dawg
from bananagram import Bananagrams

w = open('../../data/sowpods.txt', 'r').read()
G = DirectedGraph()
G.parselex(w)
trie_to_dawg(G)
print("DAWG Finished!")

# Bananagrams tile frequency
freq =[13, 3, 3, 6, 18, 3, 4, 3, 12, 2, 2, 5, 3, 8, 11, 3, 2, 9, 6, 9, 6, 3, 3,
       2, 3, 2]
chars = sorted(G.top.children.keys())
tiles = reduce(lambda x, y: x+y, [[chars[i] for j in range(f)] 
                                  for i, f in enumerate(freq)])

B = Bananagrams(G)

testresults = []
nosolve = []
for i in range(50):
    rack = random.sample(tiles, 21)
    rackp = reduce(lambda x, y: x+y, rack)
    print("Attempt {}, rack = {}".format(i, rackp))

    sol = B.solve(rack)
    if sol:
        is_solution, words = B.validate(sol)
        testresults += [[is_solution, sol, rack, words]]
        B.show(sol)
        if is_solution:
            print("Is a solution!")
        else:
            print("Is NOT a solution!")
    else:
        nosolve += [rack]
        print("No solution found for rack {}".format(rackp))

report = 0
for r in testresults:
    report += r[0]

report = float(report)/float(len(testresults))*100.

print("{}% of random selections were correct solutions".format(report))


