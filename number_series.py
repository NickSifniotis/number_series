__author__ = 'Nick Sifniotis'

from matrix import Matrix
import math
import sys


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


if len(sys.argv) == 1:
    print("Usage: python number_series.py number_1 number_2 ... number_N")
    exit(0)

args = sys.argv[1:]
test_values = []
for value in args:
    try:
        number = int(value)
        test_values.append(number)
    except ValueError:
        print("Error: " + value + " is not a number.")
        exit(0)

num_nums = len(test_values)
result_vector = vector(test_values)
working_matrix = Matrix((num_nums, num_nums))

for col in range(0, num_nums):
    for row in range(0, num_nums):
        working_matrix.set((row, col), math.pow(col + 1, row))

result = solve(working_matrix, result_vector)

output_string = ""
for position in range(num_nums - 1, -1, -1):
    if result.get((position, 0)) != 0:
        output_string += " + " if output_string != "" else ""
        output_string += "{:.2f}".format(result.get((position, 0)))
        if position == 1:
            output_string += "x"
        elif position > 1:
            output_string += "x^" + str(position)

print(output_string)
