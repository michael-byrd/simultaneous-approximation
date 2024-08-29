from bivariate_polynomials import BivariatePolynomial
from sympy import *
import math


def cross_product_polynomial_gradients(polynomial1: BivariatePolynomial,
                                       polynomial2: BivariatePolynomial) -> BivariatePolynomial:
    """
    Computes the cross product of the gradients of two bivariate polynomials.
    :param polynomial1: The first bivariate polynomial
    :param polynomial2: The second bivariate polynomial
    :return: The cross product of the gradients of the two polynomials
    """
    gradient1 = polynomial1.gradient()
    gradient2 = polynomial2.gradient()

    cross_product = gradient1[0] * gradient2[1] - gradient1[1] * gradient2[0]
    return cross_product


def sympy_to_bivariate_polynomial(sympy_poly):
    """
    Converts a sympy polynomial to a BivariatePolynomial object.
    :param sympy_poly: The sympy polynomial to convert
    :return: A BivariatePolynomial object representing the sympy polynomial
    """
    coefficients = {}
    for term in sympy_poly.as_dict().items():
        monomial, coefficient = term
        x_power, y_power = monomial[0], monomial[1]
        coefficients[(x_power, y_power)] = coefficient
    return BivariatePolynomial(coefficients)


def bivariate_polynomial_to_sympy(bivariate_poly):
    """
    Converts a BivariatePolynomial object to a sympy polynomial.
    :param bivariate_poly: The BivariatePolynomial object to convert
    :return: A sympy polynomial representing the BivariatePolynomial object
    """
    sympy_poly = 0
    for (x_power, y_power), coefficient in bivariate_poly.coefficients.items():
        sympy_poly += coefficient * symbols('x') ** x_power * symbols('y') ** y_power
    return Poly(sympy_poly, symbols('x'), symbols('y'), symbols('z'))


def weyl_inner_product(poly1, poly2):
    """
    Computes the Weyl inner product of two bivariate polynomials.
    :param poly1: The first bivariate polynomial
    :param poly2: The second bivariate polynomial
    :return: The Weyl inner product of the two polynomials
    """
    degree = poly1.total_degree()

    homogenized_poly1 = poly1.homogenize(symbols('z'))
    homogenized_poly2 = poly2.homogenize(symbols('z'))

    weyl_inner_product_value = 0
    for term in homogenized_poly1.terms():
        exponents, coefficient = term[0], term[1]
        monomial_coeff = ((math.factorial(exponents[0]) * math.factorial(exponents[1]) * math.factorial(exponents[2]))
                          / math.factorial(degree))
        weyl_inner_product_value += monomial_coeff * coefficient ** 2

    return weyl_inner_product_value


u, v, x, y, z = symbols('u v x y z')
f = Poly(2 * x ** 2 + 3 * x * y ** 5 + 4 * y ** 2, x, y, z)
g = Poly(5 * x ** 3 + 2 * x ** 2 * y + 3 * y ** 2, x, y, z)

print(f, g)

bivar_f = sympy_to_bivariate_polynomial(f)
bivar_g = sympy_to_bivariate_polynomial(g)

print(bivar_f.gradient(), bivar_g.gradient())

cross_p = cross_product_polynomial_gradients(bivar_f, bivar_g)

print(cross_p)

sympy_cross_p = bivariate_polynomial_to_sympy(cross_p)

homogenized_f = f.homogenize(z)
homogenized_g = g.homogenize(z)
homogenized_cross_p = sympy_cross_p.homogenize(z)

pprint(homogenized_cross_p.as_expr())

weyl_p = weyl_inner_product(homogenized_cross_p, homogenized_cross_p)
weyl_f = weyl_inner_product(homogenized_f, homogenized_f)
weyl_g = weyl_inner_product(homogenized_g, homogenized_g)

# Print all three Weyl inner products with labels
print(f"Weyl Inner Product of f: {weyl_f}")
print(f"Weyl Inner Product of g: {weyl_g}")
print(f"Weyl Inner Product of cross_p: {weyl_p}")
