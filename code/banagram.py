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
        """ Print the board """
        return self.board.__repr__()

    def cross_check(self, y, x, down=False):
        """
        When searching across (down), find compatible
        letters for adjacent tiles already placed, by
        walking down (across).
        input:
            y, x: ints, coordinates of empty tile with
                    adjacent occupancy to be checked
            down: True/False, current search direction,
                    will look for compatible letters in
                    opposite direction
        returns:
            allowed: list of allowed letters, compatible
                    with words existing on board
        """
        if down:  # Search down, cross-check across
            prefix = self.board.walk(y, x-1, not down, -1)
            suffix = self.board.walk(y, x+1, not down, +1)
        else:  # Search across, cross-check down
            prefix = self.board.walk(y-1, x, not down, -1)
            suffix = self.board.walk(y+1, x, not down, +1)
        node = self.G.downto(prefix)
        if suffix and node.children:
            allowed = []
            for edge in node.children:
                n = node.children[edge].downto(suffix)
                if n:
                    if n.strset:
                        allowed.append(edge)
            return allowed
        else:  # check that children make words
            return [c for c in node.children if node[c].strset]

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

    print("Across")
    for i in range(min(B.board.y)-1, max(B.board.y)+2):
        print('Row ' + str(i))
        anchors = B.board.find_anchors(i)
        print("\tAnchors x = " + (' ,'.join(map(str, anchors))))
        cc = B.board.cross_checks(i)
        for c in cc:
            print("CC for (y,x)=({},{}) across: {}".format(i, c,
                                                           B.cross_check(i, c)))
    print("Down")
    for j in range(min(B.board.x)-1, max(B.board.x)+2):
        print("Column " + str(j))
        anchors = B.board.find_anchors(j, down=True)
        print("\tAnchors x = " + (' ,'.join(map(str, anchors))))
        cc = B.board.cross_checks(j, down=True)
        for c in cc:
            print("CC for (y,x)=({},{}) down: {}".format(c, j,
                                                         B.cross_check(c, j, True)))


