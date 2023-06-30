"""
Sign 'A' is a tap with the fist on the hand of the recipient.
The touchscreen has difficulty detecting the whole area, but rather
detects only individual points. Therefore, a circle is defined within
which the tap needs to occur.
"""

# Circle template parameters for sign "A" in pixels
# Circle center x-coordinate
XC = 477.5
# Circle center y-coordinate
YC = 755.5
# Circle radius
R = 369.5

from typing import List


def timestamp_duration_valid(timestamps: List[float]) -> bool:
    """
    Checks whether the difference between the first and the last timestamp is larger than 3 seconds.

    :param timestamps: List of timestamps
    :return: True if the duration is less than or equal to 3 seconds, False otherwise
    """
    return timestamps[-1] - timestamps[0] <= 3


def locations_inside_circle(locations: List[List[float]]) -> bool:
    """
    Checks whether each location is within the defined circle.

    :param locations: List of locations where each location is a list of x and y coordinates
    :return: True if all the locations are inside the circle, False otherwise
    """
    for location in locations:
        x, y = location
        # Calculates square of distance between point and center and applying Pythagorean theorem
        if not ((x - XC) ** 2 + (y - YC) ** 2 <= R ** 2):
            return False
    return True


def is_sign_a(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    Checks whether a touch event is within the circle, the number of taps is below 10
    and the duration is not more than 3 seconds.

    :param timestamps: List of timestamps
    :param locations: List of locations where each location is a list of x and y coordinates
    :return: True if the gesture satisfies all three conditions, False otherwise
    """
    if len(timestamps) > 15:
        print("Too many touch points")
        return False

    if not timestamp_duration_valid(timestamps):
        print("Duration too long")
        return False

    if not locations_inside_circle(locations):
        print("Location not inside circle")
        return False

    return True
