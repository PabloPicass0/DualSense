import json
import os
from typing import List

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import euclidean
from extraction import extract_timestamps_and_locations
from parameterisation import generate_two_quartic_beziers_control_points, return_two_quartic_bezier_curves
from recognition import timestamp_duration_valid, compare_sequences_fdtw
from extraction import split_touch_locations_two_curves


matplotlib.use('Agg')


def fit_bezier_for_ll():
    """
    This function fits two quartic Bézier curves to the given data and saves them as templates for later comparison.
    Used only once for saving templates of the sign ll.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_ll.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_ll = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_ll)

    # splits locations into both Bézier curves
    curve1, curve2 = split_touch_locations_two_curves('LL', locations)

    # generates Bezier curve control points
    bezier1_control, bezier2_control = generate_two_quartic_beziers_control_points(curve1, curve2)

    # calculates and returns full curves
    bezier1_curve, bezier2_curve = return_two_quartic_bezier_curves(bezier1_control, bezier2_control)

    # transforms into numpy arrays
    bezier1_curve_np = np.array(bezier1_curve)
    bezier2_curve_np = np.array(bezier2_curve)

    # plots the first Bézier curve
    # plt.figure(figsize=(6, 6))
    # plt.plot(bezier1_curve_np[:, 0], bezier1_curve_np[:, 1], label='Bezier 1')
    # plt.scatter(bezier1_curve_np[:, 0], bezier1_curve_np[:, 1], s=10)
    plt.plot(bezier1_curve_np[:, 0], bezier1_curve_np[:, 1], color='green')

    # plots the second Bézier curve
    # plt.plot(bezier2_curve_np[:, 0], bezier2_curve_np[:, 1], label='Bezier 2')
    # plt.scatter(bezier2_curve_np[:, 0], bezier2_curve_np[:, 1], s=10)
    plt.plot(bezier2_curve_np[:, 0], bezier2_curve_np[:, 1], color='green')

    # plots touch locations
    plt.scatter([x[0] for x in locations], [x[1] for x in locations], color='red', s=5)

    # setting up the title and labels
    # plt.title('Bezier Curves')
    # plt.xlabel('X Coordinate')
    # plt.ylabel('Y Coordinate')

    # displays the legend
    # plt.legend()

    # shows the plot
    plt.show()

    # saves the templates for future use
    file_path_b1 = os.path.join(current_dir, 'bezier1_upper_curve_template.npy')
    np.save(file_path_b1, bezier1_curve)
    file_path_b2 = os.path.join(current_dir, 'bezier2_lower_curve_template.npy')
    np.save(file_path_b2, bezier2_curve)


def is_sign_ll(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "LL"
    according to a predefined templates of the gesture. 'LL' uses two curves and has two templates.
    If the performed gesture deviates from the templates by more than a certain threshold,
    the function returns False. Otherwise, it returns True.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """
    # checks if time frame is valid
    if not timestamp_duration_valid('LL', timestamps):
        print("Duration too long")
        return False

    try:
        # splits locations into both Bézier curves
        curve1, curve2 = split_touch_locations_two_curves('LL', locations)
    except ValueError:
        print("\nCurve2 is empty")
        return False

    # returns control points for both Bezier points
    user_curve_1_control, user_curve_2_control = generate_two_quartic_beziers_control_points(curve1, curve2)

    # creates full Bezier curves
    user_curve_1_b, user_curve_2_b = return_two_quartic_bezier_curves(user_curve_1_control, user_curve_2_control)

    # loads the templates for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b1 = os.path.join(current_dir, 'bezier1_upper_curve_template.npy')
    bezier1_upper_curve_template = np.load(file_path_b1)
    file_path_b2 = os.path.join(current_dir, 'bezier2_lower_curve_template.npy')
    bezier2_lower_curve_template = np.load(file_path_b2)

    # # The code below saves a figure to see how the user curves compare to the templates
    # # Needs to uncomment agg at the top of the file
    # creates a new figure
    # plt.figure()
    # # plots the templates
    # plt.plot(bezier1_upper_curve_template[:, 0], bezier1_upper_curve_template[:, 1], label='Bezier 1 Template',
    #          linestyle='dashed')
    # plt.plot(bezier2_lower_curve_template[:, 0], bezier2_lower_curve_template[:, 1], label='Bezier 2 Template',
    #          linestyle='dashed')
    # # plots user curves
    # plt.plot(user_curve_1_b[:, 0], user_curve_1_b[:, 1], label='User Bezier 1')
    # plt.plot(user_curve_2_b[:, 0], user_curve_2_b[:, 1], label='User Bezier 2')
    # # adds a legend
    # plt.legend()
    # # saves the plot
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # filename = os.path.join(current_dir, 'output_figure.png')
    # plt.savefig(filename)
    # # closes the figure to free up memory
    # plt.close()

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

    if distance1_template > 7000.0 or distance2_template > 7000.0:
        return False

    return True


# # Code below already executed to fit template
# if __name__ == '__main__':
#     fit_bezier_for_ll()
