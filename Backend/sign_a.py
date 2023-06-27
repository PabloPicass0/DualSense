"""
Sign 'A' is a tap with the fist on the hand of the recipient.
The touchscreen has difficulty detecting the whole area, but rather
detects only individual points. Therefore, a circle is defined within
which the tap needs to occur
"""


# Circle template for sign "A" in pixels
# Circle center x-coordinate
XC = 477.5
# Circle center y-coordinate
YC = 755.5
# Circle radius
R = 369.5


def is_touch_inside_circle(x: float, y: float) -> bool:
    """
    Checks whether a touch is within the circle
    """
    # Calculates if touch is within circle using Pythagorean Theorem
    return (x - XC)**2 + (y - YC)**2 <= R**2
