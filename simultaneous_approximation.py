import math

from polynomial_library.bivariate_polynomials import *
from interval_arithmetic_library.interval_arithmetic import Interval
from interval_arithmetic_library.box_arithmetic import Box
from simultaneous_approximation_predicates import *
from simultaneous_approximation_tools import *
# from piecewise_edges import *

def subdivision_without_c1_cross(function_list, initial_box):
    subdivision_queue = [initial_box]
    c0_boxes, c1_boxes = [], []

    while subdivision_queue:
        current_box = subdivision_queue.pop(0)
        if c0_predicate(function_list, current_box):
            c0_boxes.append(current_box)
            current_box.C0_predicate = True
        elif c0_c1_predicate(function_list, current_box):
            c1_boxes.append(current_box)
            current_box.C0_predicate = False
            current_box.C1_predicate = True
        elif c1_predicate(function_list, current_box):
            c1_boxes.append(current_box)
            current_box.C0_predicate = False
            current_box.C1_predicate = True
            # current_box.C1Prime = True
        else:
            subdivision_queue.extend(current_box.subdivide())
    return c0_boxes, c1_boxes


def subdivision_with_c1_cross(function_list, initial_box):
    subdivision_queue = [initial_box]
    c0_boxes, c1_boxes = [], []

    while subdivision_queue:
        current_box = subdivision_queue.pop(0)

        not_c0_functions = set()
        not_c1_functions = set()
        for i, function in enumerate(function_list):
            if not c0_predicate([function], current_box):
                not_c0_functions.add(i)
            if not c1_predicate([function], current_box):
                not_c1_functions.add(i)

        # Box has more than 2 curves
        if len(not_c0_functions) > 2:
            subdivision_queue.extend(current_box.subdivide())
            continue

        # Box has exactly 2 curves
        if len(not_c0_functions) == 2:
            if not_c0_functions & not_c1_functions:
                subdivision_queue.extend(current_box.subdivide())
                continue

            both_curves = [function_list[i] for i in not_c0_functions]
            w = 6.5
            extended_x_interval = Interval(current_box.x_interval.lower_bound - w*current_box.width(),
                                           current_box.x_interval.upper_bound + w*current_box.width())
            extended_y_interval = Interval(current_box.y_interval.lower_bound - w*current_box.width(),
                                           current_box.y_interval.upper_bound + w*current_box.width())
            two_neighborhood_current_box = PVBox(extended_x_interval, extended_y_interval)
            if c1_cross_predicate(*both_curves, two_neighborhood_current_box):
                c1_boxes.append(current_box)
                current_box.C0_predicate = False
                current_box.C1_predicate = True
                current_box.C1Prime = True
            else:
                subdivision_queue.extend(current_box.subdivide())
            continue

        # Box has exactly 1 curve
        if len(not_c0_functions) == 1:
            if not_c0_functions & not_c1_functions:
                subdivision_queue.extend(current_box.subdivide())
            else:
                c1_boxes.append(current_box)
                current_box.C0_predicate = False
                current_box.C1_predicate = True
            continue

        # Box has no curves
        c0_boxes.append(current_box)
        current_box.C0_predicate = True

    return c0_boxes, c1_boxes
