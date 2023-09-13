import json
import os
from typing import List
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from extraction import extract_timestamps_and_locations
from parameterisation import return_cubic_bezier, fit_quartic_bezier_control_points, return_quartic_bezier_curve
from recognition import compare_sequences_fdtw, timestamp_duration_valid  # compare_sequences_dtw

# matplotlib.use('Agg')


def fit_bezier_for_z_cubic():
    """
    This function fits a cubic Bézier curve to the given data and saves it as a template for later comparison.
    Used only once for saving templates of the sign 'Z'.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_z.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_z = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_z)

    # converts the touch locations into a Bézier curve
    curve_points = return_cubic_bezier(locations)

    # converts list of tuples to numpy array
    curve_points_np = np.array(curve_points)

    # saves the template for future use
    file_path_b = os.path.join(current_dir, 'bezier_curve_template_cubic.npy')
    np.save(file_path_b, curve_points_np)

    # plots curves
    plt.scatter([x[0] for x in locations], [x[1] for x in locations], color='red', s=5)
    plt.plot(curve_points_np[:, 0], curve_points_np[:, 1], color='green')

    plt.show()


def fit_bezier_for_z_quartic():
    """
        This function fits one quartic Bézier curve to the given data and saves them as templates for later comparison.
        Used only once for saving templates of the sign 'Z'.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_z.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_z = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_z)

    # generates Bezier curve control points
    bezier_control = fit_quartic_bezier_control_points(locations)

    # calculates and returns full curves
    bezier_curve = return_quartic_bezier_curve(bezier_control)

    # plots the first Bézier curve
    plt.figure(figsize=(6, 6))
    plt.plot(bezier_curve[:, 0], bezier_curve[:, 1], label='Bezier 1')
    plt.scatter(bezier_curve[:, 0], bezier_curve[:, 1], s=10)

    # setting up the title and labels
    plt.title('Bezier Curve')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    # displays the legend
    plt.legend()

    # shows the plot
    plt.show()

    # saves the templates for future use
    file_path_b1 = os.path.join(current_dir, 'bezier_curve_template_quartic.npy')
    np.save(file_path_b1, bezier_curve)


def is_sign_z_cubic(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "Z"
    according to a predefined template of the gesture.
    If the performed gesture deviates from the template by more than a certain threshold,
    the function returns False. Otherwise, it returns True.
    Recognition is compared to recognition using a quartic Bézier curve.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """
    # checks if time frame is valid
    if not timestamp_duration_valid('Z', timestamps):
        print("Duration too long")
        return False

    # creates cubic Bézier curve representing the user-performed gesture
    curve_points_user = return_cubic_bezier(locations)

    # loads the template for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b = os.path.join(current_dir, 'bezier_curve_template_cubic.npy')
    bezier_curve_template = np.load(file_path_b)

    # converts list of numpy arrays to a single 2D numpy array
    curve_points_user = np.vstack(curve_points_user)
    bezier_curve_template = np.vstack(bezier_curve_template)

    # # The code below saves a figure to see how the user curves compare to the templates
    # # Needs to uncomment agg at the top of the file
    # # creates a new figure
    # plt.figure()
    # # plots the template
    # plt.plot(bezier_curve_template[:, 0], bezier_curve_template[:, 1], label='Bezier 1 Template',
    #          linestyle='dashed')
    # # plots user curve
    # plt.plot(curve_points_user[:, 0], curve_points_user[:, 1], label='User Bezier 1')
    # # adds a legend
    # plt.legend()
    # # saves the plot
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # filename = os.path.join(current_dir, 'comparison_z_cubic.png')
    # plt.savefig(filename)
    # # closes the figure to free up memory
    # plt.close()

    # calculates distance using DTW
    distance_template = compare_sequences_fdtw(curve_points_user, bezier_curve_template)

    # debugging
    print(f"distance_template: {distance_template}")

    # compares if distance to template is below threshold
    if distance_template > 3000.0:
        return False

    return True


def is_sign_z_quartic(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "Z"
    according to a predefined template of the gesture.
    If the performed gesture deviates from the template by more than a certain threshold,
    the function returns False. Otherwise, it returns True.This one uses only one Bézier curve instead of trying
    to fit Ñ into two curves. This function is used to compare the accuracy as opposed to fitting the
    sign into a cubic curve.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """
    # checks if time frame is valid
    if not timestamp_duration_valid('Z', timestamps):
        print("Duration too long")
        return False

    # returns control points
    user_curve_control = fit_quartic_bezier_control_points(locations)

    # creates full Bezier curve
    user_curve_b = return_quartic_bezier_curve(user_curve_control)

    # loads the template for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b = os.path.join(current_dir, 'bezier_curve_template_quartic.npy')
    bezier_curve_template_quartic = np.load(file_path_b)

    # # The code below saves a figure to see how the user curves compare to the templates
    # # Needs to uncomment agg at the top of the file
    # # creates a new figure
    # plt.figure()
    # # plots the template
    # plt.plot(bezier_curve_template_quartic[:, 0], bezier_curve_template_quartic[:, 1], label='Bezier 1 Template',
    #          linestyle='dashed')
    # # plots user curves
    # plt.plot(user_curve_b[:, 0], user_curve_b[:, 1], label='User Bezier')
    #
    # # adds a legend
    # plt.legend()
    # # saves the plot
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # filename = os.path.join(current_dir, 'comparison_z_quartic.png')
    # plt.savefig(filename)
    # # closes the figure to free up memory
    # plt.close()

    # calculates DTW distance
    distance_template = compare_sequences_fdtw(user_curve_b, bezier_curve_template_quartic)

    print(f"distance_template: {distance_template}")

    if distance_template > 3000.0:
        return False

    return True


# # Code below already executed to fit template
# if __name__ == '__main__':
#     fit_bezier_for_z_cubic()
#     # fit_bezier_for_z_quartic()
