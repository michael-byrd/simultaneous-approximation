from interval_arithmetic_library.interval_arithmetic import Interval
import math


class Box:
    def __init__(self, x_int, y_int):
        self.x_interval = x_int
        self.y_interval = y_int
        self.sides = self.find_sides()
        self.vertex = []
        self.mark = False
        self.parent = None
        self.balanced = False  # Mark True if box was subdivided for balancing.
        self.children = []

    def __str__(self):
        return f"X: {self.x_interval}, Y: {self.y_interval}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        """
        Check if two Box objects are equal. Two boxes are considered equal if their x and y intervals are the same.

        :param other: The other Box object to compare with.
        :return: True if both boxes have the same x and y intervals, False otherwise.
        """
        return self.x_interval == other.x_interval and self.y_interval == other.y_interval

    def width(self):
        """
        Compute the width of the box.

        The width of the box is defined as the minimum of the widths of the x and y intervals.

        :return: The width of the box as a float. This is the smaller value between the width of the x interval
                 and the width of the y interval.
        """
        return min(self.x_interval.width(), self.y_interval.width())

    def diameter(self):
        """
        Compute the diameter of the box.

        :return: The Euclidean distance between the two opposite corners of the box.
        """
        return math.sqrt(self.x_interval.width() ** 2 + self.y_interval.width() ** 2)

    def find_sides(self):
        """
            Computes and returns the sides of the box based on the x and y intervals.

            The box is defined by its two intervals: x_interval (horizontal) and
            y_interval (vertical). The method calculates the four sides of the
            rectangular box by determining the coordinates of the vertices and
            connecting them in sequence.

            Returns:
                list: A list of four sides, where each side is represented as a
                tuple of two coordinates. Each coordinate is a 2-tuple representing
                the (x, y) position of a vertex.

                The sides are ordered as follows:
                1. Bottom side (right to left)
                2. Right side (top to bottom)
                3. Top side (left to right)
                4. Left side (bottom to top)
            """
        # Define the vertices of the box
        top_right = (self.x_interval.upper_bound, self.y_interval.upper_bound)
        bottom_right = (self.x_interval.upper_bound, self.y_interval.lower_bound)
        top_left = (self.x_interval.lower_bound, self.y_interval.upper_bound)
        bottom_left = (self.x_interval.lower_bound, self.y_interval.lower_bound)

        # Use the vertices to define the sides
        side_1 = [bottom_right, top_right]
        side_2 = [top_right, top_left]
        side_3 = [top_left, bottom_left]
        side_4 = [bottom_left, bottom_right]

        return [side_1, side_2, side_3, side_4]

    # TODO: What if a point lies on a corner of a box?
    def which_side(self, pt):
        """
        Determines which side of the box the given point lies on.

        Args:
            pt (tuple): A 2-tuple (x, y) representing the coordinates of the point.

        Returns:
            str: A string indicating the side of the box on which the point lies.
            Possible values:
                - "right_side"  : if the point lies on the right vertical side
                - "top_side"    : if the point lies on the top horizontal side
                - "left_side"   : if the point lies on the left vertical side
                - "bottom_side" : if the point lies on the bottom horizontal side
                - "not_on_side" : if the point does not lie on any side
        """
        if pt[0] == self.x_interval.upper_bound:  # Right side
            return "right_side"
        elif pt[1] == self.y_interval.upper_bound:  # Top side
            return "top_side"
        elif pt[0] == self.x_interval.lower_bound:  # Left side
            return "left_side"
        elif pt[1] == self.y_interval.lower_bound:  # Bottom side
            return "bottom_side"
        else:
            return "not_on_side"

    def midpoint(self):
        """
        Calculate the midpoint of the box.
        :return: A pair of numbers representing the midpoint of the box.
        """
        return self.x_interval.midpoint(), self.y_interval.midpoint()

    def contains_point(self, p):
        """
        Check if a given point is inside the box.

        :param p: A tuple representing the point to check (x, y).
        :return: True if the point is inside the box, False otherwise.
        """
        return self.x_interval.contains(p[0]) and self.y_interval.contains(p[1])

    def intersection(self, other_box):
        """
        Compute the intersection of two boxes. The intersection is defined by the overlapping region
        in both the x and y dimensions. If there is no overlap in either dimension, an empty box is returned.

        :param other_box: The other Box object to intersect with.
        :return: A new Box object representing the intersection of the two boxes. If there is no overlap,
                 the returned Box will have intervals with negative infinity to indicate no valid intersection.
        """

        x_interval_intersection = self.x_interval.intersection(other_box.x_interval)
        y_interval_intersection = self.y_interval.intersection(other_box.y_interval)

        if x_interval_intersection.width() >= 0 and y_interval_intersection.width() >= 0:
            return Box(x_interval_intersection, y_interval_intersection)
        else:
            return Box(Interval(-math.inf, -math.inf), Interval(-math.inf, -math.inf))

    def is_neighbor(self, other_box):
        """
        Determine if two boxes are neighbors (adjacent). Two boxes are neighbors if they share a side.

        Parameters:
            other_box (Box): The other box to check for adjacency.

        Returns:
            bool: True if the boxes are neighbors (i.e., share a side), False otherwise.
        """
        box_intersection = self.intersection(other_box)
        intersection_x_width = box_intersection.x_interval.width()
        intersection_y_width = box_intersection.y_interval.width()

        # Check if the boxes are neighbors:
        # one dimension must have width 0 (shared side), and the other must be positive
        return ((intersection_x_width == 0 and intersection_y_width > 0)
                or (intersection_y_width == 0 and intersection_x_width > 0))

    def find_neighbors(self, box_list):
        """
        Find all boxes in the provided list that are neighbors (adjacent) to the current box.

        :param box_list: A list of Box objects to check for adjacency.
        :return: A list of Box objects that are neighbors of the current box.
        """
        neighboring_boxes = [box for box in box_list if self.is_neighbor(box)]
        return neighboring_boxes

    def get_vertices(self):
        """
        Get the coordinates of the vertices of the box in clockwise order starting from the bottom-left corner.

        :return: A list of tuples, each representing the coordinates of a vertex of the box.
        """
        return [
            (self.x_interval.lower_bound, self.y_interval.lower_bound),
            (self.x_interval.upper_bound, self.y_interval.lower_bound),
            (self.x_interval.upper_bound, self.y_interval.upper_bound),
            (self.x_interval.lower_bound, self.y_interval.upper_bound)
        ]

    def subdivide(self):
        """
        Subdivide the current box into four smaller boxes.

        This method splits the current box into four sub-boxes by dividing both the
        x and y intervals in half. The resulting boxes inherit the class type of the
        current box (i.e., if called from a `PVBox`, it returns `PVBox` instances).

        Each new box is assigned the current box as its parent, and the current box
        will have a `children` attribute that stores the four sub-boxes.

        Returns:
            list[Box]: A list of four sub-boxes, each of the same type as the calling class
                       (either `Box` or `PVBox`).
        """
        x1 = Interval(self.x_interval.lower_bound, (self.x_interval.lower_bound + self.x_interval.upper_bound) / 2)
        x2 = Interval((self.x_interval.lower_bound + self.x_interval.upper_bound) / 2, self.x_interval.upper_bound)

        y1 = Interval(self.y_interval.lower_bound, (self.y_interval.lower_bound + self.y_interval.upper_bound) / 2)
        y2 = Interval((self.y_interval.lower_bound + self.y_interval.upper_bound) / 2, self.y_interval.upper_bound)

        # Use type(self) to dynamically determine if it's Box or PVBox
        box1 = type(self)(x2, y2)
        box2 = type(self)(x1, y2)
        box3 = type(self)(x1, y1)
        box4 = type(self)(x2, y1)

        # Set parent relationships
        box1.parent = self
        box2.parent = self
        box3.parent = self
        box4.parent = self

        # Set children for the current box
        self.children = [box1, box2, box3, box4]

        return [box1, box2, box3, box4]
