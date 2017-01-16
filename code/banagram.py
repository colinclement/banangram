"""
bananagram.py

author: Colin Clement, Samuel Kachuck
date: 2016-01-16

This does it, it plays bananagrams
"""

from board import Board
from graph import DirectedGraph, trie_to_dawg


class Bananagrams(object):
    def __init__(self, dawg, **kwargs):
        self.board = kwargs.get("board", Board())
        self.G = dawg

    def __repr__(self):
        return self.board.__repr__()

    def cross_check(self, x, y, down=False):
        check = [y-1]
        prefix = ''
        # Look above empty tile
        while check:
            up = check.pop(0)
            n = self.board.check(x,up)
            prefix = n + prefix
            if n:
                check.append(up-1)
        # Walk down DAWG to empty tile
        node = self.G.downto(prefix)
        # Are there tiles below?
        if self.board.check(x, y+1):
            # What chars have allowed suffix?
            check = [y+1]
            suffix = ''
            while check:
                down = check.pop(0)
                n = self.board.check(x, down)
                suffix += n
                if n:
                    check.append(down+1)
            c = node.children
            allowed = []
            for k in node.children:
                n = node.children[k].downto(suffix)
                if n.strset:
                    allowed.append(k)
            return allowed
        else:
            return node.children.keys()

    def solve(self, tiles):
        pass

if __name__ == "__main__":
    lex = "at car cars cat cats do dog dogs done ear ears eat eats"
    G = DirectedGraph()
    G.parselex(lex)
    trie_to_dawg(G)
    tiles = [s for s in "cateas"]

    B = Bananagrams(G)
    xs = [2, 2, 0, 1, 2]
    ys = [0, 1, 2, 2, 2]
    ss = [s for s in 'eacat']
    B.board.placeall(xs, ys, ss)

    print(B)

    print(B.cross_check(2,3))

