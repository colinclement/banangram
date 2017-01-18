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
                s = self.check(y, x)
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

    def check(self, y, x):
        """ Return value of tile at (y, x) or None """
        return self.tiledict[(y, x)]

    #TODO write helper function with nicer arguments for walk

    def coord_line(self, down=False):
        """ Select coordinates for line search down/across"""
        if down:
            return self.y, self.x
        else:
            return self.x, self.y

    def switch(self, y, x, down):
        if down:
            return y, x
        else:
            return x, y

    def walk(self, y, x, down=False, sgn=1):
        """
        Starting at site (y,x), move down (across)
        in direction sgn (+/-1) reading tiles.
        input:
            y, x: ints, coordinates of empty tile with
                    adjacent occupancy to be checked
            down: True/False, walk line
            sgn: +/-1, direction of walk.
                e.g. 'up' is down=True, sgn=-1
        returns:
            path: str of tiles visited
        """
        # Walk along line starting at coord
        if down:  # move along y at constant x
            coord, line = x, y

            def check(yy):
                return self.check(yy, x)
        else:  # move along x at constant y
            coord, line = y, x

            def check(xx):
                return self.check(y, xx)
        path = ''
        tocheck = [line]  # go up or down
        while tocheck:
            nxt = tocheck.pop(0)
            n = check(nxt)
            if n:
                tocheck.append(nxt + sgn)
            if sgn > 0:
                path += n
            else:  # add backwards
                path = n + path
        return path

    def occupied(self, ind, down=False):
        coord, line = self.coord_line(down)
        return {coord[i] for i, j in enumerate(line) if j == ind}

    def find_anchors(self, ind, down=False):
        """
        Find anchor points, left(up)-most unnocupied sites adjacent to occupied
        sites.
        input:
            down: True/False.
            ind: int, row (down=False) or col (down=True)
        returns:
            set of anchor coords in row or col ind
        """
        coord, line = self.coord_line(down)
        occupied = {coord[i] for i, j in enumerate(line) if j == ind}
        left = {o - 1 for o in occupied}
        left.difference_update(occupied)
        return left

    def cross_checks(self, ind, down=False):
        """
        Find points which need to be cross-check for board consistency.
        input:
            ind: int, row (down=False) or col (down=True)
            down: True/False
        returns:
            set of cross-check coords in row or col ind
        """
        coord, line = self.coord_line(down)
        occ = {coord[i] for i, j in enumerate(line) if j == ind}
        up = {coord[i] for i, j in enumerate(line) if j == ind - 1}
        down = {coord[i] for i, j in enumerate(line) if j == ind + 1}
        return (up.union(down)).difference(occ)


if __name__ == "__main__":
    B = Board()
    ys = [-1, 0, 0, 1, 1, 1, 2, 2]
    xs = [2, 0, 2, 0, 1, 2, 0, 2]
    ss = [s for s in 'claeatts']
    B.placeall(ys, xs, ss)
