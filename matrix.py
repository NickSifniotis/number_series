# -*- Mode: Python; tab-width: 4 -*-
#
#	Author: Sam Rushing <rushing@nightmare.com>
#
# One goal is to work with any object type that supports the numeric
# protocol.  (i.e., classes for rationals, complex or even matrices)
#
# Algorithms are from
# Cormen, Leiserson & Rivest, <Introduction to Algorithms>, Ch. 31
#
# Warning: ItoA thinks a[i,j] == a[row,column], whereas I
# think a[i,j] == a[column, row].  beware of arbitrary-seeming
# index-reversals!

# Note: I made a small change to yarn.py, in order to better accomodate
# this sort of thing:  yarn.Rat (Rat(1,3), Rat(1,4))
#
# 252c252,256
# <                       n, d = int(args[0]), int(args[1])
# ---
# >                       if ((type(args[0]) != types.InstanceType)
# >                           or self.__class__ != args[0].__class__):
# >                           n, d = int(args[0]), int(args[1])
# >                       else:
# >                           n, d = args[0], args[1]
#
#
# Modified somewhat by Nick Sifniotis 8th December 2015
# This class now works correctly with Python 3.4


class Matrix:
    def __init__(self, size=(3, 3)):
        if type(size) is list:
            # another option for creation
            self.v = size
        else:
            c, r = size
            rows = []
            for i in range(r):
                rows.append([0] * c)
            self.v = rows

    # --------------------------------------------------
    # mutation
    # --------------------------------------------------

    def size(self):
        """
        returns (columns, rows)
        :return:
        """
        return len(self.v[0]), len(self.v)

    def __setitem__(self, coords, v):
        (x, y) = coords
        self.v[y][x] = v

    set = __setitem__

    def __getitem__(self, coords):
        (x, y) = coords
        return self.v[y][x]

    get = __getitem__

    # --------------------------------------------------
    # operations
    # --------------------------------------------------

    def copy(self):
        v = []
        for row in self.v:
            v.append(row[:])
        return Matrix(v)

    def __cmp__(self, other):
        ss = self.size()
        os = other.size()
        if ss != os:
            return 1
        else:
            # this does a 'deep' compare
            return not (self.v == other.v)

    def __mul__(self, other):
        ss = self.size()
        os = other.size()
        if ss[0] != os[1]:
            raise ValueError("dimensions do not match")
        new = Matrix((os[0], ss[1]))
        for i in range(os[0]):
            for j in range(ss[1]):
                total = 0
                for k in range(ss[0]):
                    total += (self[k, j] * other[i, k])
                new[i, j] = total
        return new

    # --------------------------------------------------
    # protocol
    # --------------------------------------------------

    def __repr__(self):
        m = 0
        # find the fattest element
        for r in self.v:
            for c in r:
                l = len(str(c))
                if l > m:
                    m = l
        f = '%%%ds' % (m+1)
        s = '<matrix'
        for r in self.v:
            s += '\n'
            for c in r:
                s += (f % str(c))
        s += '>'
        return s
