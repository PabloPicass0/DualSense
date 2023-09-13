"""
Sign 'B' is a tap with the straight hand while the thumb is folded up.
The touchscreen has difficulty detecting the whole area, but rather
detects only individual points which differ from time to time. Therefore,
a rectangle is defined into which the tap needs to fall.
"""
from typing import List

from recognition import timestamp_duration_valid

# Constants for the corners of the rectangle; y-values increases going down in graphical systems
RECT_TOP_LEFT = (155, 548.5)
RECT_BOTTOM_RIGHT = (955, 1020.5)


def locations_inside_rectangle(locations: List[List[float]]) -> bool:
    """
    Checks whether all touches are within the defined rectangle.

    :param locations: A list of locations. Each location is a list with two floats representing x and y coordinates
    of a touch point.
    :return: True if all points are inside the rectangle, False otherwise (if any point is outside).
    """
    # unpacks rectangle coordinates
    rect_x1, rect_y1 = RECT_TOP_LEFT
    rect_x2, rect_y2 = RECT_BOTTOM_RIGHT

    # iterates over all locations
    for location in locations:
        x, y = location
        # if any touch point is outside the rectangle, returns False
        if not (rect_x1 <= x <= rect_x2 and rect_y1 <= y <= rect_y2):
            return False

    # if no touch point was outside the rectangle, returns True
    return True


def is_sign_b(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    Checks whether a touch event is within the rectangle, the number of taps is below 20
    and the duration is not more than 3 seconds.

    :param timestamps: List of timestamps
    :param locations: List of locations where each location is a list of x and y coordinates
    :return: True if the gesture satisfies all three conditions, False otherwise
    """
    if len(timestamps) > 20:
        print("Too many touch points")
        return False

    if not timestamp_duration_valid('B', timestamps):
        print("Duration too long")
        return False

    if not locations_inside_rectangle(locations):
        print("Location not inside rectangle")
        return False

    return True
