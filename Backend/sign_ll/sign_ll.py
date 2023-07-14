import json
import os
from typing import List, Tuple

import numpy as np
from matplotlib import pyplot as plt

from extraction import extract_timestamps_and_locations
from sign_ch.sign_ch import split_touch_locations
from sign_j.sign_j import return_cubic_bezier


# generates Bezier curves
# generates Bezier curves
def generate_two_cubic_beziers(locations: List[List[float]]) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Generates two cubic Bézier curves given a list of touch locations.

    :param locations: The list of touch locations, where each location is a tuple of x and y coordinates.
    :return: Two numpy arrays, each representing a cubic Bézier curve.
    """

    # splits touch locations into individual curves
    curve1, curve2 = split_touch_locations(locations)

    # raises error if curve2 is empty
    if not curve2:
        raise ValueError("Curve2 is empty.")

    # fits curves into cubic Bézier curves
    curve_points1 = return_cubic_bezier(curve1)
    curve_points2 = return_cubic_bezier(curve2)

    return curve_points1, curve_points2


def fit_bezier_for_ll():
    """
    This function fits two cubic Bézier curves to the given data and saves them as templates for later comparison.
    Used only once for saving templates of the sign.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_ll.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_ll = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_ll)

    # generates Bezier curves
    bezier1, bezier2 = generate_two_cubic_beziers(locations)

    # Transform into numpy arrays
    bezier1 = np.array(bezier1)
    bezier2 = np.array(bezier2)

    # plots the first bezier curve
    plt.figure(figsize=(6, 6))
    plt.plot(bezier1[:, 0], bezier1[:, 1], label='Bezier 1')
    plt.scatter(bezier1[:, 0], bezier1[:, 1], s=10)

    # plots the second bezier curve
    plt.plot(bezier2[:, 0], bezier2[:, 1], label='Bezier 2')
    plt.scatter(bezier2[:, 0], bezier2[:, 1], s=10)

    # setting up the title and labels
    plt.title('Bezier Curves')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    # displays the legend
    plt.legend()

    # shows the plot
    plt.show()

    #
    # # saves the templates for future use
    # file_path_b1 = os.path.join(current_dir, 'bezier1_upper_curve_template.npy')
    # np.save(file_path_b1, bezier1)
    # file_path_b2 = os.path.join(current_dir, 'bezier2_lower_curve_template.npy')
    # np.save(file_path_b2, bezier2)
    #
    # # plots curves
    # plt.plot(bezier1[:, 0], bezier1[:, 1], color='blue')  # curve1 # plt.scatter([P0_curve1[0],
    # # P1_curve1[0]], [P0_curve1[1], P1_curve1[1]], color='red')  # control points for curve1
    # plt.plot(bezier2[:, 0], bezier2[:, 1], color='green')  # curve2 # plt.scatter([P0_curve2[0], P1_curve2[0]],
    # # [P0_curve2[1], P1_curve2[1]], color='red')  # control points for curve2
    #
    # plt.show()


if __name__ == '__main__':
    fit_bezier_for_ll()
