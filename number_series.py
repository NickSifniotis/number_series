__author__ = 'user'

from matrix import solve, vector, matrix
import math

test_values = [4, 8, 16, 32, 955]

num_nums = len(test_values)
result_vector = vector(test_values)
working_matrix = matrix((num_nums, num_nums))

for i in range(0, num_nums):
    for j in range(0, num_nums):
        working_matrix.set((j, i), math.pow(i + 1, j + 1))

result = solve(working_matrix, result_vector, 0)

output_string = ""
for i in range(num_nums - 1, -1, -1):
    if result.get((i, 0)) != 0:
        output_string += " + " if output_string != "" else ""
        output_string += "{:.2f}".format(result.get((i, 0))) + "x^" + str(i)

print(output_string)
