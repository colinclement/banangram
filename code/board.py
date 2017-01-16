"""
board.py

author: Colin Clement and Samuel Kachuck
date: 2016-01-15

Representation of a Bananagrams board, an unbounded square lattice

"""

from collections import defaultdict


class Board(object):
    def __init__(self):
        self.x = []  # integers of occupied sites x-coords
        self.y = []  # integers of occupied sites y-coords
        self.tile = []
        self.tiledict = defaultdict(str)

    def __repr__(self):
        boardstr = "\033[0;30;47m"
        for y in range(min(self.y), max(self.y)+1):
            for x in range(min(self.x), max(self.x)+1):
                s = self.check(x, y)
                if s:
                    boardstr += s
                else:
                    boardstr += ' '
            boardstr += '\n'
        return boardstr+"\033[0m"

    def place(self, x, y, s):
        self.x.append(x)
        self.y.append(y)
        self.tile.append(s)
        self.tiledict[(x,y)] = s

    def check(self, x, y):
        return self.tiledict[(x,y)]

    def find_anchors(self, down=False, ind=0):
        if down:
            coord, line = self.y, self.x
        else:
            coord, line = self.x, self.y
        occupied = {coord[i] for i,j in enumerate(line) if j == ind}
        left = {o - 1 for o in occupied}
        left.difference_update(occupied)
        return left

    def cross_checks(self, down=False, ind=0):
        if down:
            coord, line = self.y, self.x
        else:
            coord, line = self.x, self.y
        occupied = {coord[i] for i,j in enumerate(line) if j == ind}
        occ_up = {coord[i] for i,j in enumerate(line) if j == ind - 1}
        occ_up.difference_update(occupied)
        occ_down = {coord[i] for i,j in enumerate(line) if j == ind + 1}
        occ_down.difference_update(occupied)
        return occ_up, occ_down


if __name__ == "__main__":
    B = Board()
    xs = [2, 0, 2, 0, 1, 2, 0, 2]
    ys = [-1, 0, 0, 1, 1, 1, 2, 2]
    ss = [s for s in 'claeatts']
    for x, y, s in zip(xs, ys, ss):
        B.place(x, y, s)
