# Author: Michael Byrd
# Date: 2024

import math


class Interval:
    def __init__(self, lower, upper=None):
        """ Form an interval object.

        :param lower: Lower bound of the interval.
        :param upper: Upper bound of the interval.
        :return: None

        If only one bound is provided, say c, then
        the interval [-c, c] is formed.
        """

        self.lower_bound = -abs(lower) if upper is None else min(lower, upper)
        self.upper_bound = abs(lower) if upper is None else max(lower, upper)

    def __str__(self):
        """ Return a string representation of the interval. """
        return f"[{self.lower_bound}, {self.upper_bound}]"

    def __eq__(self, other):
        """ Check if two intervals are equal. """
        return self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound

    def __add__(self, other):
        """ Add two intervals together or add an interval and a number.

        :param other: Either an Interval object or a number.
        :return: Interval object representing the sum of the two intervals.
        """

        if isinstance(other, Interval):
            return Interval(self.lower_bound + other.lower_bound, self.upper_bound + other.upper_bound)
        else:
            return Interval(self.lower_bound + other, self.upper_bound + other)

    def __radd__(self, other):
        """ Add two intervals together or add an interval and a number.

        :param other: Either an Interval object or a number.
        :return: Interval object representing the sum of the two intervals.
        """

        if isinstance(other, Interval):
            return Interval(other.lower_bound + self.lower_bound, other.upper_bound + self.upper_bound)
        else:
            return Interval(other + self.lower_bound, other + self.upper_bound)

    def __sub__(self, other):
        """ Subtract two intervals or subtract an interval and a number.

        :param other: Either an Interval object or a number.
        :return: Interval object representing the difference of the two intervals.
        """

        if isinstance(other, Interval):
            return Interval(self.lower_bound - other.upper_bound, self.upper_bound - other.lower_bound)
        else:
            return Interval(self.lower_bound - other, self.upper_bound - other)

    def __rsub__(self, other):
        """ Subtract two intervals or subtract an interval and a number.

                :param other: Either an Interval object or a number.
                :return: Interval object representing the difference of the two intervals.
        """

        if isinstance(other, Interval):
            return Interval(other.lower_bound - self.upper_bound, other.upper_bound - self.lower_bound)
        else:
            return Interval(other - self.upper_bound, other - self.lower_bound)

    def __mul__(self, other):
        """ Multiply two intervals together or multiply an interval and a number.

        :param other: Either an Interval object or a number.
        :return: Interval object representing the product of the two intervals.
        """

        if isinstance(other, Interval):
            # Calculate all possible products of the bounds from both intervals
            products = [
                self.lower_bound * other.lower_bound,
                self.lower_bound * other.upper_bound,
                self.upper_bound * other.lower_bound,
                self.upper_bound * other.upper_bound
            ]
            # Return a new Interval with the minimum and maximum of the products
            return Interval(min(products), max(products))
        else:
            low = min(self.lower_bound * other, self.upper_bound * other)
            up = max(self.lower_bound * other, self.upper_bound * other)
            return Interval(low, up)

    __rmul__ = __mul__

    def __truediv__(self, other):
        """
        Perform true division between two intervals or between an interval and a scalar.

        :param other: Either an Interval object or a number (int or float).
        :return: A new Interval representing the result of the division.
        :raises ZeroDivisionError: If attempting to divide by an interval containing zero, or by zero itself.
        :raises TypeError: If 'other' is not an Interval or a number.
        """
        if isinstance(other, Interval):
            if other.contains_zero():
                raise ZeroDivisionError("Division by an interval containing zero is undefined.")
            # Create an interval that represents the reciprocal of the divisor interval
            reciprocal = Interval(1 / other.upper_bound, 1 / other.lower_bound)
            return self * reciprocal
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero is undefined.")
            # Multiply by the reciprocal of the scalar
            return self * (1 / other)
        else:
            raise TypeError(f"Unsupported operand type(s) for division: 'Interval' and '{type(other).__name__}'")

    def __rtruediv__(self, other):
        return "TODO: Not yet implemented"

    def contains_zero(self):
        """
        Check if the interval contains zero.
        :return: True if the interval contains zero, False otherwise.
        """
        return self.lower_bound <= 0 <= self.upper_bound

    def width(self):
        """
        Calculate the width of the interval.
        :return: The width of the interval as a float.
        """
        value = self.upper_bound - self.lower_bound
        if self.lower_bound == -math.inf and self.upper_bound == -math.inf:
            return -1
        if math.isnan(value):
            return -1
        return value

    def midpoint(self):
        """
        Calculate the midpoint of the interval.
        :return: The midpoint of the interval as a float.
        """
        return (self.lower_bound + self.upper_bound) / 2

    def contains(self, other):
        """
        Check if the interval contains another interval or a scalar value.
        :param other: An Interval object or a scalar value.
        :return: True if the interval contains the other interval or scalar, False otherwise.
        """
        if isinstance(other, Interval):
            return self.lower_bound <= other.lower_bound and self.upper_bound >= other.upper_bound
        else:
            return self.lower_bound <= other <= self.upper_bound

    def __abs__(self):
        """
        Calculate the absolute value of the interval.
        :return: A new Interval representing the absolute value of the original interval.
        """
        abs_lower = abs(self.lower_bound)
        abs_upper = abs(self.upper_bound)
        if self.contains_zero():
            return Interval(0, max(abs_lower, abs_upper))
        else:
            return Interval(min(abs_lower, abs_upper), max(abs_lower, abs_upper))

    # Unsure if I want to remove the non-magic method version of this
    def __contains__(self, other):
        return self.contains(other)

    def __pow__(self, other):
        """
        Calculate the power of the interval to the given exponent.
        :param other: The exponent to raise the interval to.
        :return: A new Interval representing the result of the power operation.
        """
        if isinstance(other, Interval):
            raise NotImplementedError("Exponentiation with an interval as the exponent is not supported.")
        if not isinstance(other, int):
            raise NotImplementedError("Exponentiation with a non-integer exponent is not supported.")
        absolute_interval = abs(self)
        if other == 0:
            return Interval(1)  # Check this
        elif other > 0:
            if other % 2 == 0:
                return Interval(absolute_interval.lower_bound ** other, absolute_interval.upper_bound ** other)
            else:
                return Interval(self.lower_bound ** other, self.upper_bound ** other)
        else:
            if self.contains_zero():
                raise ZeroDivisionError("Interval raised to a negative power contains zero.")
            if other % 2 == 0:
                return Interval(absolute_interval.upper_bound ** other, absolute_interval.lower_bound ** other)
            else:
                return Interval(self.upper_bound ** other, self.lower_bound ** other)

    def root(self, n):
        """
        Calculate the n-th root of the interval.
        :param n: The index of the root to take.
        :return: An Interval object representing the n-th root of the original interval.
        """
        if n == 0:
            raise ValueError("Cannot take the 0-th root of an interval.")
        if n % 2 == 0 and self.lower_bound < 0:
            raise ValueError("Cannot take an even root of an interval containing negative numbers.")

        lower_root = self.lower_bound ** (1.0 / n) if self.lower_bound >= 0 else -(-self.lower_bound) ** (1.0 / n)
        upper_root = self.upper_bound ** (1.0 / n) if self.upper_bound >= 0 else -(-self.upper_bound) ** (1.0 / n)
        return Interval(lower_root, upper_root)


    def intersection(self, other):
        """
        Compute the intersection of two intervals.
        :param other: The other interval to intersect with.
        :return: An Interval object representing the intersection of the two intervals.
        """
        if other.lower_bound > self.upper_bound or self.lower_bound > other.upper_bound:
            return Interval(-math.inf, -math.inf)
        else:
            return Interval(max(self.lower_bound, other.lower_bound), min(self.upper_bound, other.upper_bound))

