#!/usr/bin/env python

__author__ = 'Nick Sifniotis'

from Polynomial import Polynomial
from matrix import Matrix
import argparse
import math


class ANSIEscapeCodes(object):
    ESCAPE = '\033[%sm'
    ENDC = ESCAPE % '0'

    BOLD = '1;'
    FAINT = '2;' # Not widely supported
    ITALIC = '3;'
    UNDERLINE = '4;'
    SLOW_BLINK = '5;'
    FAST_BLINK = '6;' # Not widely supported

    COLORS = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
    }

    def decorate(self, format, msg):
        format_sequence = self.ESCAPE % format
        return format_sequence + msg + self.ENDC

    ### EXAMPLE USE ###

    def white_bold_underlined(self, msg):
        return self.decorate(self.BOLD + self.UNDERLINE + self.COLOR['white'], msg)


def identity(n=3):
    """
    Create a new identity matrix. Default size is 3 x 3.

    :param n: The size of the matrix to create.
    :return: The identity matrix object.
    """
    new = Matrix((n, n))
    for i in range(n):
        new[i, i] = 1
    return new


def vector(init):
    """
    Creates a matrix object of cardinality (n, 1) from the given list of numbers.

    :param init: A python list of values.
    :return: A matrix object initialised to the values in init.
    """
    if type(init) == type(1):
        return Matrix((init, 1))
    else:
        return Matrix([init])


def lu_decomposition(a):
    """
    Gaussian elimination of the matrix A.

    :param a: The matrix to reduce.
    :return: I really don't know.
    """
    a = a.copy()
    n = a.size()[0]
    u = identity(n)
    l = identity(n)
    for k in range(n):
        u[k, k] = a[k, k]
        for i in range(k + 1, n):
            l[k, i] = float(a[k, i]) / u[k, k]
            u[i, k] = a[i, k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[j, i] = a[j, i] - (l[k, i] * u[j, k])
    return l, u, range(n)


def lup_solve(l, u, p, b):
    """
    I don't know what this method does.

    :param l:
    :param u:
    :param p:
    :param b:
    :return:
    """
    n = l.size()[0]
    y = b.copy()
    # forward
    for i in range(n):
        total = b[p[i], 0]
        for j in range(i):
            total -= (l[j, i] * y[j, 0])
        y[i, 0] = total
    # backward
    x = vector(n)
    for i in range(n - 1, -1, -1):
        total = y[i, 0]
        for j in range(i + 1, n):
            total -= (u[j, i] * x[j, 0])
        x[i, 0] = total / u[i, i]
    return x


def solve(a, b):
    """
    Performs matrix reduction operations to solve the system of linear equations
    Ax = B

    :param a: The matrix A
    :param b: The solution vector B
    :return: The vector x that satisfies the equation Ax = B
    """
    l, u, p = lu_decomposition(a)
    return lup_solve(l, u, p, b)


# start the script by getting the number series from the command line.
parser = argparse.ArgumentParser()
parser.add_argument('test_values', nargs='+', help='The number series to process.', metavar='N')
results = parser.parse_args()
test_values = []
for string_num in vars(results)['test_values']:
    test_values.append(int(string_num))


num_nums = len(test_values)
result_vector = vector(test_values)
working_matrix = Matrix((num_nums, num_nums))

for col in range(0, num_nums):
    for row in range(0, num_nums):
        working_matrix.set((row, col), math.pow(col + 1, row))

result = Polynomial(solve(working_matrix, result_vector))


# output!
print("\033c")
formatter = ANSIEscapeCodes()


# display the original series.
print(formatter.decorate(formatter.COLORS['white'], "Input vector"))
print(formatter.decorate(formatter.COLORS['red'], str(test_values)))


# display the polynomial equation that this series satisfies
print()
print(formatter.decorate(formatter.COLORS['white'], "Polynomial equation satisfying the number series"))
print(formatter.decorate(formatter.COLORS['yellow'], str(result)))


# compute the next logical point along the series.
print()
print(formatter.decorate(formatter.COLORS['white'], "Next logical point along series"))
print(formatter.decorate(formatter.COLORS['yellow'], Polynomial.if_int_get_int(result.solve(num_nums + 1))))


# compute the 'triangle of differences'
print()
print(formatter.decorate(formatter.COLORS['white'], "Triangle of Differences"))
working_list = test_values
while len(working_list) > 1:
    print(formatter.decorate(formatter.COLORS['green'], str(working_list)))
    new_list = []
    for i in range(0, len(working_list) - 1):
        new_list.append(working_list[i + 1] - working_list[i])
    working_list = new_list
print(formatter.decorate(formatter.COLORS['green'], str(working_list)))

print()
print()