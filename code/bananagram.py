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

def argsort(lst, **kwargs):
    return sorted(range(len(lst)), key=lst.__getitem__, **kwargs)


class Bananagrams(object):
    def __init__(self, dawg, **kwargs):
        self.board = kwargs.get("board", Board())
        self.G = dawg

    def __repr__(self):
        """ Print the board """
        return self.board.show()

    def show(self, board):
        print(self.board.show(board=board))

    def anagrams(self, rack):
        """
        Return all words that can be formed with letters in rack
        input:
            rack: list of str, available characters
        return:
            sorted list of words that can be formed from rack
        """
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
        return sorted(wordwalk(self.G.top, '', rack))

    def firstwords(self, rack):
        """
        Using characters from a rack, returns all words modulo unique 
        prefixes. I.e. the graph is walked using all paths consistent with the
        rack, but only the first terminal node of each path is returned as solve
        will explore the suffixes. 
        input:
            rack: list of str, available characters
        return:
            sorted list of words that can be formed modulo unique prefix.
        """
        def firstwalk(node, partial, rack):
            results = []
            if node.strset:
                results += [partial]
            else:
                for e in node.children:
                    if e in rack:
                        rack.remove(e)
                        results += flatten([firstwalk(node[e], partial+e, rack)])
                        rack.append(e)
            return results
        return sorted(firstwalk(self.G.top, '', rack))

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
        if not node:  # No edges from prefix
            return []
        elif suffix and node.children:
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
                set of possible words satisfying board and lexicon constraints
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
                allowed = set(rack)
                if coord in cross:
                    allowed.intersection_update(cross[coord])
                for e in allowed.intersection(node.children):
                    rack.remove(e)
                    if node[e]:
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
            results = []
            proceed = True  # Check that translated partial is legal
            for i, c in enumerate(partial):
                if pos+i in cross:
                    if not c in cross[pos+i]:
                        proceed = False
            if proceed:
                complete = right(partial, node, anchor+1, rack) if node else []
                if complete:
                    results = [(pos, complete)]
                if limit > 0:
                    allowed = set(rack)
                    if anchor in cross:  # Always adding tile to anchor 
                        allowed.intersection_update(cross[anchor])
                    for e in allowed.intersection(node.children):
                        rack.remove(e)
                        # Move partial left 1, adding edge at anchor
                        results += flatten([left(partial+e, node[e],
                                                 rack, limit-1)])
                        rack.append(e)
            return results

        if prefix:  # Results using the already-placed left part
            pos = anchor - len(prefix)
            results = []
            node = self.G.downto(prefix)
            if node:
                results = [(pos, right(prefix, node, anchor, rack))]
            # Results going right from anchor
            results += left('', self.G.top, rack, 0)
        else:
            results = left('', self.G.top, rack, maxlen)

        output = set([])
        for pos, words in results:
            for w in words:
                output.add((pos, w))
        return output
            
    def updateboard(self, line, coord, word, board, rack, transpose=False):
        """
        Update board and rack with placed word.
        input:
            line: int, line along which word is placed
            coord: int, coordinate along line upon which word is started
            word: str, word to be placed
            board: tuple (ys (list), xs (list), ss (list)), board to be
                    updated
            rack: list of str, letters in rack to be updated
            transpose: True (line=y, coord=x)/False (line=x, coord=y)
        returns:
            board (tuple of lists, updated), rack (list of str, updated)
            # NOTE: Returns copied updated board/rack
        """
        ys, xs, ss = board
        ys, xs = self.board.coord_line(transpose, board=board)
        altrack = rack[:]  # Copies!
        altys, altxs, altss = ys[:], xs[:], ss[:]
        newboard = (altys, altxs, altss)

        for i, l in enumerate(word):
            c = self.board.check(line, coord+i, transpose=False,
                                 board=newboard)
            if not c:  # Play tile if spot is empty
                altrack.remove(l)
                altys.append(line)
                altxs.append(coord+i)
                altss.append(l)

        altys, altxs = self.board.coord_line(transpose, board=newboard)
        return (altys, altxs, altss), altrack

    def solve(self, rack, branch_limit = 100000):
        """
        Solve a bananagram! Only first found solution is returned
        input:
            rack: list of str, letters that we can use
            branch_limit: int, limit on backtrack graph width
                    (default of 100000)
        returns:
            board: tuple of lists (ys, xs, ss), Solution!. If no solution
                    found, empty tuple is returned.
        """
        firstw = self.firstwords(rack)  # order first words by descending len
        #len_ord = argsort(map(len, firstw), reverse=True)
        boards_racks = [self.updateboard(0, 0, firstw[i], ([], [], []), rack) 
                        for i in argsort(map(len, firstw), reverse=True)]
        #boards_racks = [self.updateboard(0, 0, w, ([],[],[]), rack)
        #                for w in self.firstwords(rack)]
        self._solution = ()
        self._branches = 0

        def backtrack(board, rack):
            """
            Backtracking algorithm for searching for words
            """
            self._branches += 1
            ys, xs, ss = board
            ymin, ymax, xmin, xmax = min(ys), max(ys), min(xs), max(xs)

            if len(rack) == 0:  # DONE!
                self._solution = board

            if not self._solution and self._branches < branch_limit:
                # Down moves
                for x in range(xmin, xmax+1):
                    cross = self.board.cross_checks(x, True, board=board)
                    anchors = self.board.find_anchors(x, True, board=board)
                    for a in anchors:
                        wlist = self.get_words(x, a, rack, cross, True,
                                               board=board)
                        for p, word in wlist:
                            nxtb, nxtr = self.updateboard(x, p, word, board,
                                                          rack, True)
                            if nxtr != rack:  # only call again if playable!
                                backtrack(nxtb, nxtr)
            if not self._solution and self._branches < branch_limit:
                # Across moves
                for y in range(ymin, ymax+1):
                    cross = self.board.cross_checks(y, board=board)
                    anchors = self.board.find_anchors(y, board=board)
                    for a in anchors:
                        wlist = self.get_words(y, a, rack, cross, 
                                               board=board)
                        for p, word in wlist:
                            nxtb, nxtr = self.updateboard(y, p, word, board,
                                                          rack)
                            if nxtr != rack:  # only call again if playable!
                                backtrack(nxtb, nxtr)

        # Consider sorting boards_racks by word length, starting with longest
        for b, r in boards_racks:
            if not self._solution and self._branches < branch_limit:
                backtrack(b, r)
        if self._solution:
            self.board.placeall(*self._solution)
        return self._solution

    def validate(self, board):
        """
        Check if board is a valid solution given the lexicon of self.G.
        Find all contiguous lines of tiles longer than one and compare
        to the lexicon.
        input:
            board: tuple of lists (ys, xs, ss)
        returns:
            board is a solution (True/False), list of words on board
        """
        ys, xs, ss = board
        ymin, ymax, xmin, xmax = min(ys), max(ys), min(xs), max(xs)
        # Check down words
        words, solution = [], True
        for x in range(xmin, xmax+1):
            anchors = self.board.find_anchors(x, True, board=board)
            for a in anchors:
                w = self.board.walk(x, a+1, True, 1, board=board)
                if len(w) > 1:
                    words += [w]
                    node = self.G.top.downto(w)
                    if node:
                        if not self.G.top.downto(w).strset:
                            solution = False
                    else:
                        solution = False
        # Check across words
        for y in range(ymin, ymax+1):
            anchors = self.board.find_anchors(y, board=board) 
            for a in anchors:
                w = self.board.walk(y, a+1, False, 1, board=board)
                if len(w) > 1:
                    words += [w]
                    node = self.G.top.downto(w)
                    if node:
                        if not self.G.top.downto(w).strset:
                            solution = False
                    else:
                        solution = False
        return solution, words


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
