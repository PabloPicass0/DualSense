"""
Sign 'CH' is a multi-touch gesture, where the index and middle-finger draw a line, each, on the palm of the
recipient. For recognition, each line is fitted into a Bezier curve, so that user-performed gestures can be
compared to the curve to determine accuracy.
"""
import json
import math
import matplotlib.pyplot as plt

from extraction import extract_timestamps_and_locations


def distance(point1, point2):
    """
        Add docstring
        :return:
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def split_touch_locations(locations):
    """
        Add docstring
        :return:
    """
    curve1 = []
    curve2 = []

    # Start by putting the first point in curve1
    curve1.append(locations[0])
    for i in range(1, len(locations)):
        if distance(locations[i], curve1[-1]) <= 10:
            curve1.append(locations[i])
        else:
            curve2.append(locations[i])

    return curve1, curve2


def fit_bezier_ch():
    """
    Add docstring
    :return:
    """
    # opens and loads the JSON file
    with open('data_ch.json') as file:
        data_ch = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_ch)
    curve1, curve2 = split_touch_locations(locations)

    curve1_x, curve1_y = zip(*curve1)  # separate x and y coordinates for curve1
    curve2_x, curve2_y = zip(*curve2)  # separate x and y coordinates for curve2

    plt.figure(figsize=(10, 10))
    plt.plot(curve1_x, curve1_y, label='Curve 1')
    plt.plot(curve2_x, curve2_y, label='Curve 2')
    plt.legend()
    plt.show()

    # splits touch locations into individual curves

    # fits curves into Bezier curves

    # safes template
    pass


def is_sign_ch():
    """
    Add docstring
    :return:
    """
    # checks if time frame is valid

    # splits location points into respective curves

    # compares to template curves
    pass


if __name__ == '__main__':
    fit_bezier_ch()
