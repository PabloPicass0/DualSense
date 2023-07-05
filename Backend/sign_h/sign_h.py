"""
Sign 'H' is a single touch gesture, where the thumb draws a line through the middle of the recipient's hand.
For recognition, the line is fitted into a Bézier curve, just like sign 'G'.
"""
import json
import os
from typing import List, Dict, Union

import numpy as np
from matplotlib import pyplot as plt

from extraction import extract_timestamps_and_locations
from sign_a import timestamp_duration_valid
from sign_ch.sign_ch import compare_sequences
from sign_g.sign_g import generate_linear_bezier


def fit_bezier_for_h():
    """
    This function fits one linear Bézier curve to the given data and saves it as templates for later comparison.
    Used only once for saving templates of the sign.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_h.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_h = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_h)

    # generates Bezier curves
    bezier = generate_linear_bezier(locations)

    # saves the templates for future use
    file_path_b = os.path.join(current_dir, 'bezier_curve_template.npy')
    np.save(file_path_b, bezier)

    # plots curves
    plt.plot(bezier[:, 0], bezier[:, 1], color='blue')  # curve1 # plt.scatter([P0_curve1[0],

    plt.show()


def is_sign_h(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "H"
    according to a predefined template of the gesture.
    If the performed gesture deviates from the template by more than a certain threshold,
    the function returns False. Otherwise, it returns True.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """
    # creates Bézier curve representing the user-performed gesture
    user_curve = generate_linear_bezier(locations)

    # loads the template for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b = os.path.join(current_dir, 'bezier_curve_template.npy')
    bezier_curve_template = np.load(file_path_b)

    # calculates distance using DTW
    distance_template = compare_sequences(user_curve, bezier_curve_template)

    # debugging
    print(f"distance_template: {distance_template}")

    # compares if distance to template is below threshold
    if distance_template > 2000.0:
        return False

    # checks if time frame is valid
    if not timestamp_duration_valid(timestamps):
        print("Duration too long")
        return False

    return True

# if __name__ == '__main__':
#     # already executed to save templates
#     fit_bezier_for_h()
