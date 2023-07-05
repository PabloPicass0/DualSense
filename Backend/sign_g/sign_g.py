"""
Sign 'G' is a single touch gesture, where the index draws a line on the upper side of the recipient's hand.
For recognition, the line is fitted into a Bézier curve, just like sign 'CH'.
"""
import json
import os
from typing import List

import numpy as np
from matplotlib import pyplot as plt

from extraction import extract_timestamps_and_locations
from sign_a import timestamp_duration_valid
from sign_ch.sign_ch import linear_bezier_curve, compare_sequences


def generate_linear_bezier(locations: List[List[float]]) -> np.ndarray:
    """
    Generates one linear Bézier curve given a list of touch locations.

    :param locations: The list of touch locations, where each location is a tuple of x and y coordinates.
    :return: One numpy array,representing a linear Bézier curve.
    """

    # control points: fits curves into linear Bézier curve
    P0_curve = np.array(locations[0])
    P1_curve = np.array(locations[-1])

    # assigns parameter values
    t = np.linspace(0, 1, num=100)

    # calculates points for curve1
    bezier = linear_bezier_curve(P0_curve, P1_curve, t=t)

    return bezier


def fit_bezier_for_g():
    """
    This function fits one linear Bézier curve to the given data and saves it as templates for later comparison.
    Used only once for saving templates of the sign.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_g.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_g = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_g)

    # generates Bezier curves
    bezier = generate_linear_bezier(locations)

    # saves the templates for future use
    file_path_b = os.path.join(current_dir, 'bezier_curve_template.npy')
    np.save(file_path_b, bezier)

    # plots curves
    plt.plot(bezier[:, 0], bezier[:, 1], color='blue')  # curve1 # plt.scatter([P0_curve1[0],

    plt.show()


def is_sign_g(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "G"
    according to a predefined template of the gesture.
    If the performed gesture deviates from the template by more than a certain threshold,
    the function returns False. Otherwise, it returns True.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """
    # checks if time frame is valid
    if not timestamp_duration_valid(timestamps):
        print("Duration too long")
        return False

    # creates Bézier curve representing the user-performed gesture
    user_curve = generate_linear_bezier(locations)

    # loads the template for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b = os.path.join(current_dir, 'bezier_curve_template.npy')
    bezier_curve_template = np.load(file_path_b)

    # calculates distance using DTW
    distance_template = compare_sequences(user_curve, bezier_curve_template)

    print(f"distance_template: {distance_template}")

    if distance_template > 1500.0:
        return False

    return True

# if __name__ == '__main__':
#     # already executed to save templates
#     fit_bezier_for_g()
