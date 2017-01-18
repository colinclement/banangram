"""
board.py

author: Colin Clement and Samuel Kachuck
date: 2016-01-15

Representation of a Bananagrams board, an unbounded square lattice

"""

from collections import defaultdict


class Board(object):
    """ Representation of a Bananagram board """
    def __init__(self):
        self.y = []  # integers of occupied sites y-coords
        self.x = []  # integers of occupied sites x-coords
        self.tile = []
        self.tiledict = defaultdict(str)

    def __repr__(self):
        """ Pretty print the board! Coords are abs """
        xc_range = range(min(self.x), max(self.x)+1)
        boardstr = ' ' + ''.join(map(lambda x: str(abs(x)), xc_range))
        boardstr += '\n'
        for y in range(min(self.y), max(self.y)+1):
            boardstr += str(abs(y)) + "\033[0;30;47m"
            for x in range(min(self.x), max(self.x)+1):
                s = self.check(y, x, transpose=False)
                if s:
                    boardstr += s.upper()
                else:
                    boardstr += ' '
            boardstr += '\033[0m' + '\n'
        return boardstr

    def place(self, y, x, s):
        """ Place tile at y, x with letter s """
        self.y.append(y)
        self.x.append(x)
        self.tile.append(s)
        self.tiledict[(y, x)] = s

    def pop(self, ind=-1):
        """ Removes the last-placed tile and returns y, x, s """
        x, y, s = self.y.pop(ind), self.x.pop(ind), self.tile.pop(ind)
        self.tiledict.pop((y, x))
        return y, x, s

    def placeall(self, ys, xs, ss):
        """ place a list of tiles """
        for y, x, s in zip(ys, xs, ss):
            self.place(y, x, s)

    def check(self, line, coord, transpose=False):
        """ 
        Return value of tile in line, along coord.
            (line, coord) = (y, x) if transpose=False
            (line, coord) = (x, y) if transpose=True
        """
        if transpose:
            y, x = coord, line
        else:
            x, y = coord, line
        return self.tiledict[(y,x)]

    def coord_line(self, transpose=False):
        """ Select coordinates for line search, swap if transpose"""
        if transpose:
            return self.y, self.x
        else:
            return self.x, self.y

    def walk(self, line, coord, transpose=False, sgn=1):
        """
        Starting at site (y,x) = (line, coord) if transpose=False
                         (x,y) = (line, coord) if transpose=True
        in direction sgn (+/-1) along line (across if transpose=False)
        input:
            line: int, line along which to walk 
                (y=line if transpose=False, x=line if tranpose=True)
            coord: int, coordinate along line to start walking
                (x=coord if transpose=False, y=coord if transpose=True)
            transpose: False/True, swap (y,x)
            sgn: +/-1, direction along line of walk.
        returns:
            path: str of tiles visited, including start point
        """
        path = ''
        tocheck = [coord]
        while tocheck:
            nxt = tocheck.pop(0)
            n = self.check(line, nxt, transpose)
            if n:
                tocheck.append(nxt + sgn)
            if sgn > 0:
                path += n
            else:  # add backwards
                path = n + path
        return path

    def occupied(self, line, transpose=False):
        """ 
        Return occupied indices from row y=line (transpose=False)
        or column x=line (transpose=True)
        """
        c, l = self.coord_line(transpose)
        return {c[i] for i, j in enumerate(l) if j == line}

    def find_anchors(self, line, transpose=False):
        """
        Find anchor points, left(up)-most unnocupied sites adjacent to occupied
        tiles.
        input:
            line: int, row (transpose=False) or col (transpose=True)
            transpose: True/False. swap y, x 
        returns:
            set of anchor coords in row or col ind
        """
        occupied = self.occupied(line, transpose)
        left = {o - 1 for o in occupied}
        left.difference_update(occupied)
        return left

    def cross_checks(self, line, transpose=False):
        """
        Find points which need to be cross-check for board consistency.
        input:
            line: int, y = row (transpose=False) or 
                    x=col (transpose=True)
            transpose: True/False, swap y,x
        returns:
            set of cross-check coords in row or col ind
        """
        occupied = self.occupied(line, transpose)
        up = self.occupied(line - 1, transpose) 
        down = self.occupied(line + 1, transpose) 
        return (up.union(down)).difference(occupied)


if __name__ == "__main__":
    B = Board()
    ys = [-1, 0, 0, 1, 1, 1, 2, 2]
    xs = [2, 0, 2, 0, 1, 2, 0, 2]
    ss = [s for s in 'claeatts']
    B.placeall(ys, xs, ss)
