import sys
sys.path.append('../')
import random

import graph
import bananagram as bg

w = open('../../data/sowpods.txt', 'r').read()
G = graph.DirectedGraph()
G.parselex(w)
graph.trie_to_dawg(G)
print("DAWG Finished!")

# Bananagrams tile frequency
freq =[13, 3, 3, 6, 18, 3, 4, 3, 12, 2, 2, 5, 3, 8, 11, 3, 2, 9, 6, 9, 6, 3, 3,
       2, 3, 2]
chars = sorted(G.top.children.keys())
tiles = reduce(lambda x, y: x+y, [[chars[i] for j in range(f)] 
                                  for i, f in enumerate(freq)])

B = bg.Bananagrams(G)

random.seed(9208914850)
rack = random.sample(tiles, 21)

