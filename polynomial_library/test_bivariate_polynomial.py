import unittest
from bivariate_polynomials import BivariatePolynomial


class TestBivariatePolynomials(unittest.TestCase):

    def test_constructing_polynomial(self):
        polynomial1 = BivariatePolynomial([1, 2, 3, 4])
        self.assertEqual(polynomial1.coefficients,
                         {(0, 0): 1, (1, 0): 2, (0, 1): 3, (2, 0): 4})

    def test_reduce(self):
        self.assertEqual((BivariatePolynomial([1, 2, 3, 4, 5]) - BivariatePolynomial([1, 2, 3, 4])).coefficients,
                         {(1, 1): 5})

    def test_print(self):
        pass
        # polynomial1 = BivariatePolynomial([1, -2, 3, -4])
        # print(polynomial1)

    def test_derivative(self):
        self.assertEqual(BivariatePolynomial([1, 2, 3, 4]).derivative(0).coefficients,
                         {(0, 0): 2, (1, 0): 8})
        self.assertEqual(BivariatePolynomial([1, 2, 3, 4]).derivative(1).coefficients,
                         {(0, 0): 3})
        self.assertEqual(BivariatePolynomial([0, 0, 0, 0, 0, 3, 2]).derivative(0).coefficients, {(2, 0): 6})
        self.assertEqual(BivariatePolynomial([0, 0, 0, 0, 0, 3, 2]).derivative(1).coefficients, {(0, 1): 6})
        self.assertEqual(BivariatePolynomial([1]).derivative(0).coefficients, {})
        self.assertEqual(BivariatePolynomial([1]).derivative(1).coefficients, {})
        self.assertEqual(BivariatePolynomial({(2, 3): 2, (3, 2): 5}).derivative(0).coefficients,
                         {(1, 3): 4, (2, 2): 15})

    def test_add(self):
        zero_polynomial = BivariatePolynomial([])
        summand_1 = BivariatePolynomial([1, 2, 3])
        summand_2 = BivariatePolynomial([-1, -2, -3])
        summand_3 = BivariatePolynomial([1, 2, 3, 4])
        self.assertEqual(summand_1 + summand_2, zero_polynomial)
        self.assertEqual(summand_1 + zero_polynomial, summand_1)
        self.assertEqual(zero_polynomial + summand_1, summand_1)
        self.assertEqual(summand_1 + summand_1, BivariatePolynomial([2, 4, 6]))
        self.assertEqual(summand_1 + summand_3, BivariatePolynomial([2, 4, 6, 4]))

