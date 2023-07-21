"""
Sign 'CH' is a multitouch gesture, where the index and middle-finger draw a line, each, on the palm of the
recipient. For recognition, each line is fitted into a Bézier curve, so that user-performed gestures can be
compared to the curve to determine accuracy.
"""
import os
import json
import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt

from extraction import extract_timestamps_and_locations
from extraction import euclidean_distance
from parameterisation import linear_bezier_curve
from recognition import compare_sequences
from sign_a.sign_a import timestamp_duration_valid


def split_touch_locations(locations: List[List[float]]) -> Tuple[
    List[List[float]], List[List[float]]]:
    """
    Splits the provided locations into two curves based on a distance threshold.

    :param locations: A list of tuples, each representing the (x, y) coordinates of a point.

    :return: Two lists of tuples, each list represents a curve and each tuple within the list represents a point on the
    curve.
    """
    curve1 = []
    curve2 = []

    # starts by putting the first point in curve1
    curve1.append(locations[0])
    for i in range(1, len(locations)):
        # assigns point to either curve1 or curve2 depending on distance
        if euclidean_distance(locations[i], curve1[-1]) <= 10:
            curve1.append(locations[i])
        else:
            curve2.append(locations[i])

    return curve1, curve2


def generate_two_linear_beziers(locations: List[List[float]]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates two linear Bézier curves given a list of touch locations.

    :param locations: The list of touch locations, where each location is a tuple of x and y coordinates.
    :return: Two numpy arrays, each representing a linear Bézier curve.
    """

    # splits touch locations into individual curves
    curve1, curve2 = split_touch_locations(locations)

    # raises error if curve2 is empty
    if not curve2:
        raise ValueError("Curve2 is empty.")

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
    Used only once for saving templates of the sign.
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

    plt.show()


def is_sign_ch(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "CH"
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

    try:
        # splits location points into respective curves
        user_curve_1, user_curve_2 = generate_two_linear_beziers(locations)
    except ValueError:
        print("\nCurve2 is empty")
        return False

    # loads the templates for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b1 = os.path.join(current_dir, 'bezier1_upper_curve_template.npy')
    bezier1_upper_curve_template = np.load(file_path_b1)
    file_path_b2 = os.path.join(current_dir, 'bezier2_lower_curve_template.npy')
    bezier2_lower_curve_template = np.load(file_path_b2)

    # calculates the Euclidean distance between the first point of user's curves and the first point of the templates
    dist1 = euclidean_distance(user_curve_1[0], bezier1_upper_curve_template[0])
    dist2 = euclidean_distance(user_curve_1[0], bezier2_lower_curve_template[0])

    if dist1 < dist2:
        # if the first point of user_curve_1 is closer to bezier1
        distance1_template = compare_sequences(user_curve_1, bezier1_upper_curve_template)
        distance2_template = compare_sequences(user_curve_2, bezier2_lower_curve_template)
    else:
        # if the first point of user_curve_1 is closer to bezier2
        distance1_template = compare_sequences(user_curve_1, bezier2_lower_curve_template)
        distance2_template = compare_sequences(user_curve_2, bezier1_upper_curve_template)

    print(f"distance1_template: {distance1_template}")
    print(f"distance2_template: {distance2_template}")

    if distance1_template > 5000.0 or distance2_template > 5000.0:
        return False

    return True

# if __name__ == '__main__':
#     # already executed to save templates
#     fit_bezier_for_ch()
