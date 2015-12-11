__author__ = 'nsifniotis'

import math


class Polynomial:
    def __init__(self, input_matrix):
        self.coefficients = []
        (x, y) = input_matrix.size()
        for i in range(0, x):
            self.coefficients.append(input_matrix.get((i, 0)))

    def __repr__(self):
        """
        Returns a prettified string representing this polynomial object.
        :return:
        """
        output_string = ""
        for position in range(len(self.coefficients) - 1, -1, -1):
            if self.coefficients[position] != 0:
                sign = "+" if self.coefficients[position] > 0 else "-"
                coeff = math.fabs(self.coefficients[position])
                output_string += " " + sign + " " if output_string != "" else ""
                output_string += sign if output_string == "" and sign == "-" else ""

                output_string += Polynomial.if_int_get_int(coeff) if (coeff != 1 or position == 0) else ""
                if position == 1:
                    output_string += "x"
                elif position > 1:
                    output_string += "x^" + str(position)

        return output_string

    def solve(self, x_value):
        """
        Solves the polynomial for the given X value.

        :param x_value: The x value to solve for.
        :return: The corresponsing Y value.
        """
        next_point = 0
        for position in range(0, len(self.coefficients)):
            next_point += (self.coefficients[position] * int(math.pow(x_value, position)))
        return next_point

    @staticmethod
    def if_int_get_int(value):
        """
        Returns an integer if the value passed is a whole number, otherwise returns the value itself.

        :param value: THe original value.
        :return: The int or value
        """
        return str(int(value)) if (int(value) == value) else "{:.2f}".format(value)