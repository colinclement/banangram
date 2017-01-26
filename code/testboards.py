"""
testboards.py

author: Samuel Kachuck
date: 2017-01-23

Tests N boards for solutions with M tiles initially drawn without replacement
from the Bananagrams tile distribution.
"""

import bananagram as bg
from rack import gen_rack, numlist, genfreqlist
import argparse


parser = argparse.ArgumentParser(description='Test Bananagram solutions.')
parser.add_argument('--N', default = 50, type=int,
                    help='Number of boards to attempt (default 50).')

parser.add_argument('--M', default = 21, type=int,
                    help='Number of tiles to draw (default 21).')

args = parser.parse_args()
N, M = args.N, args.M

with open('../data/twl06.txt', 'r') as infile:
    w = infile.read()

try:
    foo = G.top.downto('aa')
except:
    G = bg.DirectedGraph()
    G.parselex(w)
    bg.trie_to_dawg(G)
    print('Constructed DAWG.')

B = bg.Bananagrams(G)

solutions = []
falsesolutions = []
nosolution = []

for i in range(N):
    rack = gen_rack(M, genfreqlist(numlist), numlist, False)
    print('Testing board {} of {} with rack: {}'.format(i+1, N, rack))
    sol = B.solve(rack)

    if sol:
        val, words = B.validate(sol)
        if val:
            solutions.append(sol)
        else:
            falsesolutions.append(sol)
    else:
        nosolution.append(rack)

msg = 'Out of {} racks with {} tiles, there were {}/{} correct solutions'

print(msg.format(N, M, len(solutions), len(solutions)+len(falsesolutions)))
