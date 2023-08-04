import json
import os
from typing import List

import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import euclidean

from extraction import extract_timestamps_and_locations, split_touch_locations_three_curves
from parameterisation import fit_quartic_bezier_control_points, return_quartic_bezier_curve, \
    generate_two_quartic_beziers_control_points, return_two_quartic_bezier_curves
from recognition import timestamp_duration_valid, compare_sequences_fdtw, compare_sequences_dtw


def fit_three_beziers_for_w():
    """
    This function fits three quartic Bézier curves to the given data and saves them as templates for later comparison.
    Used only once for saving templates of the sign w. This is done to compare the accuracy of three Bézier curves as
    compared to only one.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_w.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_w = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_w)

    # splits locations into its three curves
    curve1, curve2, curve3 = split_touch_locations_three_curves(locations)

    # fits bezier control points
    bezier1_control, bezier2_control = generate_two_quartic_beziers_control_points(curve1, curve2)
    bezier3_control = fit_quartic_bezier_control_points(curve3)

    # calculates and returns full curves
    bezier1_curve, bezier2_curve = return_two_quartic_bezier_curves(bezier1_control, bezier2_control)
    bezier3_curve = return_quartic_bezier_curve(bezier3_control)

    # transforms into numpy arrays
    bezier1_curve_np = np.array(bezier1_curve)
    bezier2_curve_np = np.array(bezier2_curve)
    bezier3_curve_np = np.array(bezier3_curve)

    # plots the first Bézier curve
    plt.figure(figsize=(6, 6))
    plt.plot(bezier1_curve_np[:, 0], bezier1_curve_np[:, 1], label='Bezier 1')
    plt.scatter(bezier1_curve_np[:, 0], bezier1_curve_np[:, 1], s=10)
    # plots the second Bézier curve
    plt.plot(bezier2_curve_np[:, 0], bezier2_curve_np[:, 1], label='Bezier 2')
    plt.scatter(bezier2_curve_np[:, 0], bezier2_curve_np[:, 1], s=10)
    # plots the third Bézier curve
    plt.plot(bezier3_curve_np[:, 0], bezier3_curve_np[:, 1], label='Bezier 2')
    plt.scatter(bezier3_curve_np[:, 0], bezier3_curve_np[:, 1], s=10)

    # setting up the title and labels
    plt.title('Bezier Curves')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    # displays the legend
    plt.legend()

    # shows the plot
    plt.show()

    # saves the templates for future use
    file_path_b1 = os.path.join(current_dir, 'bezier1_curve_template.npy')
    np.save(file_path_b1, bezier1_curve)
    file_path_b2 = os.path.join(current_dir, 'bezier2_curve_template.npy')
    np.save(file_path_b2, bezier2_curve)
    file_path_b3 = os.path.join(current_dir, 'bezier3_curve_template.npy')
    np.save(file_path_b3, bezier3_curve)


def fit_bezier_for_w_single_curve():
    """
    This function fits one quartic Bézier curve to the given data and saves it as template for later comparison.
    Used only once for saving templates of the sign w. This is used to compare the accuracy as opposed to fitting the
    sign with two Bézier curves.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_w.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_w = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_w)

    # generates Bezier curve control points
    bezier_control = fit_quartic_bezier_control_points(locations)

    # calculates and returns full curves
    bezier_curve = return_quartic_bezier_curve(bezier_control)

    # Code below plots fitted Bézier curves
    # transforms into numpy arrays
    # bezier_curve_np = np.array(bezier_curve)

    # plots Bézier curve
    # plt.figure(figsize=(6, 6))
    # plt.plot(bezier_curve_np[:, 0], bezier_curve_np[:, 1], label='Bezier 1')
    # plt.scatter(bezier_curve_np[:, 0], bezier_curve_np[:, 1], s=10)
    #
    # # setting up the title and labels
    # plt.title('Bézier curves')
    # plt.xlabel('X Coordinate')
    # plt.ylabel('Y Coordinate')
    #
    # # displays the legend
    # plt.legend()
    #
    # # shows the plot
    # plt.show()
    #
    # # saves the templates for future use
    # file_path_b = os.path.join(current_dir, 'bezier_curve_single_template.npy')
    # np.save(file_path_b, bezier_curve)


def is_sign_w_single_curve(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "W"
    according to a predefined template of the gesture.
    If the performed gesture deviates from the template by more than a certain threshold,
    the function returns False. Otherwise, it returns True.This function uses only one Bézier curve instead of trying
    to fit W into three curves. This is used to compare the accuracy as opposed to fitting the
    sign with three Bézier curves.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """

    # checks if time frame is valid
    if not timestamp_duration_valid('W', timestamps):
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
    plt.plot(bezier_curve_single_template[:, 0], bezier_curve_single_template[:, 1], label='Bezier 1 Template',
             linestyle='dashed')
    # plots user curves
    plt.plot(user_curve_b[:, 0], user_curve_b[:, 1], label='User Bezier')

    # adds a legend
    plt.legend()
    # saves the plot
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'output_figure_single.png')
    plt.savefig(filename)
    # closes the figure to free up memory
    plt.close()

    # calculates DTW distance
    distance_template = compare_sequences_fdtw(user_curve_b, bezier_curve_single_template)

    print(f"distance_template: {distance_template}")

    if distance_template > 3000.0:
        return False

    return True


def is_sign_w_three_curves(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "W"
    according to a predefined templates of the gesture.
    If the performed gesture deviates from the templates by more than a certain threshold,
    the function returns False. Otherwise, it returns True.This function uses only one Bézier curve instead of trying
    to fit W into three curves. This is used to compare the accuracy as opposed to fitting the
    sign with three Bézier curves.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """

    # checks if time frame is valid
    if not timestamp_duration_valid('W', timestamps):
        print("Duration too long")
        return False

    try:
        # splits user touch locations into three curves
        curve1, curve2, curve3 = split_touch_locations_three_curves(locations)
    except ValueError as error:
        print(f"ValueError: {error}")
        return False

    # fits user touch locations into Bézier curve
    # fits bezier control points
    user1_control, user2_control = generate_two_quartic_beziers_control_points(curve1, curve2)
    user3_control = fit_quartic_bezier_control_points(curve3)
    # calculates and returns full curves
    user1_curve_bezier, user2_curve_bezier = return_two_quartic_bezier_curves(user1_control, user2_control)
    user3_curve_bezier = return_quartic_bezier_curve(user3_control)

    # loads the templates for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b1 = os.path.join(current_dir, 'bezier1_curve_template.npy')
    bezier1_curve_template = np.load(file_path_b1)
    file_path_b2 = os.path.join(current_dir, 'bezier2_curve_template.npy')
    bezier2_curve_template = np.load(file_path_b2)
    file_path_b3 = os.path.join(current_dir, 'bezier3_curve_template.npy')
    bezier3_curve_template = np.load(file_path_b3)

    # The code below saves a figure to see how the user curves compare to the templates
    # Needs to uncomment agg at the top of the file
    # creates a new figure
    plt.figure()
    # plots the templates
    plt.plot(bezier1_curve_template[:, 0], bezier1_curve_template[:, 1], label='Bezier 1 Template',
             linestyle='dashed')
    plt.plot(bezier2_curve_template[:, 0], bezier2_curve_template[:, 1], label='Bezier 2 Template',
             linestyle='dashed')
    plt.plot(bezier3_curve_template[:, 0], bezier3_curve_template[:, 1], label='Bezier 3 Template',
             linestyle='dashed')
    # plots user curves
    plt.plot(user1_curve_bezier[:, 0], user1_curve_bezier[:, 1], label='User Bezier 1')
    plt.plot(user2_curve_bezier[:, 0], user2_curve_bezier[:, 1], label='User Bezier 2')
    plt.plot(user3_curve_bezier[:, 0], user3_curve_bezier[:, 1], label='User Bezier 3')
    # adds a legend
    plt.legend()
    # saves the plot
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'output_figure_three_curves.png')
    plt.savefig(filename)
    # closes the figure to free up memory
    plt.close()

    # matches curves
    template_curves = [bezier1_curve_template, bezier2_curve_template, bezier3_curve_template]
    user_curves = [user1_curve_bezier, user2_curve_bezier, user3_curve_bezier]
    # calculate distances between first point of user curves and templates
    distances = []

    # for each user curve
    for user_curve in user_curves:
        distances_for_this_curve = []
        # calculates the distance to each template
        for template_curve in template_curves:
            distance = euclidean(user_curve[0], template_curve[0])
            distances_for_this_curve.append(distance)
        distances.append(distances_for_this_curve)

    # assigns each user curve to the closest template
    assignments = []
    for i in range(3):
        min_distance_index = np.argmin(distances[i])
        assignments.append(min_distance_index)

    # compares user curves to templates
    for i in range(3):
        assigned_template = template_curves[assignments[i]]
        distance_template = compare_sequences_dtw(user_curves[i], assigned_template)
        # prints the distance to the respective template
        print(f"distance{assignments[i] + 1}_template: {distance_template}")
        if distance_template > 5000:
            return False

    return True


# # executed once to create the template
# if __name__ == '__main__':
#     # fit_bezier_for_w_single_curve()
#     fit_three_beziers_for_w()
