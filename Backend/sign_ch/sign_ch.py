"""
Sign 'CH' is a multi-touch gesture, where the index and middle-finger draw a line, each, on the palm of the
recipient. For recognition, each line is fitted into a Bezier curve, so that user-performed gestures can be
compared to the curve to determine accuracy.
"""
import os
import json
import math
import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt

from ..extraction import extract_timestamps_and_locations
from ..sign_a import timestamp_duration_valid


def linear_bezier_curve(p0: np.ndarray, p1: np.ndarray, t: np.ndarray) -> np.ndarray:
    """
    Function to calculate a linear Bézier curve.

    :param p0: The starting control point of the Bézier curve. It is a numpy array.
    :param p1: The ending control point of the Bézier curve. It is a numpy array.
    :param t: The parameter values, typically ranging from 0 to 1. It is a numpy array.

    :return: The computed Bézier curve as a numpy array.
    """
    return (1 - t)[:, None] * p0 + t[:, None] * p1


def euclidean_distance(point1, point2):
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

    # starts by putting the first point in curve1
    curve1.append(locations[0])
    for i in range(1, len(locations)):
        # assigns point to 
        if euclidean_distance(locations[i], curve1[-1]) <= 10:
            curve1.append(locations[i])
        else:
            curve2.append(locations[i])

    return curve1, curve2


def generate_two_linear_beziers(locations: List[List[float]]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate two linear Bézier curves given a list of touch locations.

    :param locations: The list of touch locations, where each location is a tuple of x and y coordinates.
    :return: Two numpy arrays, each representing a linear Bézier curve.
    """

    # splits touch locations into individual curves
    curve1, curve2 = split_touch_locations(locations)

    # fits curves into linear Bézier curves
    # control points for curve1
    P0_curve1 = np.array(curve1[0])
    P1_curve1 = np.array(curve1[-1])

    # control points for curve2
    P0_curve2 = np.array(curve2[0])
    P1_curve2 = np.array(curve2[-1])

    # assigns parameter values
    t = np.linspace(0, 1, num=100)

    # calculates points for curve1
    bezier1 = linear_bezier_curve(P0_curve1, P1_curve1, t=t)

    # calculates points for curve2
    bezier2 = linear_bezier_curve(P0_curve2, P1_curve2, t=t)

    return bezier1, bezier2


def fit_bezier_for_ch():
    """
    This function fits two Bézier curves to the given data and saves them as templates for later comparison.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_ch.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_ch = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_ch)

    # generates Bezier curves
    bezier1, bezier2 = generate_two_linear_beziers(locations)

    # saves the templates for future use
    file_path_b1 = os.path.join(current_dir, 'bezier1_upper_curve_template.npy')
    np.save(file_path_b1, bezier1)
    file_path_b2 = os.path.join(current_dir, 'bezier2_lower_curve_template.npy')
    np.save(file_path_b2, bezier2)

    # plots curves
    plt.plot(bezier1[:, 0], bezier1[:, 1], color='blue')  # curve1 # plt.scatter([P0_curve1[0],
    # P1_curve1[0]], [P0_curve1[1], P1_curve1[1]], color='red')  # control points for curve1
    plt.plot(bezier2[:, 0], bezier2[:, 1], color='green')  # curve2 # plt.scatter([P0_curve2[0], P1_curve2[0]],
    # [P0_curve2[1], P1_curve2[1]], color='red')  # control points for curve2
    #
    plt.show()


def is_sign_ch(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    Add docstring
    :return:
    """
    # checks if time frame is valid
    if not timestamp_duration_valid(timestamps):
        print("Duration too long")
        return False

    # splits location points into respective curves
    generate_two_linear_beziers(locations)

    # compares to template curves
    # loads the templates for future use
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b1 = os.path.join(current_dir, 'bezier1_upper_curve_template.npy')
    bezier1_upper_curve_template = np.load(file_path_b1)
    file_path_b2 = os.path.join(current_dir, 'bezier2_lower_curve_template.npy')
    bezier2_lower_curve_template = np.load(file_path_b2)

    # from fastdtw import fastdtw
    # from scipy.spatial.distance import euclidean
    #
    # def compare_sequences(seq1, seq2):
    #     """
    #     Compares two sequences using Dynamic Time Warping.
    #
    #     :param seq1: The first sequence.
    #     :param seq2: The second sequence.
    #     :return: The Dynamic Time Warping distance between the sequences.
    #     """
    #     distance, _ = fastdtw(seq1, seq2, dist=euclidean)
    #
    #     return distance


if __name__ == '__main__':
    # Makes web server listen on port 5000 and makes it externally visible by binding it to 0.0.0.0
    fit_bezier_for_ch()
