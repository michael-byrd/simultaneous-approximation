import unittest
from interval_arithmetic_library import Interval

class TestIntervalArithmetic(unittest.TestCase):

    def test_constructing_interval(self):
        interval1 = Interval(1, 2)
        self.assertEqual(interval1.lower_bound, 1)
        self.assertEqual(interval1.upper_bound, 2)
        interval2 = Interval(-1, 1)
        self.assertEqual(interval2.lower_bound, -1)
        self.assertEqual(interval2.upper_bound, 1)
        interval3 = Interval(-1, -2)
        self.assertEqual(interval3.lower_bound, -2)
        self.assertEqual(interval3.upper_bound, -1)
        interval4 = Interval(1)
        self.assertEqual(interval4.lower_bound, -1)
        self.assertEqual(interval4.upper_bound, 1)

    def test_add_two_positive_intervals(self):
        interval1 = Interval(1, 2)
        interval2 = Interval(3, 4)
        result = interval1 + interval2
        expected = Interval(4, 6)
        self.assertEqual(result, expected)

    def test_add_interval_and_number(self):
        interval1 = Interval(1, 2)
        result1 = interval1 + 3
        expected1 = Interval(4, 5)
        result2 = 3 + interval1
        expected2 = Interval(4, 5)
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_add_positive_and_negative_interval(self):
        interval1 = Interval(1, 2)
        interval2 = Interval(-1, 1)
        interval3 = Interval(-3, -2)
        result1 = interval1 + interval2
        expected1 = Interval(0, 3)
        result2 = interval1 + interval3
        expected2 = Interval(-2, 0)
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_subtract_two_positive_intervals(self):
        interval1 = Interval(1, 2)
        interval2 = Interval(3, 4)
        result1 = interval1 - interval2
        expected1 = Interval(-3, -1)
        result2 = interval2 - interval1
        expected2 = Interval(1, 3)
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_subtract_interval_and_number(self):
        interval1 = Interval(1, 2)
        result1 = interval1 - 3
        expected1 = Interval(-2, -1)
        result2 = 3 - interval1
        expected2 = Interval(1, 2)
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_subtract_positive_and_negative_intervals(self):
        interval1 = Interval(1, 2)
        interval2 = Interval(-1, 1)
        interval3 = Interval(-3, -2)
        result1 = interval1 - interval2
        expected1 = Interval(0, 3)
        result2 = interval1 - interval3
        expected2 = Interval(3, 5)
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_multiply_two_positive_intervals(self):
        interval1 = Interval(1, 2)
        interval2 = Interval(3, 4)
        interval3 = Interval(0, 1)
        result1 = interval1 * interval2
        expected1 = Interval(3, 8)
        result2 = interval2 * interval1
        expected2 = Interval(3, 8)
        result3 = interval1 * interval3
        expected3 = Interval(0, 2)
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)

    def test_multiply_interval_and_number(self):
        interval1 = Interval(1, 2)
        result1 = interval1 * 3
        expected1 = Interval(3, 6)
        result2 = 3 * interval1
        expected2 = Interval(3, 6)
        result3 = -3 * interval1
        expected3 = Interval(-6, -3)
        result4 = interval1 * -3
        expected4 = Interval(-6, -3)
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)
        self.assertEqual(result4, expected4)

    def test_multiply_positive_and_negative_intervals(self):
        interval1 = Interval(1, 2)
        interval2 = Interval(-1, 1)
        interval3 = Interval(-3, -2)
        result1 = interval1 * interval2
        expected1 = Interval(-2, 2)
        result2 = interval1 * interval3
        expected2 = Interval(-6, -2)
        result3 = interval3 * interval3
        expected3 = Interval(4, 9)
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)

    # Add division later.

    def test_positive_odd_power(self):
        interval1 = Interval(2, 3)
        interval2 = Interval(-2, 3)
        result1 = interval1 ** 3
        expected1 = Interval(8, 27)
        result2 = interval2 ** 3
        expected2 = Interval(-8, 27)
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_positive_even_power(self):
        interval1 = Interval(2, 3)
        interval2 = Interval(-2, 3)
        result1 = interval1 ** 2
        expected1 = Interval(4, 9)
        result2 = interval2 ** 2
        expected2 = Interval(0, 9)
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_negative_odd_power(self):
        interval1 = Interval(2, 3)
        interval2 = Interval(-2, 3)
        result1 = interval1 ** -3
        expected1 = Interval(1/27, 1/8)
        self.assertEqual(result1, expected1)
        with self.assertRaises(ZeroDivisionError):
            interval2 ** -3

    def test_negative_even_power(self):
        interval1 = Interval(2, 3)
        interval2 = Interval(-2, 3)
        result1 = interval1 ** -2
        expected1 = Interval(1/9, 1/4)
        self.assertEqual(result1, expected1)
        with self.assertRaises(ZeroDivisionError):
            interval2 ** -2

    def test_noninteger_power(self):
        interval1 = Interval(2, 3)
        with self.assertRaises(NotImplementedError):
            interval1 ** 1.5
        with self.assertRaises(NotImplementedError):
            interval1 ** Interval(2, 3)



