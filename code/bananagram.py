"""
bananagram.py

author: Colin Clement, Samuel Kachuck
date: 2016-01-16

This does it, it plays bananagrams
"""

from collections import defaultdict
from graph import DirectedGraph, trie_to_dawg
from board import Board

def flatten(lst):
    return reduce(lambda x, y: x + y, lst, [])


class Bananagrams(object):
    def __init__(self, dawg, **kwargs):
        self.board = kwargs.get("board", Board())
        self.G = dawg

    def __repr__(self):
        """ Print the board """
        return self.board.show()

    def allwords(self, rack):
        def wordwalk(node, partial, rack):
            results = []
            if node.strset:
                results += [partial]
            for e in node.children:
                if e in rack:
                    rack.remove(e)
                    results += flatten([wordwalk(node[e], partial+e, rack)])
                    rack.append(e)
            return results
        return wordwalk(self.G.top, '', rack)

    def cross_check(self, line, coord, transpose=False, **kwargs):
        """
        When searching across (down), find compatible
        letters for adjacent tiles already placed, by
        walking down (across).
        input:
            line: int, search line (y=line if down=False,
                    x=line if down=True)
            coord: int, coordinate along line (x=coord if
                    down=False, y=coord if down=False)
            transpose: True/False, swap x,y.

            *Note that when down=False (default), line, coord = (y, x), 
             the standard 2d array slicing order. In this way down=True
             is a transpose.
        kwargs:
            board: tuple (ys (list), xs (list), ss (list)) for
                specifying a custom board
        returns:
            allowed: list of allowed letters, compatible
                    with words existing on board
        """
        # NOTE: walk perpendicular to word-building direction!
        prefix = self.board.walk(coord, line-1, not transpose, -1, **kwargs)
        suffix = self.board.walk(coord, line+1, not transpose, +1, **kwargs)
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

    def get_words(self, line, anchor, rack, checks=[], transpose=False,
                  **kwargs):
        """
        input:
            line: int, search line (y=line if down=False,
                    x=line if down=True)
            coord: int, coordinate along line (x=coord if
                    down=False, y=coord if down=False)
            transpose: True/False, swap x,y.
        kwargs:
            board: tuple (ys (list), xs (list), ss (list)) for
                specifying a custom board

            *Note that when down=False (default), line, coord = (y, x), 
             the standard 2d array slicing order. In this way down=True
             is a transpose.
        returns:
            words: list of tuples of the form (start, [word1, word2,...])
                where start is the coordinate along `line` at which each
                word in the tuple begins
        """
        occ = self.board.occupied(line, transpose, **kwargs)
        cross = {c: self.cross_check(line, c, transpose, **kwargs) 
                 for c in checks}
        maxlen = min([len(rack)]+[anchor - o - 1 for o in occ 
                                    if anchor - o > 0])
        prefix = self.board.walk(line, anchor-1, transpose, -1, **kwargs)

        def right(partial, node, coord, rack):
            """
            Build words from rack consistent with partial words beginning
            at coord (along line defined by get_words) by traversing
            DAWG starting at node.
            input:
                partial: str, partial word to build on
                node: Node object, IMPORTANT that it be self.top.downto(partial)
                coord: int, coordinate (along line) to start building word.
                        (should basically always start at an anchor)
                rack: list of str, characters used to build words
            returns:
                list of possible words satisfying board and lexicon constraints
            """
            l = self.board.check(line, coord, transpose, **kwargs)
            results = []
            if l:  # If tile is occupied, use it and continue (or stop)
                if node[l]:
                    results += flatten([right(partial+l, node[l], 
                                              coord+1, rack)])
                return results
            else:  # If tile is unoccupied, try filling it
                if node.strset:
                    results += [partial]
                for e in node.children:
                    allowed = set(rack)
                    if coord in cross:
                        allowed.intersection_update(cross[coord])

                    if e in allowed:
                        rack.remove(e)
                        results += flatten([right(partial+e, node[e],
                                                  coord+1, rack)])
                        rack.append(e)
                return results
            
        def left(partial, node, rack, limit):
            """
            Move left of `anchor` at most `limit` spaces, building words
            to the right by calling `right`.
            input:
                partial: str, partial word
                node: Node object, IMPORTANT that it be self.top
                rack: list of str, characters used to build words
                limit: int, maximum distance to try moving left
            returns:
                list of tuples in format described in get_words docstring
            """
            pos = anchor - (maxlen - limit) + 1 
            complete = right(partial, node, anchor+1, rack)
            results = []
            if complete:
                results = [(pos, complete)]
            if limit > 0:
                for e in node.children:
                    allowed = set(rack)
                    if pos-1 in cross:
                        allowed.intersection_update(cross[pos-1])

                    if e in allowed: 
                        rack.remove(e)
                        results += flatten([left(partial+e, node[e],
                                                 rack, limit-1)])
                        rack.append(e)
            return results

        if prefix:
            pos = anchor - len(prefix)
            # Results using the alread-placed left part
            results =  [(pos, right(prefix, self.G.downto(prefix), anchor, rack))]
            # Results going right from anchor
            results += left('', self.G.top, rack, 0)
            return results
        else:
            return left('', self.G.top, rack, maxlen)

    def consume(self, tiles):
        pass


if __name__ == "__main__":
    anchor_cross = False

    lex = "dad at car cars cat cats do dog dogs done ear ears eat eats deed ate"
    G = DirectedGraph()
    G.parselex(lex)
    trie_to_dawg(G)
    tiles = [s for s in "cateas"]

    B = Bananagrams(G)
    ys = [0, 1, 2, 2, 2, 3]
    xs = [2, 2, 0, 1, 2, 1]
    ss = [s for s in 'eacatt']
    B.board.placeall(ys, xs, ss)

    print(B)

    if anchor_cross:
        print("Across")
        for i in range(min(B.board.y)-1, max(B.board.y)+2):
            print('Row ' + str(i))
            anchors = B.board.find_anchors(i)
            print("\tAnchors x = " + (' ,'.join(map(str, anchors))))
            cc = B.board.cross_checks(i)
            for c in cc:
                allowed = B.cross_check(i, c)
                print("CC for (y,x)=({},{}) across: {}".format(i, c, allowed))
        print("Down")
        for j in range(min(B.board.x)-1, max(B.board.x)+2):
            print("Column " + str(j))
            anchors = B.board.find_anchors(j, transpose=True)
            print("\tAnchors x = " + (' ,'.join(map(str, anchors))))
            cc = B.board.cross_checks(j, transpose=True)
            for c in cc:
                allowed = B.cross_check(j, c, True)
                print("CC for (y,x)=({},{}) down: {}".format(c, j, allowed))

    #print("Test for right extend from (y,x)=(0,2)")
    #print("with rack = 'a', 'r', 't', 's'")
    #print(B._right('', B.G.top, 0, 2, ['a', 'r', 't', 's']))
    #print("")
    print("Test for up to 3 left extend from anchor (y,x)=(0,1)")
    print("with rack = 'a', 'e', 'd', 'd', 'n', 'o', 't'")
    #print('(0,1)', B.get_words(0, 1, ['d', 'r', 'o', 'n', 'a', 't', 'e', 'd']))
    print('(1,1)', B.get_words(1, 1, ['d', 'r', 'o', 'n', 'a', 't', 'e', 'd'],
                               checks=[1]))
