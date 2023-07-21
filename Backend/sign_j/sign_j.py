import json
import os
from typing import List

import numpy as np
from matplotlib import pyplot as plt

from extraction import extract_timestamps_and_locations

from parameterisation import return_cubic_bezier
from recognition import compare_sequences
from sign_a.sign_a import timestamp_duration_valid


def fit_bezier_for_j():
    """
    This function fits a cubic Bézier curve to the given data and saves it as a template for later comparison.
    Used only once for saving templates of the sign.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_j.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_j = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_j)

    # generates cubic bezier curve
    curve_points = return_cubic_bezier(locations)

    # converts list of tuples to numpy array
    curve_points_np = np.array(curve_points)

    # saves the template for future use
    file_path_b = os.path.join(current_dir, 'bezier_curve_template.npy')
    np.save(file_path_b, curve_points_np)

    # plots curves
    plt.plot(curve_points_np[:, 0], curve_points_np[:, 1], color='blue')

    plt.show()


def is_sign_j(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "J"
    according to a predefined template of the gesture.
    If the performed gesture deviates from the template by more than a certain threshold,
    the function returns False. Otherwise, it returns True.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """
    # creates cubic Bézier curve representing the user-performed gesture
    curve_points_user = return_cubic_bezier(locations)

    # loads the template for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b = os.path.join(current_dir, 'bezier_curve_template.npy')
    bezier_curve_template = np.load(file_path_b)

    # converts list of numpy arrays to a single 2D numpy array
    curve_points_user = np.vstack(curve_points_user)
    bezier_curve_template = np.vstack(bezier_curve_template)

    # calculates distance using DTW
    distance_template = compare_sequences(curve_points_user, bezier_curve_template)

    # debugging
    print(f"distance_template: {distance_template}")

    # compares if distance to template is below threshold
    if distance_template > 3000.0:
        return False

    # checks if time frame is valid
    if not timestamp_duration_valid('J', timestamps):
        print("Duration too long")
        return False

    return True

# # Code below already executed to fit template
# if __name__ == '__main__':
#     fit_bezier_for_j()
