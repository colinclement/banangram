# Solve Bananagrams with any lexicon and set of tiles

## Usage:

```python
from graph import DirectedGraph, trie_to_dawg
from bananagram import Bananagrams

lexicon = open('data/sowpods.txt', 'r').read()
G = DirectedGraph()
G.parselex(lexicon)  # build prefix trie
trie_to_dawg(G)  # reduce graph by merging suffixes

B = Bananagrams(G)

#  Available tiles
rack = [s for s in 'lbwnytkmexroatiliaape']
sol = B.solve(rack)

B.show(sol)  # Print solution!
""" Outputs:
3210123
2  P
1 MIB
0TI AA
1 R LAWN
2 Y L
3   O
4   T
5   E
6  KEX
"""
```
## Bananagrams:

## The rules are simple:
Randomly collect N letter tiles
Use all N letters to make a Scrabble-like grid of words.
If no solution exists, grab more tiles

## The Question: for N randomly grabbed letters, how likely is it that a solution exist?
### Sub-questions: 
1. As N increases, how does likelihood of solution change? Where does the change occur?
2. How does the behavior depend on the distribution of letters grabbable?

## Sources:
  * Thanks to Alex Alemi for suggesting directed acyclic words graphs (DAWG)
  * Appel and Jacobsen (1986) "The World's Fastest Scrabble Program"
  * http://stevehanov.ca/blog/index.php?id=115
