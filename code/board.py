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
        self.ys = []  # integers of occupied sites y-coords
        self.xs = []  # integers of occupied sites x-coords
        self.ss = []  # list of str at corresponding y, x

    def show(self, **kwargs):
        """ Pretty print the board! Coords are abs """
        ys, xs, ss = kwargs.get('board', (self.ys, self.xs, self.ss))
        xc_range = range(min(xs), max(xs)+1)
        boardstr = ' ' + ''.join(map(lambda x: str(abs(x)), xc_range))
        boardstr += '\n'
        for y in range(min(ys), max(ys)+1):
            boardstr += str(abs(y)) + "\033[0;30;47m"
            for x in range(min(xs), max(xs)+1):
                s = self.check(y, x, transpose=False, **kwargs)
                if s:
                    boardstr += s.upper()
                else:
                    boardstr += ' '
            boardstr += '\033[0m' + '\n'
        return boardstr

    def __repr__(self):
        return self.show()

    def place(self, y, x, s):
        """ Place tile at y, x with letter s """
        assert isinstance(y, int), "y must be int"
        assert isinstance(x, int), "x must be int"
        assert isinstance(s, str), "s must be str"
        self.ys.append(y)
        self.xs.append(x)
        self.ss.append(s)

    def pop(self, ind=-1):
        """ Removes the last-placed tile and returns y, x, s """
        return self.ys.pop(ind), self.xs.pop(ind), self.ss.pop(ind)

    def placeall(self, ys, xs, ss):
        """ place a list of tiles """
        for y, x, s in zip(ys, xs, ss):
            self.place(y, x, s)

    def check(self, line, coord, transpose=False, **kwargs):
        """
        Find value of tile in line, along coord.
            (line, coord) = (y, x) if transpose=False
            (line, coord) = (x, y) if transpose=True
        kwargs:
            board: tuple (ys (list), xs (list), ss (list)) for
                specifying a custom board
        """
        ys, xs, ss = kwargs.get('board', (self.ys, self.xs, self.ss))
        s = None
        if transpose:
            y, x = coord, line
        else:
            x, y = coord, line
        y0, x0 = 0, 0
        while not s:
            try:
                iy = ys.index(y, y0, len(ys))
                ix = xs.index(x, x0, len(xs))
            except ValueError as verr:
                return ''
            if iy == ix:
                s = ss[iy]
            else:
                y0 = max(iy, ix)
                x0 = y0
        return s

    def coord_line(self, transpose=False, **kwargs):
        """
        Select coordinates for line search, swap if transpose

        kwargs:
            board: tuple (ys (list), xs (list), ss (list)) for
                specifying a custom board
        """
        ys, xs, ss = kwargs.get('board', (self.ys, self.xs, self.ss))
        if transpose:
            return xs, ys
        else:
            return ys, xs

    def walk(self, line, coord, transpose=False, sgn=1, **kwargs):
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
        kwargs:
            board: tuple (ys (list), xs (list), ss (list)) for
                specifying a custom board
        returns:
            path: str of tiles visited, including start point
        """
        path = ''
        tocheck = [coord]
        while tocheck:
            nxt = tocheck.pop(0)
            n = self.check(line, nxt, transpose, **kwargs)
            if n:
                tocheck.append(nxt + sgn)
            if sgn > 0:
                path += n
            else:  # add backwards
                path = n + path
        return path

    def occupied(self, line, transpose=False, **kwargs):
        """
        Find occupied indices from row y=line (transpose=False)
        or column x=line (transpose=True)
        kwargs:
            board: tuple (ys (list), xs (list), ss (list)) for
                specifying a custom board
        """
        l, c = self.coord_line(transpose, **kwargs)
        return {c[i] for i, j in enumerate(l) if j == line}

    def find_anchors(self, line, transpose=False, **kwargs):
        """
        Find anchor points, left(up)-most unnocupied sites adjacent to occupied
        tiles.
        input:
            line: int, row (transpose=False) or col (transpose=True)
            transpose: True/False. swap y, x
        kwargs:
            board: tuple (ys (list), xs (list), ss (list)) for
                specifying a custom board
        returns:
            set of anchor coords in row or col ind
        """
        occupied = self.occupied(line, transpose, **kwargs)
        left = {o - 1 for o in occupied}
        left.difference_update(occupied)
        return left

    def cross_checks(self, line, transpose=False, **kwargs):
        """
        Find points which need to be cross-check for board consistency.
        input:
            line: int, y = row (transpose=False) or
                    x=col (transpose=True)
            transpose: True/False, swap y,x
        kwargs:
            board: tuple (ys (list), xs (list), ss (list)) for
                specifying a custom board
        returns:
            set of cross-check coords in row or col ind
        """
        occupied = self.occupied(line, transpose, **kwargs)
        up = self.occupied(line - 1, transpose, **kwargs)
        down = self.occupied(line + 1, transpose, **kwargs)
        return (up.union(down)).difference(occupied)


if __name__ == "__main__":
    B = Board()
    ys = [-1, 0, 0, 1, 1, 1, 2, 2]
    xs = [2, 0, 2, 0, 1, 2, 0, 2]
    ss = [s for s in 'claeatts']
    B.placeall(ys, xs, ss)
