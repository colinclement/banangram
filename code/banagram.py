"""
bananagram.py

author: Colin Clement, Samuel Kachuck
date: 2016-01-16

This does it, it plays bananagrams
"""

from board import Board
from graph import DirectedGraph, trie_to_dawg

def flatten(lst):
    return reduce(lambda x, y: x + y, lst, [])


class Bananagrams(object):
    def __init__(self, dawg, **kwargs):
        self.board = kwargs.get("board", Board())
        self.G = dawg

    def __repr__(self):
        """ Print the board """
        return self.board.__repr__()

    # TODO: No 'if down:' in bananagram, only in board!
    # Figure out better, more consistent convention. Or
    # Commit fully to the transposition idea...

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

    def _right(self, partial, node, y, x, rack, down=False):
        # TODO: Make bidirectional
        l = self.board.check(y, x)
        results = []
        if l:
            if node[l]:
                results += flatten([self._right(partial+l, node[l], 
                                                y, x+1, rack, down)])
            return results
        else:
            for e in node.children:
                if e in rack: #and cross-check
                    rack.remove(e)
                    results += flatten([self._right(partial+e, node[e],
                                                    y, x+1, rack, down)])
                    rack.append(e)
            if node.strset:
                results += [partial]
            return results
 
    def _prefix(self, rack, ind, down=False):
        """
        Return all possible left parts at each anchor in row/col ind
        """
        #NOTE: ANCHOR IS EMPTY!
        anchors = sorted(self.board.find_anchors(ind, down))
        checks = sorted(self.board.cross_checks(ind, down))
        occ = sorted(self.board.occupied(ind, down))
        if down:  # dict(coord: {allowed edges})
            cross = {c: self.cross_checks(c, ind, down) for c in checks}
        else:
            cross = {c: self.cross_checks(ind, c, down) for c in checks}
        leftparts = defaultdict(list)
        for i, a in enumerate(anchors):
            #leftparts[a] += ['']
            if i:
                maxleft = min(len(rack), anchors[i]-anchors[i-1])
                maxleft = min(maxleft, min([a - o for o in occ if a - o > 0]))
                maxleft = min(maxleft-2, len(rack))
            else:  # first one, bounded only by rack size
                maxleft = len(rack)
            prefix = self.board.walk(ind, a-1, down, -1)
            if prefix:
                return prefix
            else:  # walk the DAWG
                for l in range(maxleft):
                    if a-l in cross:  # check
                        pass
                    else:
                        pass  # walk
                   
    def _leftpart(self):
        pass
                    
    def consume(self, tiles):
        pass


if __name__ == "__main__":
    anchor_cross = False

    lex = "at car cars cat cats do dog dogs done ear ears eat eats"
    G = DirectedGraph()
    G.parselex(lex)
    trie_to_dawg(G)
    tiles = [s for s in "cateas"]

    B = Bananagrams(G)
    ys = [0, 1, 2, 2, 2]
    xs = [2, 2, 0, 1, 2]
    ss = [s for s in 'eacat']
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
            anchors = B.board.find_anchors(j, down=True)
            print("\tAnchors x = " + (' ,'.join(map(str, anchors))))
            cc = B.board.cross_checks(j, down=True)
            for c in cc:
                allowed = B.cross_check(c, j, True)
                print("CC for (y,x)=({},{}) down: {}".format(c, j, allowed))

    print("Test for right extend from (y,x)=(0,2)")
    print("with rack = 'a', 'r', 't', 's'")
    print(B._right('', B.G.top, 0, 2, ['a', 'r', 't', 's']))
