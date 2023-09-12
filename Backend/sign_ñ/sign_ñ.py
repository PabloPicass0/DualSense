import json
import os
from typing import List

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import euclidean

from extraction import extract_timestamps_and_locations, split_touch_locations_two_curves
from parameterisation import fit_quartic_bezier_control_points, return_quartic_bezier_curve, \
    return_two_quartic_bezier_curves, generate_two_quartic_beziers_control_points
from recognition import timestamp_duration_valid, compare_sequences_fdtw

matplotlib.use('Agg')


def fit_bezier_for_ñ_two_curves():
    """
    This function fits two quartic Bézier curves to the given data and saves them as templates for later comparison.
    Used only once for saving templates of the sign ñ.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_ñ.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_ñ = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_ñ)

    # splits touch locations into individual curves
    curve1, curve2 = split_touch_locations_two_curves('Ñ', locations)

    # generates Bezier curve control points
    bezier1_control, bezier2_control = generate_two_quartic_beziers_control_points(curve1, curve2)

    # calculates and returns full curves
    bezier1_curve, bezier2_curve = return_two_quartic_bezier_curves(bezier1_control, bezier2_control)

    # transforms into numpy arrays
    bezier1_curve_np = np.array(bezier1_curve)
    bezier2_curve_np = np.array(bezier2_curve)

    # Code below plots fitted Bézier curves; comment 'matplotlib.use('Agg')' to run
    # plots the first Bézier curve
    # plt.figure(figsize=(6, 6))
    plt.plot(bezier1_curve_np[:, 0], bezier1_curve_np[:, 1], color='green')
    # plt.scatter(bezier1_curve_np[:, 0], bezier1_curve_np[:, 1], s=10)

    # plots the second Bézier curve
    plt.plot(bezier2_curve_np[:, 0], bezier2_curve_np[:, 1], color='green')
    # plt.scatter(bezier2_curve_np[:, 0], bezier2_curve_np[:, 1], s=10)

    # plots touch locations
    plt.scatter([x[0] for x in locations], [x[1] for x in locations], color='red', s=5)

    # # setting up the title and labels
    # plt.title('Bezier Curves')
    # plt.xlabel('X Coordinate')
    # plt.ylabel('Y Coordinate')

    # # displays the legend
    # plt.legend()

    # shows the plot
    plt.show()

    # saves the templates for future use
    file_path_b1 = os.path.join(current_dir, 'bezier1_curve_template.npy')
    np.save(file_path_b1, bezier1_curve)
    file_path_b2 = os.path.join(current_dir, 'bezier2_curve_template.npy')
    np.save(file_path_b2, bezier2_curve)


# Function below currently not implemented in endpoint as accuracy is lower than with single function
def is_sign_ñ_two_curves(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "Ñ"
    according to a predefined template of the gesture.
    If the performed gesture deviates from the template by more than a certain threshold,
    the function returns False. Otherwise, it returns True.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """
    # checks if time frame is valid
    if not timestamp_duration_valid('Ñ', timestamps):
        print("Duration too long")
        return False

    try:
        # splits location points into respective curves and returns control points
        curve1, curve2 = split_touch_locations_two_curves('Ñ', locations)
    except ValueError:
        print("\nCurve2 is empty")
        return False

    # generates Bezier control points
    user_curve_1_control, user_curve_2_control = generate_two_quartic_beziers_control_points(curve1, curve2)

    # creates full Bezier curves
    user_curve_1_b, user_curve_2_b = return_two_quartic_bezier_curves(user_curve_1_control, user_curve_2_control)

    # loads the templates for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b1 = os.path.join(current_dir, 'bezier1_curve_template.npy')
    bezier1_upper_curve_template = np.load(file_path_b1)
    file_path_b2 = os.path.join(current_dir, 'bezier2_curve_template.npy')
    bezier2_lower_curve_template = np.load(file_path_b2)

    # The code below saves a figure to see how the user curves compare to the templates
    # Needs to uncomment agg at the top of the file
    # creates a new figure
    plt.figure()
    # plots the templates
    plt.plot(bezier1_upper_curve_template[:, 0], bezier1_upper_curve_template[:, 1], color='green')
    plt.plot(bezier2_lower_curve_template[:, 0], bezier2_lower_curve_template[:, 1], color='green')
    # plots user curves
    plt.plot(user_curve_1_b[:, 0], user_curve_1_b[:, 1], color='red', linestyle='dashed')
    plt.plot(user_curve_2_b[:, 0], user_curve_2_b[:, 1], color='red', linestyle='dashed')
    # adds a legend
    # plt.legend()
    # saves the plot
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'output_figure_two.png')
    plt.savefig(filename)
    # closes the figure to free up memory
    plt.close()

    # calculates the Euclidean distance between the first point of user's curves and the first point of the templates
    dist1 = euclidean(user_curve_1_b[0], bezier1_upper_curve_template[0])
    dist2 = euclidean(user_curve_1_b[0], bezier2_lower_curve_template[0])

    if dist1 < dist2:
        # if the first point of user_curve_1 is closer to bezier1
        distance1_template = compare_sequences_fdtw(user_curve_1_b, bezier1_upper_curve_template)
        distance2_template = compare_sequences_fdtw(user_curve_2_b, bezier2_lower_curve_template)
    else:
        # if the first point of user_curve_1 is closer to bezier2
        distance1_template = compare_sequences_fdtw(user_curve_1_b, bezier2_lower_curve_template)
        distance2_template = compare_sequences_fdtw(user_curve_2_b, bezier1_upper_curve_template)

    print(f"distance1_template: {distance1_template}")
    print(f"distance2_template: {distance2_template}")

    if distance1_template > 5000.0 or distance2_template > 5000.0:
        return False

    return True


def fit_bezier_for_ñ_single_curve():
    """
    This function fits one quartic Bézier curve to the given data and saves them as templates for later comparison.
    Used only once for saving templates of the sign ñ. This is used to compare the accuracy as opposed to fitting the
    sign with two Bézier curves.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_ñ.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_ñ = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_ñ)

    # generates Bezier curve control points
    bezier_control = fit_quartic_bezier_control_points(locations)

    # calculates and returns full curves
    bezier_curve = return_quartic_bezier_curve(bezier_control)

    # transforms into numpy arrays
    bezier_curve_np = np.array(bezier_curve)

    # Code below plots fitted Bézier curves
    # plots Bézier curve
    # plt.figure(figsize=(6, 6))
    plt.plot(bezier_curve_np[:, 0], bezier_curve_np[:, 1], color='green')
    # plt.scatter(bezier_curve_np[:, 0], bezier_curve_np[:, 1], s=10)

    # # setting up the title and labels
    # plt.title('Bezier Curves')
    # plt.xlabel('X Coordinate')
    # plt.ylabel('Y Coordinate')

    # displays the legend
    # plt.legend()

    # plot touch curve
    # splits touch locations into individual curves
    # curve1, curve2 = split_touch_locations_two_curves('Ñ', locations)
    # curve1 = np.array(curve1)
    # curve2 = np.array(curve2)
    # plt.plot(curve1[:, 0], curve1[:, 1], color='red')
    # plt.plot(curve2[:, 0], curve2[:, 1], color='red')
    plt.scatter([x[0] for x in locations], [x[1] for x in locations], color='red', s=5)

    # shows the plot
    plt.show()

    # saves the templates for future use
    file_path_b = os.path.join(current_dir, 'bezier_curve_single_template.npy')
    np.save(file_path_b, bezier_curve)


def is_sign_ñ_single_curve(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "Ñ"
    according to a predefined template of the gesture.
    If the performed gesture deviates from the template by more than a certain threshold,
    the function returns False. Otherwise, it returns True.This one uses only one Bézier curve instead of trying
    to fit Ñ into two curves. This is used to compare the accuracy as opposed to fitting the
    sign with two Bézier curves.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """
    # checks if location inputs are valid by assessing number of touch points
    if len(locations) < 20:
        return False

    # checks if time frame is valid
    if not timestamp_duration_valid('Ñ', timestamps):
        print("Duration too long")
        return False

    # returns control points
    user_curve_control = fit_quartic_bezier_control_points(locations)

    # creates full Bezier curve
    user_curve_b = return_quartic_bezier_curve(user_curve_control)

    # loads the template for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b = os.path.join(current_dir, 'bezier_curve_single_template.npy')
    bezier_curve_single_template = np.load(file_path_b)

    # The code below saves a figure to see how the user curves compare to the templates
    # Needs to uncomment agg at the top of the file
    # creates a new figure
    plt.figure()
    # plots the template
    plt.plot(bezier_curve_single_template[:, 0], bezier_curve_single_template[:, 1], color='green')
    # plots user curves
    plt.plot(user_curve_b[:, 0], user_curve_b[:, 1], color='red', linestyle='dashed')

    # # adds a legend
    # plt.legend()
    # saves the plot
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'output_figure_single.png')
    plt.savefig(filename)
    # closes the figure to free up memory
    plt.close()

    # calculates DTW distance
    distance_template = compare_sequences_fdtw(user_curve_b, bezier_curve_single_template)

    print(f"distance_template: {distance_template}")

    # captures the very different sign, usually the first --> this is the random single few points when the gesture
    # terminates
    if distance_template > 20000:
        print("large distance print")
        plt.figure()
        # plots the template
        plt.plot(bezier_curve_single_template[:, 0], bezier_curve_single_template[:, 1], label='Bezier 1 Template',
                 linestyle='dashed')
        # plots user curves
        plt.plot(user_curve_b[:, 0], user_curve_b[:, 1], label='User Bezier')

        # adds a legend
        plt.legend()
        # saves the plot
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(current_dir, 'output_figure_single_high_distance.png')
        plt.savefig(filename)
        # closes the figure to free up memory
        plt.close()

    if distance_template > 3000.0:
        return False

    return True


# # Code below already executed to fit template
# if __name__ == '__main__':
#     # fits two curves
#     fit_bezier_for_ñ_two_curves()
#     # fits one curve
#     # fit_bezier_for_ñ_single_curve()
