from polynomial_library.bivariate_polynomials import BivariatePolynomial
from simultaneous_approximation_tools import *


def c0_predicate(function_list, box):
    """
    Evaluate the C0 predicate for a list of functions within a specified box.

    The C0 predicate is true if none of the functions' varieties (zeros) are contained within the box.
    If any function's variety is contained in the box, the C0 predicate is false.

    Args:
        function_list (list[BivariatePolynomial]): A list of bivariate functions to check.
        box (Box): The box in which to check if the variety of any function is contained.

    Returns:
        bool: True if none of the functions have a variety (contain a zero) within the box;
              False if at least one function's variety is contained in the box.
    """
    for function in function_list:
        # Check if the variety of the function is contained in the box
        if evaluate_bivariate_over_box(function, box).contains_zero():
            return False  # Return early if any function contains a zero
    return True  # C0 is true if no varieties are contained


def c1_predicate(function_list, box):
    """
    Check the C1 predicate for a list of bivariate polynomials within a given box.

    The C1 predicate ensures that the gradient (partial derivatives) of each function
    in the list is non-zero throughout the specified box. The predicate is false
    if the inner product (sum of squares of the partial derivatives) contains zero
    at any point in the box, indicating that the gradient is zero.

    Args:
        function_list (list[BivariatePolynomial]): A list of bivariate polynomials to check.
        box (Box): The box in which the C1 predicate is evaluated.

    Returns:
        bool: True if the C1 predicate holds (i.e., the gradient is non-zero throughout
              the box for all functions). False if the gradient is zero for any function
              in the box.
    """
    for function in function_list:
        # Evaluate the partial derivatives over the box once
        dx_evaluation = evaluate_bivariate_over_box(function.derivative(0), box)
        dy_evaluation = evaluate_bivariate_over_box(function.derivative(1), box)

        # Compute the inner product of the partial derivatives
        inner_product_evaluation = dx_evaluation * dx_evaluation + dy_evaluation * dy_evaluation

        # If the inner product contains zero, return False (C1 predicate fails)
        if inner_product_evaluation.contains_zero():
            return False
    return True


def c0_c1_predicate(function_list, box):
    c0_functions = []
    for function in function_list:
        c0_flag = c0_predicate([function], box)
        if c0_flag:
            c0_functions.append(function)
            if len(c0_functions) > 1:
                return False
    if len(c0_functions) == 1:
        return c1_predicate(c0_functions, box)
    return True


def c1_cross_predicate(function1, function2, box):
    dfdx_evaluation = evaluate_bivariate_over_box(function1.derivative(0), box)
    dfdy_evaluation = evaluate_bivariate_over_box(function1.derivative(1), box)
    dgdx_evaluation = evaluate_bivariate_over_box(function2.derivative(0), box)
    dgdy_evaluation = evaluate_bivariate_over_box(function2.derivative(1), box)
    cross_product_evaluation = dfdx_evaluation * dgdy_evaluation - dfdy_evaluation * dgdx_evaluation
    return not cross_product_evaluation.contains_zero()
