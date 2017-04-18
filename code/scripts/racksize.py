"""
racksize.py

author: Colin Clement
date: 2017-01-25

This script generates random tile-selections with the frequency of the 
Banangrams game, checking each solution found to ensure proper behavior
of the algorithm. Random tile selections are unlikely to produce solutions.
"""

import sys
sys.path.append('../')
import random
from collections import defaultdict
import pickle

from graph import DirectedGraph, trie_to_dawg
from bananagram import Bananagrams

#w = open('../../data/twl06.txt', 'r').read()
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

sizedict = {}

for s in range(2, 25):
    sizedict[s] = [] 
    for i in range(1000):
        rack = random.sample(tiles, s)
        results = {'rack': rack}
    
        sol = B.solve(rack)
        results['solution'] = sol
        results['branches'] = B._branches
        sizedict[s] += [results]
    report = 0
    for g in sizedict[s]:
        if g['solution']:
            report += 1
    report = float(report)/float(len(sizedict[s]))
    print("{}% of rack size {} solved".format(report*100., s))

pickle.dump(sizedict, open('../../data/2016-01-27-racksize-data-sowpods.pkl',
                           'w'), 0)
