from polynomial_library.bivariate_polynomials import *
from interval_arithmetic_library.box_arithmetic import Box
from interval_arithmetic_library.interval_arithmetic import Interval

class PVBox(Box):
    def __init__(self, x_int, y_int):
        super().__init__(x_int, y_int)



def evaluate_bivariate_over_box(function, box):
    """
    Evaluate a bivariate polynomial function over a box using interval arithmetic.
    This function maps I x J -> K, where I, J, and K are intervals over the reals.

    Parameters:
        function (Polynomial): The bivariate polynomial function to evaluate.
        box (Box): The box object, with x_interval and y_interval, over which to evaluate the function.

    Returns:
        Interval: The resulting interval of the polynomial evaluation.
    """

    midpoint = box.midpoint()  # Assuming box.midpoint() returns a tuple (mid_x, mid_y)
    result_interval = Interval(0, 0)
    max_degree = function.deg  # Assuming function.deg gives the maximum degree of the polynomial

    # Precompute factorials to avoid recalculating inside the loop
    factorials = {i: math.factorial(i) for i in range(max_degree + 1)}

    for x_order in range(max_degree + 1):
        for y_order in range(max_degree + 1):
            if x_order + y_order > 0:
                # Compute the mixed derivative component
                derivative_component = function.derivative(0, x_order).derivative(1, y_order)

                # Evaluate the current summand using the interval arithmetic
                current_summand = (derivative_component.eval(midpoint)
                                   * (box.x_interval - midpoint[0]) ** x_order
                                   * (box.y_interval - midpoint[1]) ** y_order
                                   * (1 / factorials[x_order])
                                   * (1 / factorials[y_order]))

                result_interval += current_summand

    # Add the function value at the midpoint (the zero-order term)
    result_interval += function.eval(midpoint)

    return result_interval


def is_boundary_box(bounding_box, sub_box):
    """
    Checks if a sub_box is a boundary box, meaning it shares at least one edge
    with the bounding_box.

    Parameters:
        bounding_box (Box): The starting box at the beginning of the PV algorithm.
        sub_box (Box): A box contained within the bounding_box.

    Returns:
        bool: True if the sub_box lies on the boundary of the bounding_box, False otherwise.
    """
    # Check if the sub_box shares an edge with the bounding_box
    return (
            sub_box.x_interval.lower_bound == bounding_box.x_interval.lower_bound or
            sub_box.x_interval.upper_bound == bounding_box.x_interval.upper_bound or
            sub_box.y_interval.lower_bound == bounding_box.y_interval.lower_bound or
            sub_box.y_interval.upper_bound == bounding_box.y_interval.upper_bound
    )


def find_boundary_sides(bounding_box, sub_box):
    """
    Determine which sides of the sub_box are shared with the bounding_box.

    Parameters:
        bounding_box (Box): The bounding box at the beginning of the PV algorithm.
        sub_box (Box): A box that is contained within the bounding_box.

    Returns:
        list of str: A list of strings representing each side of the bounding_box
                     that the sub_box shares. Sides are labeled as "right_side",
                     "top_side", "left_side", and "bottom_side", rotating
                     counter-clockwise starting from the right side.
    """
    side_index = []

    if sub_box.x_interval.upper_bound == bounding_box.x_interval.upper_bound:
        side_index.append("right_side")
    if sub_box.y_interval.upper_bound == bounding_box.y_interval.upper_bound:
        side_index.append("top_side")
    if sub_box.x_interval.lower_bound == bounding_box.x_interval.lower_bound:
        side_index.append("left_side")
    if sub_box.y_interval.lower_bound == bounding_box.y_interval.lower_bound:
        side_index.append("bottom_side")

    return side_index


def detect_sign_change(function, point1, point2):
    """
    Determine if a function changes sign along the edge defined by two points.

    Parameters:
        function (Callable): The function being tested for a sign change.
        point1 (tuple or list): The first point (x, y) of the edge.
        point2 (tuple or list): The second point (x, y) of the edge.

    Returns:
        bool: True if the function changes sign between point1 and point2, False otherwise.
    """
    function_value1 = function.eval(point1)
    function_value2 = function.eval(point2)

    # Replace zero function values with a positive value (slight perturbation)
    if function_value1 == 0:
        function_value1 = 1
    if function_value2 == 0:
        function_value2 = 1

    # Check for a sign change
    return function_value1 * function_value2 < 0


def find_neighbors(current_box, box_list):
    neighbor_list = []
    for other_box in box_list:
        if current_box.is_neighbor(other_box):
            neighbor_list.append(other_box)
    return neighbor_list

exit()

# Test find_neighbors

# Define the intervals for the boxes
x1 = Interval(0, 1)
x2 = Interval(1, 2)
y1 = Interval(0, 1)

print(x1)



box1 = Box(x1, y1)
box2 = Box(x2, y1)

print(find_neighbors(box1, [box1, box2]))
